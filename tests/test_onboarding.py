from chat.orchestrator import ChatOrchestrator


def make_orch(tmp_path):
    return ChatOrchestrator(data_path=str(tmp_path / "state.json"))


def test_onboarding_banner_blank_input(tmp_path):
    orch = make_orch(tmp_path)
    resp = orch.handle("")
    assert "Welcome" in resp or "Finance Tracker" in resp


def test_onboarding_skip(tmp_path):
    orch = make_orch(tmp_path)
    resp = orch.handle("skip")
    assert "Onboarding skipped" in resp
    # subsequent command works
    resp2 = orch.handle("add 5.00 coffee test")
    assert "Added" in resp2


def test_onboarding_start_and_flow(tmp_path):
    orch = make_orch(tmp_path)
    # explicit start path
    r1 = orch.handle("start")
    assert "Enter how many" in r1
    r2 = orch.handle("3")
    assert "Now enter each category" in r2
    r3 = orch.handle("groceries 300")
    assert "Added groceries" in r3 or "Added Groceries" in r3
    r4 = orch.handle("rent 1200")
    assert "Added rent" in r4 or "Added Rent" in r4
    r5 = orch.handle("fun 100")
    assert "Type 'done'" in r5 or "Type 'done'" in r5
    r6 = orch.handle("done")
    assert "Setup complete" in r6
    # After completion, normal commands should work without onboarding interference
    r7 = orch.handle("add 10 groceries milk")
    assert "Added" in r7


def test_onboarding_invalid_count_then_valid(tmp_path):
    orch = make_orch(tmp_path)
    r1 = orch.handle("abc")
    assert "number 1-10" in r1
    r2 = orch.handle("2")
    assert "Now enter each category" in r2
    r3 = orch.handle("food 200")
    assert "Added" in r3
    r4 = orch.handle("transport 150")
    assert "Type 'done'" in r4
    r5 = orch.handle("done")
    assert "Setup complete" in r5


def test_command_bypasses_onboarding(tmp_path):
    orch = make_orch(tmp_path)
    # Issue a valid command first: should disable onboarding
    resp = orch.handle("add 5.00 coffee test")
    assert "Added" in resp
    # Blank input now should not re-trigger onboarding (since disabled)
    resp2 = orch.handle("")
    # Ensure the onboarding Welcome banner isn't shown again
    assert "Welcome" not in resp2
