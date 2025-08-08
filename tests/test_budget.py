import unittest
from src.budget.budget_setup import BudgetSetup
import pytest

class TestBudgetSetup(unittest.TestCase):

    def setUp(self):
        self.budget_setup = BudgetSetup()

    def test_prompt_for_categories(self):
        # Simulate user input for categories
        categories = self.budget_setup.prompt_for_categories()
        self.assertIsInstance(categories, list)
        self.assertGreater(len(categories), 0)

    def test_store_budget_data(self):
        # Test storing budget data
        test_data = {'Food': 200, 'Transport': 100}
        self.budget_setup.store_budget_data(test_data)
        self.assertEqual(self.budget_setup.budget_data, test_data)

@pytest.mark.skip(reason="Legacy BudgetSetup deprecated; see services tests.")
def test_legacy_budget_setup():
    assert True

if __name__ == '__main__':
    unittest.main()