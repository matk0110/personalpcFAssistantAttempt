class ReceiptParser:
    def __init__(self, ocr_engine):
        self.ocr_engine = ocr_engine

    def parse_receipt(self, image_path):
        text = self.ocr_engine.extract_text(image_path)
        return self.extract_spending_data(text)

    def extract_spending_data(self, text):
        # Logic to extract spending data from the OCR text
        spending_data = {}
        # Example parsing logic (to be implemented)
        lines = text.split('\n')
        for line in lines:
            # Parse each line for relevant spending information
            pass
        return spending_data