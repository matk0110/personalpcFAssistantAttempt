import unittest
from src.budget.budget_setup import BudgetSetup
from src.spending.tracker import SpendingTracker
from src.receipt.parser import ReceiptParser
from src.persistence.storage import PersistenceManager

class TestIntegration(unittest.TestCase):

    def setUp(self):
        self.budget_setup = BudgetSetup()
        self.spending_tracker = SpendingTracker()
        self.receipt_parser = ReceiptParser()
        self.persistence_manager = PersistenceManager()

    def test_full_workflow(self):
        # Step 1: Set up budget
        self.budget_setup.prompt_user_for_budget()
        budget_data = self.budget_setup.get_budget_data()

        # Step 2: Track spending
        self.spending_tracker.track_expense("Food", 20)
        self.spending_tracker.track_expense("Transport", 15)
        remaining_budget = self.spending_tracker.calculate_remaining_budget(budget_data)

        # Step 3: Parse a receipt
        receipt_data = self.receipt_parser.parse_receipt("path/to/sample_receipt.jpg")
        self.spending_tracker.track_expense(receipt_data['category'], receipt_data['amount'])

        # Step 4: Save state
        self.persistence_manager.save_state(budget_data, self.spending_tracker.get_expenses())

        # Step 5: Load state and verify
        loaded_budget, loaded_expenses = self.persistence_manager.load_state()
        self.assertEqual(loaded_budget, budget_data)
        self.assertEqual(loaded_expenses, self.spending_tracker.get_expenses())

if __name__ == '__main__':
    unittest.main()