# Deprecated OCR placeholder. Future OCR integration will live in a new module.

def perform_ocr(*_, **__):
    raise RuntimeError("perform_ocr deprecated. OCR not part of MVP.")


def extract_receipt_data(*_, **__):
    raise RuntimeError("extract_receipt_data deprecated. Use SimpleReceiptParser for text parsing.")