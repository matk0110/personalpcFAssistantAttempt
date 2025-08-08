from services.receipts import SimpleReceiptParser
from services.categories import CategoryResolver

def test_simple_receipt_parser_basic():
    parser = SimpleReceiptParser(CategoryResolver())
    text = "Milk 2.50\nBread 1.20\nTotal 3.70"
    result = parser.parse(text)
    assert len(result.lines) == 2
    assert str(result.total_detected) == "3.70"


def test_simple_receipt_to_transactions():
    parser = SimpleReceiptParser(CategoryResolver())
    text = "Coffee 3.00"  # should map coffee -> Dining
    result = parser.parse(text)
    txns = parser.to_transactions(result)
    assert txns[0].category in {"Dining", "Other"}
