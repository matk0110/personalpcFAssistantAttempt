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
