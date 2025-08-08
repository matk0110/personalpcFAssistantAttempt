from __future__ import annotations
from dataclasses import dataclass, field
from datetime import date, datetime
from typing import List, Optional, Dict, Any
import uuid
from decimal import Decimal, ROUND_HALF_UP

Money = Decimal  # alias for clarity


def _money(value: Any) -> Money:
    if isinstance(value, Decimal):
        return value.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
    return Decimal(str(value)).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)


@dataclass
class Transaction:
    id: str
    amount: Money
    category: str
    description: str
    txn_date: date
    created_at: datetime = field(default_factory=datetime.utcnow)
    meta: Dict[str, Any] = field(default_factory=dict)

    @classmethod
    def create(cls, amount: Any, category: str, description: str, txn_date: Optional[date] = None, **meta):
        return cls(
            id=str(uuid.uuid4()),
            amount=_money(amount),
            category=category.strip() or "Uncategorized",
            description=description.strip(),
            txn_date=txn_date or date.today(),
            meta=meta or {}
        )


@dataclass
class BudgetCategory:
    name: str
    limit: Money
    spent: Money = Decimal("0.00")

    def remaining(self) -> Money:
        return _money(self.limit - self.spent)

    def usage_ratio(self) -> float:
        if self.limit == 0:
            return 0.0
        return float((self.spent / self.limit).quantize(Decimal("0.01")))


@dataclass
class Budget:
    id: str
    month: str  # YYYY-MM
    categories: Dict[str, BudgetCategory]
    created_at: datetime = field(default_factory=datetime.utcnow)

    @classmethod
    def create(cls, month: str, categories: Dict[str, Any]):
        cat_objs = {
            k: (v if isinstance(v, BudgetCategory) else BudgetCategory(name=k, limit=_money(v)))
            for k, v in categories.items()
        }
        return cls(id=str(uuid.uuid4()), month=month, categories=cat_objs)

    def apply_transaction(self, txn: Transaction):
        cat = self.categories.get(txn.category)
        if not cat:
            # auto-create with zero limit if not defined
            cat = BudgetCategory(name=txn.category, limit=Decimal("0.00"))
            self.categories[txn.category] = cat
        cat.spent = _money(cat.spent + txn.amount)

    def summary(self) -> List[Dict[str, Any]]:
        out = []
        for name, cat in sorted(self.categories.items()):
            out.append({
                "category": name,
                "limit": str(cat.limit),
                "spent": str(cat.spent),
                "remaining": str(cat.remaining()),
                "usage_ratio": round(cat.usage_ratio(), 2)
            })
        return out


@dataclass
class ReceiptLine:
    raw: str
    description: str
    amount: Money
    quantity: int = 1


@dataclass
class ReceiptParseResult:
    original_text: str
    lines: List[ReceiptLine]
    total_detected: Optional[Money] = None
    warnings: List[str] = field(default_factory=list)

    def to_transactions(self, default_category: str = "Uncategorized") -> List[Transaction]:
        txns = []
        for line in self.lines:
            txns.append(Transaction.create(
                amount=line.amount,
                category=default_category,
                description=line.description or line.raw
            ))
        return txns
