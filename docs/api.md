# API Documentation for Free Spending Budget Agent

## Overview
This document provides an overview of the API endpoints and their functionalities for the Free Spending Budget Agent application.

## API Endpoints

### 1. Budget Setup
- **Endpoint:** `/api/budget/setup`
- **Method:** POST
- **Description:** Initializes the budget setup by prompting the user for categories and amounts.
- **Request Body:**
  ```json
  {
    "categories": [
      {
        "name": "Food",
        "amount": 300
      },
      {
        "name": "Transport",
        "amount": 150
      }
    ]
  }
  ```
- **Response:**
  - **200 OK:** Budget successfully set up.
  - **400 Bad Request:** Invalid input data.

### 2. Track Spending
- **Endpoint:** `/api/spending/track`
- **Method:** POST
- **Description:** Tracks an expense by category.
- **Request Body:**
  ```json
  {
    "category": "Food",
    "amount": 50,
    "description": "Grocery shopping"
  }
  ```
- **Response:**
  - **200 OK:** Expense tracked successfully.
  - **404 Not Found:** Category not found.

### 3. Get Remaining Budget
- **Endpoint:** `/api/budget/remaining`
- **Method:** GET
- **Description:** Retrieves the remaining budget for each category.
- **Response:**
  - **200 OK:** Returns remaining budget data.
  ```json
  {
    "remaining": [
      {
        "category": "Food",
        "remaining_amount": 250
      },
      {
        "category": "Transport",
        "remaining_amount": 150
      }
    ]
  }
  ```

### 4. Receipt Processing
- **Endpoint:** `/api/receipt/process`
- **Method:** POST
- **Description:** Processes a receipt image to extract spending data.
- **Request Body:**
  ```json
  {
    "image": "base64_encoded_image_string"
  }
  ```
- **Response:**
  - **200 OK:** Receipt processed successfully.
  - **500 Internal Server Error:** Error during processing.

## Error Handling
All endpoints will return appropriate HTTP status codes and error messages for invalid requests or server errors.

## Conclusion
This API documentation outlines the key functionalities of the Free Spending Budget Agent application. For further details, please refer to the source code and additional documentation.