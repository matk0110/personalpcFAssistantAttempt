from chat.intent import IntentParser

def test_add_expense_intent():
    p = IntentParser()
    r = p.parse("add 12.34 groceries milk and bread")
    assert r and r.name == "add_expense"
    assert r.args["amount"] == "12.34"
    assert r.args["category"] == "groceries"


def test_budget_intent():
    p = IntentParser()
    r = p.parse("budget food")
    assert r and r.name == "show_budget"
    assert r.args["category"] == "food"


def test_receipt_intent():
    p = IntentParser()
    sample = "receipt:\nMilk 2.50\nBread 1.20"
    r = p.parse(sample)
    assert r and r.name == "receipt"
    assert "body" in r.args


def test_help_intent():
    p = IntentParser()
    r = p.parse("help")
    assert r and r.name == "help"


def test_add_expense_with_date():
    p = IntentParser()
    r = p.parse("add 10.00 coffee latte on 2025-08-07")
    assert r and r.args["date"] == "2025-08-07"
