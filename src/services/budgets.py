from __future__ import annotations
from datetime import date
from typing import Dict, Any, List
from decimal import Decimal

from core import Budget, BudgetCategory, Transaction, Persistence, _money

class BudgetService:
    def __init__(self, store: Persistence):
        self.store = store

    def month_key(self, dt: date) -> str:
        return dt.strftime("%Y-%m")

    def get_or_create(self, month: str, categories: Dict[str, Any] | None = None) -> Budget:
        existing = self.store.get_budget(month)
        if existing:
            return existing
        categories = categories or {}
        b = Budget.create(month, categories)
        self.store.save_budget(b)
        return b

    def apply(self, txn: Transaction):
        month = self.month_key(txn.txn_date)
        b = self.store.get_budget(month)
        if not b:
            b = Budget.create(month, {txn.category: Decimal("0.00")})
        b.apply_transaction(txn)
        self.store.save_budget(b)

    def summary(self, month: str) -> List[dict]:
        b = self.store.get_budget(month)
        if not b:
            return []
        return b.summary()

    def set_limits(self, month: str, updates: Dict[str, Any]):
        b = self.get_or_create(month)
        for name, limit in updates.items():
            cat = b.categories.get(name)
            if not cat:
                cat = BudgetCategory(name=name, limit=_money(limit))
                b.categories[name] = cat
            else:
                cat.limit = _money(limit)
        self.store.save_budget(b)
        return b