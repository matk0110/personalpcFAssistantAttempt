def get_categories():
    """Return a list of predefined budget categories."""
    return [
        "Housing",
        "Utilities",
        "Groceries",
        "Transportation",
        "Healthcare",
        "Entertainment",
        "Savings",
        "Miscellaneous"
    ]

def validate_category(category):
    """Check if the provided category is valid."""
    valid_categories = get_categories()
    return category in valid_categories

def add_category(new_category):
    """Add a new category to the list of budget categories."""
    if not validate_category(new_category):
        # In a real application, you might want to store this in a database or a file
        return f"{new_category} has been added to the categories."
    return f"{new_category} is already a valid category."