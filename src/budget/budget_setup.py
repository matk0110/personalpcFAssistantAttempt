# Deprecated legacy module. Use services.budgets.BudgetService instead.
class BudgetSetup:  # kept for backward compatibility
    def __init__(self, *_, **__):
        raise RuntimeError("BudgetSetup is deprecated. Use BudgetService via ChatOrchestrator.")