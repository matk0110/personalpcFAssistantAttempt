import pytest

@pytest.mark.skip(reason="Legacy SpendingTracker deprecated; covered by transaction/budget service tests.")
def test_legacy_spending_tracker():
    assert True