from __future__ import annotations
import re
from typing import List
from decimal import Decimal
from core import ReceiptLine, ReceiptParseResult, Transaction
from .categories import CategoryResolver

LINE_RE = re.compile(r"^(?P<desc>.+?)\s+(?P<amount>\d+[\.,]\d{2})$")

class SimpleReceiptParser:
    def __init__(self, category_resolver: CategoryResolver | None = None):
        self.category_resolver = category_resolver or CategoryResolver()

    def parse(self, text: str) -> ReceiptParseResult:
        lines: List[ReceiptLine] = []
        warnings: List[str] = []
        total_detected = None
        for raw in [l.strip() for l in text.splitlines() if l.strip()]:
            m = LINE_RE.match(raw)
            if not m:
                # try detect total
                if raw.lower().startswith("total"):
                    amt = re.findall(r"\d+[\.,]\d{2}", raw)
                    if amt:
                        total_detected = Decimal(amt[-1].replace(",", "."))
                    continue
                warnings.append(f"Unparsed line: {raw}")
                continue
            amt = Decimal(m.group("amount").replace(",", "."))
            desc = m.group("desc").strip()
            lines.append(ReceiptLine(raw=raw, description=desc, amount=amt))
        return ReceiptParseResult(original_text=text, lines=lines, total_detected=total_detected, warnings=warnings)

    def to_transactions(self, result: ReceiptParseResult, default_category: str = "Other"):
        txns: List[Transaction] = []
        for line in result.lines:
            cat = self.category_resolver.resolve(line.description)
            txns.append(Transaction.create(amount=line.amount, category=cat, description=line.description))
        return txns