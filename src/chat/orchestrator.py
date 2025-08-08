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

HELP_TEXT = """Commands:\n add 12.34 groceries milk and bread\n budget [category]\n receipt: <paste receipt text>\n summary 7d|30d\n help\n"""

class ChatOrchestrator:
    def __init__(self, data_path: str = "data/state.json"):
        self.store = JsonFilePersistence(Path(data_path))  # type: ignore
        self.txn_service = TransactionService(self.store)
        self.budget_service = BudgetService(self.store)
        self.intent_parser = IntentParser()
        self.receipt_parser = SimpleReceiptParser(CategoryResolver())
        self.llm = MockLLMAdapter()

    def handle(self, text: str) -> str:
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
                remain = line["remaining"] if line else "n/a"
                return f"Added {amount:.2f} to {cat}. Remaining: {remain}."
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
                    return f"{cat}: spent {line['spent']} / {line['limit']} (remaining {line['remaining']})"
                rows = [f"{s['category']}: {s['spent']}/{s['limit']} rem {s['remaining']}" for s in summary]
                return "Budget\n" + "\n".join(rows)
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