# Deprecated legacy module. Use services.receipts.SimpleReceiptParser.
class ReceiptParser:  # kept for backward compatibility
    def __init__(self, *_, **__):
        raise RuntimeError("ReceiptParser is deprecated. Use SimpleReceiptParser.")