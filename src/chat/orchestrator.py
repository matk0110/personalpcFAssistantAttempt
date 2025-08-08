from __future__ import annotations
from datetime import date, datetime, timedelta
from decimal import Decimal, InvalidOperation
from typing import List
from pathlib import Path
import logging

from core import JsonFilePersistence
from services.transactions import TransactionService
from services.budgets import BudgetService
from services.receipts import SimpleReceiptParser
from services.categories import CategoryResolver
from .intent import IntentParser
from llm.adapter import MockLLMAdapter

# Configure basic logger
logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
logger = logging.getLogger("chat")

HELP_TEXT = """Commands:\n add 12.34 groceries milk and bread [on YYYY-MM-DD]\n set <category> <limit>  # set budget limit for category\n budget [category]\n limits  # list configured limits\n receipt: <paste receipt text>\n summary 7d|30d\n export csv [path]\n help"""

class ChatOrchestrator:
    def __init__(self, data_path: str = "data/state.json"):
        self.store = JsonFilePersistence(Path(data_path))  # type: ignore
        self.txn_service = TransactionService(self.store)
        self.budget_service = BudgetService(self.store)
        self.intent_parser = IntentParser()
        self.receipt_parser = SimpleReceiptParser(CategoryResolver())
        self.llm = MockLLMAdapter()
        # Onboarding state
        self._onboarding_active = True
        self._onboarding_step = 0
        self._pending_categories: list[tuple[str, str]] = []  # (name, limit_str)

    # ---------------- Onboarding Helpers -----------------
    def onboarding_banner(self) -> str:
        return (
            "Welcome! Let's set up a few budget categories. "
            "You can type 'skip' anytime to exit the guide.\n"
            "Example categories: groceries, rent, transport, fun, dining.\n"
            "First, how many categories do you want to start with? (1-10)"
        )

    def _onboarding_handle(self, text: str) -> str:
        t = text.strip()
        lower = t.lower()
        if lower == "skip":
            self._onboarding_active = False
            return "Onboarding skipped. Type 'help' for commands." 

        # Step 0: ask count
        if self._onboarding_step == 0:
            try:
                count = int(t)
            except ValueError:
                return "Please enter a number 1-10 for how many categories (or 'skip')."
            if not (1 <= count <= 10):
                return "Enter a number between 1 and 10 (or 'skip')."
            self._onboarding_step = 1
            self._onboarding_target_count = count  # type: ignore
            return (
                "Great. Now enter each category and its monthly limit one per line.\n"
                "Format: name limit  (example: groceries 400)\n"
                f"Need {count} lines. When done, type 'done'."
            )

        # Step 1: collect lines until done
        if self._onboarding_step == 1:
            if lower == "done":
                if not getattr(self, "_onboarding_target_count", 0):  # safety
                    return "No categories captured. Enter at least one line or 'skip'."
                if len(self._pending_categories) == 0:
                    return "You haven't added any lines yet. Add at least one or 'skip'."
                # Persist collected categories
                month = self.budget_service.month_key(date.today())
                updates = {}
                for name, limit_str in self._pending_categories:
                    try:
                        updates[name.title()] = Decimal(limit_str)
                    except Exception:
                        pass  # ignore bad line silently
                if updates:
                    self.budget_service.set_limits(month, updates)
                    cats_list = ", ".join(f"{k}:{v:.2f}" for k, v in updates.items())
                    self._onboarding_active = False
                    return (
                        "Setup complete. Added limits: " + cats_list + "\n" \
                        "You can now add expenses, e.g.: add 12.50 groceries milk and bread"
                    )
                return "No valid categories parsed. Enter lines like: groceries 300"
            # Parse a line
            parts = t.split()
            if len(parts) != 2:
                return "Line format is: <name> <limit> (example: dining 150). Or 'done'."
            name, limit = parts
            try:
                _ = Decimal(limit)
            except Exception:
                return "Limit must be a number. Try again or 'done'."
            self._pending_categories.append((name, limit))
            remaining_needed = getattr(self, "_onboarding_target_count", 0) - len(self._pending_categories)
            if remaining_needed > 0:
                return f"Added {name}. Need {remaining_needed} more."
            else:
                return "You've entered the target count. Type 'done' to finish or add more lines (max 15)."
        return "Onboarding state error. Type 'skip' to exit."

    def _friendly_remaining(self, line: dict | None) -> str:
        if not line:
            return "n/a"
        # hide negative remaining when limit is zero (auto-created category w/out configured limit)
        try:
            limit = Decimal(line.get("limit", "0"))
            remaining = Decimal(line.get("remaining", "0"))
        except Exception:
            return line.get("remaining", "n/a")
        if limit == 0:
            # show spent only
            return f"spent {line['spent']} (no limit)"
        return str(remaining)

    def handle(self, text: str) -> str:
        # If onboarding active and no budgets exist yet, divert flow
        if self._onboarding_active:
            month = self.budget_service.month_key(date.today())
            if self.budget_service.summary(month):
                self._onboarding_active = False
            else:
                stripped = text.strip()
                # Trigger banner only on empty input or explicit 'start'
                if self._onboarding_step == 0 and stripped == "":
                    return self.onboarding_banner()
                if stripped.lower() == "start" and self._onboarding_step == 0:
                    return "Enter how many categories (1-10) or 'skip'."
                # If we are already in step collection (user previously gave count)
                if self._onboarding_step > 0:
                    return self._onboarding_handle(text)
                # If user issued a command, allow normal intent parsing to proceed (no early onboarding)
                # Detect if text looks like a command by simple prefix keywords
                if any(stripped.lower().startswith(pfx) for pfx in ["add ", "set ", "budget", "limits", "receipt:", "summary", "export", "help"]):
                    self._onboarding_active = False  # user prefers to dive right in
                else:
                    # If it doesn't look like a command and not empty, attempt onboarding interpretation
                    if self._onboarding_step == 0 and stripped:
                        return self._onboarding_handle(text)

        intent = self.intent_parser.parse(text)
        if not intent:
            return "Could not understand. Type 'help'."
        name = intent.name
        args = intent.args
        try:
            if name == "help":
                return HELP_TEXT
            if name == "add_expense":
                try:
                    amount = Decimal(args["amount"])
                except (KeyError, InvalidOperation):
                    return "Invalid amount. Example: add 12.34 groceries milk"
                if amount <= 0:
                    return "Amount must be positive."
                cat = args["category"].title()
                desc = (args.get("desc") or cat).strip()
                raw_date = args.get("date")
                txn_date = None
                if raw_date:
                    try:
                        txn_date = datetime.strptime(raw_date, "%Y-%m-%d").date()
                    except ValueError:
                        return "Invalid date format. Use YYYY-MM-DD."
                txn = self.txn_service.add(amount=amount, category=cat, description=desc, txn_date=txn_date)
                self.budget_service.apply(txn)
                month = self.budget_service.month_key(txn.txn_date)
                summary = self.budget_service.summary(month)
                line = next((s for s in summary if s["category"].lower() == cat.lower()), None)
                remain = self._friendly_remaining(line)
                return f"Added {amount:.2f} to {cat}. Remaining: {remain}."
            if name == "set_budget":
                cat = args["category"].title()
                try:
                    limit = Decimal(args["limit"])
                except Exception:
                    return "Invalid limit. Use set groceries 300"
                if limit < 0:
                    return "Limit must be non-negative."
                month = self.budget_service.month_key(date.today())
                self.budget_service.set_limits(month, {cat: limit})
                return f"Set {cat} limit to {limit:.2f}."
            if name == "show_budget":
                month = self.budget_service.month_key(date.today())
                summary = self.budget_service.summary(month)
                if not summary:
                    return "No budget yet. Add expenses to start tracking."
                cat = args.get("category")
                if cat:
                    cat = cat.title()
                    line = next((s for s in summary if s["category"] == cat), None)
                    if not line:
                        return f"No data for {cat}."
                    rem = self._friendly_remaining(line)
                    if rem.startswith("spent"):
                        return f"{cat}: spent {line['spent']} (no limit)"
                    return f"{cat}: spent {line['spent']} / {line['limit']} (remaining {rem})"
                rows = []
                for s in summary:
                    rem = self._friendly_remaining(s)
                    if rem.startswith("spent"):
                        rows.append(f"{s['category']}: {rem}")
                    else:
                        rows.append(f"{s['category']}: {s['spent']}/{s['limit']} rem {rem}")
                return "Budget\n" + "\n".join(rows)
            if name == "limits":
                month = self.budget_service.month_key(date.today())
                limits = self.budget_service.list_limits(month)
                if not limits:
                    return "No limits configured yet. Use set <category> <limit>."
                lines = [f"{l['category']}: {l['limit']}" for l in limits]
                return "Limits\n" + "\n".join(lines)
            if name == "export":
                target = args.get("target", "csv").lower()
                if target != "csv":
                    return "Only csv export supported currently."
                path = args.get("path") or "export/transactions.csv"
                count = self.txn_service.export_csv(path)
                return f"Exported {count} transactions to {path}."
            if name == "receipt":
                body = args.get("body", "").strip()
                if not body:
                    return "Empty receipt body. Use 'receipt:' then lines like 'Milk 2.50'"
                result = self.receipt_parser.parse(body)
                txns = self.receipt_parser.to_transactions(result)
                for txn in txns:
                    self.txn_service.add(amount=txn.amount, category=txn.category, description=txn.description)
                warn_msg = f" Warnings: {len(result.warnings)}" if result.warnings else ""
                return f"Parsed {len(txns)} lines.{warn_msg}"
            if name == "summary":
                window = args.get("window", "7d")
                try:
                    days = int(window[:-1]) if window.endswith('d') else 7
                except ValueError:
                    return "Invalid window. Use e.g. summary 7d"
                cutoff = datetime.utcnow() - timedelta(days=days)
                txns = [t for t in self.txn_service.list() if datetime.combine(t.txn_date, datetime.min.time()) >= cutoff]
                total = sum(t.amount for t in txns)
                return f"Last {days}d: {total:.2f} across {len(txns)} transactions."
            return "Unhandled intent."
        except Exception as e:
            logger.exception("Unhandled error processing intent %s", name)
            return f"Error: {e}"