# Simulated in-memory database.
# The application deliberately uses an array/list because this is required
# by the summative lab.

inventory = [
    {
        "id": 1,
        "name": "Organic Almond Milk",
        "price": 4.99,
        "stock": 25,
        "barcode": "0000000000001",
        "category": "Plant-based drinks",
        "brand": "Silk",
        "ingredients_text": "Filtered water, almonds, cane sugar",
        "source": "mock database",
    },
    {
        "id": 2,
        "name": "Whole Wheat Bread",
        "price": 2.50,
        "stock": 40,
        "barcode": "0000000000002",
        "category": "Breads",
        "brand": "Example Bakery",
        "ingredients_text": "Whole wheat flour, water, yeast, salt",
        "source": "mock database",
    },
]


def next_id():
    return max((item["id"] for item in inventory), default=0) + 1
