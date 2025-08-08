class SpendingTracker:
    def __init__(self):
        self.expenses = {}
        self.budget = {}

    def set_budget(self, category, amount):
        self.budget[category] = amount
        self.expenses[category] = 0

    def track_expense(self, category, amount):
        if category in self.budget:
            self.expenses[category] += amount
        else:
            raise ValueError("Category not found in budget.")

    def calculate_remaining_budget(self, category):
        if category in self.budget:
            return self.budget[category] - self.expenses[category]
        else:
            raise ValueError("Category not found in budget.")