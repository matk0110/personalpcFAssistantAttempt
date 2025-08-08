import os
import sys
from src.receipt.parser import ReceiptParser

def ingest_receipts(receipt_folder):
    if not os.path.exists(receipt_folder):
        print(f"Receipt folder '{receipt_folder}' does not exist.")
        return

    for filename in os.listdir(receipt_folder):
        if filename.endswith(('.png', '.jpg', '.jpeg')):
            file_path = os.path.join(receipt_folder, filename)
            print(f"Processing receipt: {file_path}")
            parser = ReceiptParser()
            spending_data = parser.parse_receipt(file_path)
            print(f"Extracted data: {spending_data}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python ingest_receipts.py <receipt_folder>")
        sys.exit(1)

    receipt_folder = sys.argv[1]
    ingest_receipts(receipt_folder)