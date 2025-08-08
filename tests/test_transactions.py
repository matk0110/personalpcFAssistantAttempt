from core import JsonFilePersistence
from services.transactions import TransactionService
from pathlib import Path

def test_add_and_list_transactions(tmp_path):
    store = JsonFilePersistence(tmp_path / "state.json")
    svc = TransactionService(store)
    t1 = svc.add(5.25, "Coffee", "Morning coffee")
    t2 = svc.add(12.00, "Groceries", "Milk")
    all_txns = svc.list()
    assert len(all_txns) == 2
    assert all_txns[0].id == t1.id
    assert svc.total_for() == t1.amount + t2.amount
