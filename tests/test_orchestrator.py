from chat.orchestrator import ChatOrchestrator


def test_add_and_show_budget(tmp_path, monkeypatch):
    orch = ChatOrchestrator(data_path=str(tmp_path / "state.json"))
    resp = orch.handle("add 5.00 groceries milk")
    assert "Added" in resp
    resp2 = orch.handle("budget groceries")
    assert "spent" in resp2


def test_summary(tmp_path):
    orch = ChatOrchestrator(data_path=str(tmp_path / "state.json"))
    orch.handle("add 2.00 coffee latte")
    resp = orch.handle("summary 7d")
    assert "Last" in resp


def test_receipt_flow(tmp_path):
    orch = ChatOrchestrator(data_path=str(tmp_path / "state.json"))
    receipt_text = "receipt:\nMilk 2.50\nBread 1.20"
    resp = orch.handle(receipt_text)
    assert "Parsed" in resp


def test_set_budget_and_add_flow(tmp_path):
    orch = ChatOrchestrator(data_path=str(tmp_path / "state.json"))
    r1 = orch.handle("set groceries 250")
    assert "limit" in r1
    r2 = orch.handle("add 50.00 groceries milk")
    assert "Remaining" in r2
    r3 = orch.handle("budget groceries")
    assert "250.00" in r3
    r4 = orch.handle("limits")
    assert "Groceries" in r4


def test_export_csv(tmp_path):
    orch = ChatOrchestrator(data_path=str(tmp_path / "state.json"))
    orch.handle("add 1.00 misc test")
    resp = orch.handle("export csv " + str(tmp_path / "out.csv"))
    assert "Exported" in resp


def test_negative_amount_validation(tmp_path):
    orch = ChatOrchestrator(data_path=str(tmp_path / "state.json"))
    resp = orch.handle("add -5 food test")
    assert "positive" in resp


def test_invalid_date_validation(tmp_path):
    orch = ChatOrchestrator(data_path=str(tmp_path / "state.json"))
    resp = orch.handle("add 5 food test on 2025-13-40")
    assert "Invalid date" in resp


def test_invalid_limit_validation(tmp_path):
    orch = ChatOrchestrator(data_path=str(tmp_path / "state.json"))
    resp = orch.handle("set travel -100")
    assert "non-negative" in resp
