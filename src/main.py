# Financial Advisor Application

from __future__ import annotations

import sys
from pathlib import Path

# Ensure 'chat', 'core', etc. (inside src) are importable as top-level when running module
CURRENT_DIR = Path(__file__).resolve().parent
if str(CURRENT_DIR) not in sys.path:
    sys.path.insert(0, str(CURRENT_DIR))

from chat.orchestrator import ChatOrchestrator  # core orchestrator

def main():
    banner = (
        "Finance Tracker Chat (MVP)\n"
        "--------------------------------------------------\n"
        "Goal: Help you set a simple monthly budget and track spending.\n\n"
        "Quick Start (first time):\n"
        "  1. Decide 3–6 categories (groceries, rent, transport, dining, fun).\n"
        "  2. Set a limit:   set <category> <monthly_limit>  (set groceries 400)\n"
        "  3. Add spending:  add <amount> <category> <desc>  (add 12.50 groceries milk)\n"
        "  4. Status:        budget   |  budget groceries\n"
        "  5. List limits:   limits\n"
        "  6. Receipt paste: receipt: <lines> (Milk 2.50)\n"
        "  7. Summary:       summary 7d   (or 30d)\n"
    "  8. Export CSV:    export csv data/txns.csv\n"
    "  9. Reset All:     reset  (clears ALL data, creates backup)\n\n"
        "Tips:\n"
        "  - You can add expenses before setting a limit (category has no limit).\n"
        "  - Set a limit later with 'set'.\n"
        "  - Keep category names one word (or use hyphens).\n"
        "  - Type 'help' anytime.\n\n"
        "Press ENTER (blank) for a guided setup wizard, or start typing commands.\n"
        "Ctrl+C or 'quit' to exit.\n"
        "--------------------------------------------------"
    )
    print(banner)
    orch = ChatOrchestrator()
    while True:
        try:
            user = input("> ").strip()
            if not user:
                # Attempt onboarding banner from orchestrator (empty string triggers onboarding path)
                onboarding = orch.handle("")
                if onboarding and onboarding != "Could not understand. Type 'help'.":
                    print(onboarding)
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