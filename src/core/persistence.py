from __future__ import annotations
import json
from pathlib import Path
from threading import RLock
from typing import List, Dict, Optional, Callable
from datetime import date, datetime
from decimal import Decimal

from .models import Transaction, Budget, BudgetCategory, _money

class PersistenceError(Exception):
    pass

class Persistence:
    def save_transaction(self, txn: Transaction): raise NotImplementedError
    def list_transactions(self, *, category: Optional[str] = None) -> List[Transaction]: raise NotImplementedError
    def get_budget(self, month: str) -> Optional[Budget]: raise NotImplementedError
    def save_budget(self, budget: Budget): raise NotImplementedError

class JsonFilePersistence(Persistence):
    def __init__(self, path: Path):
        self.path = Path(path)
        self._lock = RLock()
        self._data = {"transactions": [], "budgets": {}}
        self._load()

    # ---------- Internal ----------
    def _load(self):
        if self.path.exists():
            try:
                with self.path.open("r", encoding="utf-8") as f:
                    raw = json.load(f)
                if isinstance(raw, dict):
                    self._data = raw
            except json.JSONDecodeError:  # corrupt file -> backup & reset
                backup = self.path.with_suffix(".corrupt")
                self.path.replace(backup)
        else:
            self._flush()

    def _flush(self):
        self.path.parent.mkdir(parents=True, exist_ok=True)
        tmp = self.path.with_suffix(".tmp")
        with tmp.open("w", encoding="utf-8") as f:
            json.dump(self._data, f, indent=2)
        tmp.replace(self.path)

    # ---------- Serialization Helpers ----------
    @staticmethod
    def _txn_to_dict(txn: Transaction) -> Dict:
        return {
            "id": txn.id,
            "amount": str(txn.amount),
            "category": txn.category,
            "description": txn.description,
            "txn_date": txn.txn_date.isoformat(),
            "created_at": txn.created_at.isoformat(),
            "meta": txn.meta
        }

    @staticmethod
    def _txn_from_dict(d: Dict) -> Transaction:
        return Transaction(
            id=d["id"],
            amount=_money(d["amount"]),
            category=d["category"],
            description=d["description"],
            txn_date=date.fromisoformat(d["txn_date"]),
            created_at=datetime.fromisoformat(d["created_at"]),
            meta=d.get("meta") or {}
        )

    @staticmethod
    def _budget_to_dict(b: Budget) -> Dict:
        return {
            "id": b.id,
            "month": b.month,
            "created_at": b.created_at.isoformat(),
            "categories": {
                name: {
                    "name": cat.name,
                    "limit": str(cat.limit),
                    "spent": str(cat.spent)
                } for name, cat in b.categories.items()
            }
        }

    @staticmethod
    def _budget_from_dict(d: Dict) -> Budget:
        cats = {
            name: BudgetCategory(
                name=v["name"],
                limit=_money(v["limit"]),
                spent=_money(v.get("spent", "0.00"))
            ) for name, v in d["categories"].items()
        }
        return Budget(
            id=d["id"],
            month=d["month"],
            created_at=datetime.fromisoformat(d["created_at"]),
            categories=cats
        )

    # ---------- Public API ----------
    def save_transaction(self, txn: Transaction):
        with self._lock:
            self._data["transactions"].append(self._txn_to_dict(txn))
            self._flush()

    def list_transactions(self, *, category: Optional[str] = None) -> List[Transaction]:
        with self._lock:
            txns = [self._txn_from_dict(t) for t in self._data["transactions"]]
        if category:
            txns = [t for t in txns if t.category.lower() == category.lower()]
        return sorted(txns, key=lambda t: (t.txn_date, t.created_at))

    def get_budget(self, month: str) -> Optional[Budget]:
        with self._lock:
            bdict = self._data["budgets"].get(month)
            if not bdict:
                return None
            return self._budget_from_dict(bdict)

    def save_budget(self, budget: Budget):
        with self._lock:
            self._data["budgets"][budget.month] = self._budget_to_dict(budget)
            self._flush()

    # Convenience
    def ensure_budget(self, month: str, factory: Callable[[], Budget]) -> Budget:
        b = self.get_budget(month)
        if b:
            return b
        b = factory()
        self.save_budget(b)
        return b