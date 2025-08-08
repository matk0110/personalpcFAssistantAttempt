# Finance Tracker Chat MVP

A fast, local CLI chat agent for tracking personal spending and lightweight budgeting.

## Features (MVP)
- Add expenses with category + optional description + optional date (add 12.34 groceries milk and bread on 2025-08-07)
- Auto categorization via simple keyword resolver
- Show current month budget usage (implicit categories created as you add expenses)
- Paste raw receipt text (receipt: ... lines) to batch add line items
- Summaries (summary 7d / summary 30d)
- Mock LLM adapter (deterministic echo) placeholder for future model integration

## Quick Start
```bash
python -m venv .venv
. .venv/Scripts/Activate.ps1  # Windows PowerShell
pip install -r requirements.txt -r requirements.dev.txt
python -m src.main
```
Type `help` inside the app for commands.

## Commands
```
add 12.34 groceries milk and bread
add 10.00 coffee latte on 2025-08-07
budget
budget groceries
receipt:
  Milk 2.50
  Bread 1.20
summary 7d
help
```

## Demo Transcript
```
> add 5.00 coffee latte
Added 5.00 to Coffee. Remaining: 0.00.
> add 12.00 groceries milk
Added 12.00 to Groceries. Remaining: 0.00.
> budget
Budget
Coffee: 5.00/0.00 rem -5.00
Groceries: 12.00/0.00 rem -12.00
> summary 7d
Last 7d: 17.00 across 2 transactions.
> receipt:
Milk 2.50
Bread 1.20
Parsed 2 lines.
```
(Adjust after real run.)

## Testing
```bash
pytest -q
```

## Structure
```
src/
  core/ (models + persistence)
  services/ (transactions, budgets, receipts, categories)
  chat/ (intent parser, orchestrator)
  llm/ (mock adapter)
```

## Roadmap (Fast Follow)
- Budget limits configuration command
- Conversation memory pruning / summarization
- Real LLM provider adapter
- CSV export
- Basic anomaly heuristic

## License
MIT