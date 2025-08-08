from core import JsonFilePersistence
from services.transactions import TransactionService
from services.budgets import BudgetService
from pathlib import Path
from decimal import Decimal
from datetime import date

def test_budget_apply_and_summary(tmp_path):
    store = JsonFilePersistence(tmp_path / "state.json")
    txsvc = TransactionService(store)
    buds = BudgetService(store)
    buds.set_limits(date.today().strftime("%Y-%m"), {"Groceries": 100})
    t = txsvc.add(25, "Groceries", "Veggies")
    buds.apply(t)
    summary = buds.summary(date.today().strftime("%Y-%m"))
    g = next(s for s in summary if s["category"] == "Groceries")
    assert g["spent"] == "25.00"

def test_budget_auto_category_creation(tmp_path):
    store = JsonFilePersistence(tmp_path / "state.json")
    txsvc = TransactionService(store)
    buds = BudgetService(store)
    t = txsvc.add(10, "Snacks", "Chips")
    buds.apply(t)
    month = buds.month_key(t.txn_date)
    summary = buds.summary(month)
    s = next(s for s in summary if s["category"] == "Snacks")
    assert s["spent"] == "10.00"
