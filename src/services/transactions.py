from __future__ import annotations
from datetime import date
from typing import List, Optional, Iterable
from decimal import Decimal

from core import Transaction, Persistence

class TransactionService:
    def __init__(self, store: Persistence):
        self.store = store

    def add(self, amount, category: str, description: str, txn_date: Optional[date] = None, **meta) -> Transaction:
        txn = Transaction.create(amount=amount, category=category, description=description, txn_date=txn_date, **meta)
        self.store.save_transaction(txn)
        return txn

    def list(self, *, category: Optional[str] = None) -> List[Transaction]:
        return self.store.list_transactions(category=category)

    def total_for(self, *, category: Optional[str] = None) -> Decimal:
        txns = self.list(category=category)
        total = sum(t.amount for t in txns)
        return total

    def recent(self, n: int = 10) -> List[Transaction]:
        txns = self.list()
        return txns[-n:]