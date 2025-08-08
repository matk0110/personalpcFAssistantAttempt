# Usage Documentation for Free Spending Budget Agent

## Overview
The Free Spending Budget Agent is a personal finance application designed to help users manage their budgets, track spending, and analyze financial habits. This document provides a guide on how to use the application effectively.

## Getting Started
1. **Installation**: Ensure that you have Python 3 installed on your system. Clone the repository and install the required libraries using:
   ```
   pip install -r requirements.txt
   ```

2. **Setting Up the Environment**: It is recommended to set up a virtual environment to manage dependencies. You can create one using:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. **Running the Application**: To start the application, run the following command:
   ```
   python src/main.py
   ```

## Features
- **Budget Setup**: Users can define their budget categories and set amounts for each category.
- **Spending Tracker**: The application tracks expenses by category and calculates the remaining budget.
- **Receipt Parsing**: Users can upload images of receipts, and the application will extract and categorize spending using OCR technology.
- **Persistence**: The application saves the budget and spending data in JSON format, allowing users to resume their progress.

## Usage Instructions
### Setting Up Your Budget
1. Upon starting the application, you will be prompted to enter your budget categories and the corresponding amounts.
2. Follow the on-screen instructions to complete the setup.

### Tracking Expenses
1. Navigate to the spending tracker section of the application.
2. Enter your expenses as they occur. The application will automatically update your remaining budget.

### Uploading Receipts
1. Go to the receipt parsing section.
2. Upload an image of your receipt. The application will process the image and extract spending data.

### Saving and Loading Data
- The application automatically saves your budget and spending data. You can also manually save your progress at any time.

## Conclusion
The Free Spending Budget Agent is designed to be user-friendly and efficient. By following this guide, you can effectively manage your finances and gain insights into your spending habits. For further assistance, refer to the API documentation or contact support.