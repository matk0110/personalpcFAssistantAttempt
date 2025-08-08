import unittest
from src.receipt.parser import ReceiptParser

class TestReceiptParser(unittest.TestCase):

    def setUp(self):
        self.parser = ReceiptParser()

    def test_extract_spending_data(self):
        # Example test case for extracting spending data
        test_image_path = 'path/to/test/image.jpg'
        expected_data = {
            'category': 'Groceries',
            'amount': 50.00
        }
        result = self.parser.extract_spending_data(test_image_path)
        self.assertEqual(result, expected_data)

    def test_handle_empty_image(self):
        # Test case for handling an empty image
        empty_image_path = 'path/to/empty/image.jpg'
        result = self.parser.extract_spending_data(empty_image_path)
        self.assertIsNone(result)

    def test_invalid_image_format(self):
        # Test case for handling an invalid image format
        invalid_image_path = 'path/to/invalid/image.txt'
        with self.assertRaises(ValueError):
            self.parser.extract_spending_data(invalid_image_path)

if __name__ == '__main__':
    unittest.main()