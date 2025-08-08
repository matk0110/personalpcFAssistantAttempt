from __future__ import annotations
import re
from dataclasses import dataclass
from typing import Optional, Dict, Any

INTENTS = {
    # add 12.34 groceries optional description words on 2025-08-07
    "add_expense": re.compile(r"^(add|expense)\s+(?P<amount>\d+(?:\.\d{1,2})?)\s+(?P<category>\w+)(?:\s+(?P<desc>.*?))?(?:\s+on\s+(?P<date>\d{4}-\d{2}-\d{2}))?$", re.I),
    "show_budget": re.compile(r"^(budget)(?:\s+(?P<category>\w+))?$", re.I),
    "receipt": re.compile(r"^(receipt:)(?P<body>[\s\S]+)$", re.I),
    "summary": re.compile(r"^(summary)(?:\s+(?P<window>\d+d))?$", re.I),
    "help": re.compile(r"^(help|commands)$", re.I)
}

@dataclass
class ParsedIntent:
    name: str
    args: Dict[str, Any]

class IntentParser:
    def parse(self, text: str) -> Optional[ParsedIntent]:
        t = text.strip()
        for name, pattern in INTENTS.items():
            m = pattern.match(t)
            if m:
                groups = {k: v for k, v in m.groupdict().items() if v is not None}
                return ParsedIntent(name=name, args=groups)
        return None