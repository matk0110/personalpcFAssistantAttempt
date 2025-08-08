# Deprecated legacy module. Use services.transactions.TransactionService and services.budgets.BudgetService.
class SpendingTracker:  # kept for backward compatibility
    def __init__(self, *_, **__):
        raise RuntimeError("SpendingTracker is deprecated. Use TransactionService/BudgetService.")