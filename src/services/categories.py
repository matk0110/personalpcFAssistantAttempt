from __future__ import annotations
from typing import List, Tuple

class CategoryResolver:
    def __init__(self, rules: List[Tuple[str, str]] | None = None, default: str = "Other"):
        # rules: list of (keyword_lower, category)
        self.default = default
        self.rules = rules or [
            ("grocery", "Groceries"),
            ("supermarket", "Groceries"),
            ("fuel", "Transport"),
            ("gas", "Transport"),
            ("uber", "Transport"),
            ("rent", "Housing"),
            ("coffee", "Dining"),
            ("restaurant", "Dining"),
            ("pharmacy", "Health"),
        ]

    def resolve(self, text: str) -> str:
        low = text.lower()
        for kw, cat in self.rules:
            if kw in low:
                return cat
        return self.default