from flask import Flask, jsonify, request, render_template
from external_api import find_product
from models import inventory, next_id

app = Flask(__name__)


def find_inventory_item(item_id):
    return next((item for item in inventory if item["id"] == item_id), None)


@app.get("/")
def home():
    return render_template("index.html", inventory=inventory)


@app.get("/inventory")
def get_inventory():
    return jsonify({"count": len(inventory), "inventory": inventory}), 200


@app.get("/inventory/<int:item_id>")
def get_item(item_id):
    item = find_inventory_item(item_id)
    if item is None:
        return jsonify({"error": "Inventory item not found"}), 404
    return jsonify(item), 200


@app.post("/inventory")
def create_item():
    data = request.get_json(silent=True)
    if not isinstance(data, dict):
        return jsonify({"error": "Request body must be valid JSON"}), 400

    required = ["name", "price", "stock"]
    missing = [field for field in required if field not in data]
    if missing:
        return jsonify({"error": f"Missing required fields: {', '.join(missing)}"}), 400

    try:
        price = float(data["price"])
        stock = int(data["stock"])
    except (TypeError, ValueError):
        return jsonify({"error": "price must be a number and stock must be an integer"}), 400

    if price < 0 or stock < 0:
        return jsonify({"error": "price and stock cannot be negative"}), 400

    item = {
        "id": next_id(),
        "name": str(data["name"]).strip(),
        "price": price,
        "stock": stock,
        "barcode": data.get("barcode"),
        "category": data.get("category", ""),
        "brand": data.get("brand", ""),
        "ingredients_text": data.get("ingredients_text", ""),
        "source": data.get("source", "manual"),
    }

    if not item["name"]:
        return jsonify({"error": "name cannot be empty"}), 400

    inventory.append(item)
    return jsonify(item), 201


@app.patch("/inventory/<int:item_id>")
def update_item(item_id):
    item = find_inventory_item(item_id)
    if item is None:
        return jsonify({"error": "Inventory item not found"}), 404

    data = request.get_json(silent=True)
    if not isinstance(data, dict):
        return jsonify({"error": "Request body must be valid JSON"}), 400

    allowed = {"name", "price", "stock", "barcode", "category",
               "brand", "ingredients_text"}

    unknown = set(data) - allowed
    if unknown:
        return jsonify({"error": f"Unsupported fields: {', '.join(sorted(unknown))}"}), 400

    if "price" in data:
        try:
            value = float(data["price"])
        except (TypeError, ValueError):
            return jsonify({"error": "price must be a number"}), 400
        if value < 0:
            return jsonify({"error": "price cannot be negative"}), 400
        item["price"] = value

    if "stock" in data:
        try:
            value = int(data["stock"])
        except (TypeError, ValueError):
            return jsonify({"error": "stock must be an integer"}), 400
        if value < 0:
            return jsonify({"error": "stock cannot be negative"}), 400
        item["stock"] = value

    for field in ["name", "barcode", "category", "brand", "ingredients_text"]:
        if field in data:
            if field == "name" and not str(data[field]).strip():
                return jsonify({"error": "name cannot be empty"}), 400
            item[field] = data[field]

    return jsonify(item), 200


@app.delete("/inventory/<int:item_id>")
def delete_item(item_id):
    item = find_inventory_item(item_id)
    if item is None:
        return jsonify({"error": "Inventory item not found"}), 404

    inventory.remove(item)
    return jsonify({"message": "Inventory item deleted", "item": item}), 200


@app.get("/api/lookup")
def lookup_external_product():
    query = request.args.get("query", "").strip()
    if not query:
        return jsonify({"error": "Provide a barcode or product name in ?query="}), 400

    try:
        result = find_product(query)
    except Exception as exc:
        return jsonify({"error": "External API request failed", "details": str(exc)}), 502

    if result is None:
        return jsonify({"message": "Product not found"}), 404

    return jsonify(result), 200


@app.post("/inventory/import")
def import_external_product():
    data = request.get_json(silent=True)
    if not isinstance(data, dict) or not str(data.get("query", "")).strip():
        return jsonify({"error": "Send JSON with a barcode or product name as 'query'"}), 400

    try:
        product = find_product(str(data["query"]).strip())
    except Exception as exc:
        return jsonify({"error": "External API request failed", "details": str(exc)}), 502

    if product is None:
        return jsonify({"error": "Product not found in Open Food Facts"}), 404

    try:
        price = float(data.get("price", 0))
        stock = int(data.get("stock", 0))
    except (TypeError, ValueError):
        return jsonify({"error": "price must be a number and stock must be an integer"}), 400

    if price < 0 or stock < 0:
        return jsonify({"error": "price and stock cannot be negative"}), 400

    item = {
        "id": next_id(),
        "name": product.get("product_name") or "Unknown product",
        "price": price,
        "stock": stock,
        "barcode": product.get("barcode"),
        "category": product.get("categories", ""),
        "brand": product.get("brands", ""),
        "ingredients_text": product.get("ingredients_text", ""),
        "image_url": product.get("image_url", ""),
        "nutriscore_grade": product.get("nutriscore_grade", ""),
        "source": "Open Food Facts",
    }

    inventory.append(item)
    return jsonify(item), 201


@app.errorhandler(404)
def not_found(_error):
    if request.path.startswith("/inventory") or request.path.startswith("/api/"):
        return jsonify({"error": "Route or resource not found"}), 404
    return "Page not found", 404


if __name__ == "__main__":
    app.run(debug=True)
