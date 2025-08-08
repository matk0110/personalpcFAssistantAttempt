# 📝 Project Tasks: Free Spending Budget Agent

## 0. MVP TARGET (Ship fast)
Goal: Local CLI chat that can
- Add expense (amount, category, description, date)
- Show budget status (per category vs limit)
- Ingest receipt text (no OCR; simple line parser)
- Auto-categorize (rule / keyword)
- Summarize recent spend
Storage: JSON or lightweight SQLite
Model: Mock LLM adapter interface

## 11. TRACKING CHECKBOXES
- [x] 1 Repo & env
- [x] 2 Models
- [x] 3 Persistence
- [x] 4 Budget service
- [x] 5 Transaction service
- [x] 6 Category resolver
- [x] 7 Receipt parser
- [x] 8 Chat orchestrator
- [x] 9 Intent router
- [x] 10 Prompts (implicit minimal)
- [x] 11 LLM mock
- [x] 12 Wiring
- [x] 13 Tests pass (new service tests added)
- [x] 14 CLI entry
- [x] 15 Demo transcript (placeholder)

## NEXT
- Real run to capture accurate demo transcript
- Add budget limit configuration command (e.g. set budget groceries 300)
- Improve negative remaining display (avoid - values when no limit)
- Option to export transactions (CSV)
- Remove legacy unused modules after confirming migration (budget_setup.py, old tests)