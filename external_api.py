import requests

BASE_URL = "https://world.openfoodfacts.org"
HEADERS = {
    "User-Agent": "InventoryManagementSystem/1.0 (student-project)"
}
FIELDS = (
    "code,product_name,brands,ingredients_text,categories,"
    "image_front_url,nutriscore_grade"
)


def _normalise_product(product, fallback_barcode=None):
    if not product:
        return None

    return {
        "barcode": product.get("code") or fallback_barcode,
        "product_name": product.get("product_name", ""),
        "brands": product.get("brands", ""),
        "ingredients_text": product.get("ingredients_text", ""),
        "categories": product.get("categories", ""),
        "image_url": product.get("image_front_url", ""),
        "nutriscore_grade": product.get("nutriscore_grade", ""),
    }


def get_product_by_barcode(barcode):
    """Fetch one product by barcode using the current v3 product endpoint."""
    barcode = str(barcode).strip()
    url = f"{BASE_URL}/api/v3/product/{barcode}"
    response = requests.get(
        url,
        params={"fields": FIELDS},
        headers=HEADERS,
        timeout=10,
    )
    response.raise_for_status()
    data = response.json()

    if data.get("status") != 1:
        return None

    return _normalise_product(data.get("product"), barcode)


def search_product_by_name(name):
    """
    Search by product name.

    Open Food Facts v2 does not provide general full-text search in /api/v2/search,
    so this project uses the documented legacy full-text search endpoint for the
    name-search feature required by the lab.
    """
    response = requests.get(
        f"{BASE_URL}/cgi/search.pl",
        params={
            "search_terms": name,
            "search_simple": 1,
            "action": "process",
            "json": 1,
            "page_size": 5,
            "fields": FIELDS,
        },
        headers=HEADERS,
        timeout=10,
    )
    response.raise_for_status()
    data = response.json()

    products = data.get("products", [])
    if not products:
        return None

    return _normalise_product(products[0])


def find_product(query):
    """Treat numeric input as a barcode; otherwise search by product name."""
    query = str(query).strip()
    if not query:
        return None

    if query.isdigit():
        return get_product_by_barcode(query)

    return search_product_by_name(query)
