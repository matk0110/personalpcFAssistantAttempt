import pytest

@pytest.mark.skip(reason="Legacy integration test deprecated; new orchestrator tests exist.")
def test_legacy_integration():
    assert True