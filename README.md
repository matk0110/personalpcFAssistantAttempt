# Finance Tracker Chat MVP

A fast, local CLI chat agent for tracking personal spending and lightweight budgeting.

## Features (MVP)
- Add expenses with category + optional description + optional date (add 12.34 groceries milk and bread on 2025-08-07)
- Set / update budget limits per category (set groceries 300)
- List configured limits (limits)
- Auto categorization via simple keyword resolver
- Show current month budget usage (implicit categories created as you add expenses; zero-limit categories display as spent X (no limit))
- Paste raw receipt text (receipt: ... lines) to batch add line items
- Summaries (summary 7d / summary 30d)
- Export transactions to CSV (export csv [path])
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
set groceries 300
limits
add 12.34 groceries milk and bread
add 10.00 coffee latte on 2025-08-07
budget
budget groceries
receipt:
  Milk 2.50
  Bread 1.20
summary 7d
export csv data/txns.csv
help
```

## Demo Transcript
```
> set groceries 300
Set Groceries limit to 300.00.
> add 12.00 groceries milk
Added 12.00 to Groceries. Remaining: 288.00.
> budget groceries
Groceries: spent 12.00 / 300.00 (remaining 288.00)
> add 5.00 coffee latte
Added 5.00 to Coffee. Remaining: spent 5.00 (no limit).
> budget
Budget
Coffee: spent 5.00 (no limit)
Groceries: 12.00/300.00 rem 288.00
> receipt:
Milk 2.50
Bread 1.20
Parsed 2 lines.
> summary 7d
Last 7d: 19.70 across 4 transactions.
> export csv export/transactions.csv
Exported 4 transactions to export/transactions.csv.
```
(Example transcript; update with real session as data grows.)

## Testing
```bash
pytest -q
```

## Optional OCR (Portable / Local Install)
If you want to use OCR features (receipt image to text) without installing Tesseract system-wide:

1. Create folder `tools/tesseract/` at repo root.
2. Download a Windows Tesseract build (e.g. UB Mannheim) and copy `tesseract.exe` into that folder.
3. (Optional) Put language data (`.traineddata` files) inside `tools/tesseract/tessdata/`.
4. Install Python deps if not already:
  ```bash
  pip install Pillow pytesseract
  ```
5. Use the OCR helpers:
  ```python
  from src.receipt.ocr import extract_lines
  lines = extract_lines("receipt.jpg")
  ```

If a system-wide install is preferred, just ensure `tesseract` is on PATH. The module auto-detects a portable binary at `tools/tesseract/tesseract.exe` if present.

## Structure
```
src/
  core/ (models + persistence)
  services/ (transactions, budgets, receipts, categories)
  chat/ (intent parser, orchestrator)
  llm/ (mock adapter)
```

## Roadmap (Fast Follow)
- Conversation memory pruning / summarization
- Real LLM provider adapter
- CSV export enhancements (filters, budgets)
- Basic anomaly heuristic
- Error case tests (invalid date / negative values) – partial

## License
MIT