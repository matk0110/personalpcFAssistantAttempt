import unittest
from src.spending.tracker import SpendingTracker

class TestSpendingTracker(unittest.TestCase):

    def setUp(self):
        self.tracker = SpendingTracker()
        self.tracker.set_budget({'Food': 100, 'Transport': 50})

    def test_track_expense(self):
        self.tracker.track_expense('Food', 20)
        self.assertEqual(self.tracker.get_expense('Food'), 20)

    def test_calculate_remaining_budget(self):
        self.tracker.track_expense('Food', 20)
        self.assertEqual(self.tracker.calculate_remaining_budget('Food'), 80)

    def test_overspending(self):
        self.tracker.track_expense('Transport', 60)
        self.assertGreater(self.tracker.get_expense('Transport'), self.tracker.budget['Transport'])

if __name__ == '__main__':
    unittest.main()