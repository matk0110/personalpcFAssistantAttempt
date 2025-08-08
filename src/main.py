# Financial Advisor Application

from __future__ import annotations

from budget.budget_setup import BudgetSetup
from spending.tracker import SpendingTracker
from receipt.parser import ReceiptParser
from persistence.storage import PersistenceManager
from chat.orchestrator import ChatOrchestrator

def main():
    print("Finance Tracker Chat (MVP). Type 'help' for commands. Ctrl+C to exit.")
    orch = ChatOrchestrator()
    while True:
        try:
            user = input("> ").strip()
            if not user:
                continue
            if user.lower() in {"exit", "quit"}:
                print("Bye.")
                break
            resp = orch.handle(user)
            print(resp)
        except KeyboardInterrupt:
            print("\nBye.")
            break
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    main()