import argparse
import json
import requests

DEFAULT_URL = "http://127.0.0.1:5000"


def print_json(data):
    print(json.dumps(data, indent=2))


def api_request(method, url, **kwargs):
    try:
        response = requests.request(method, url, timeout=10, **kwargs)
        try:
            data = response.json()
        except ValueError:
            data = {"message": response.text}
        print_json(data)
        return response
    except requests.RequestException as exc:
        print(f"API request failed: {exc}")
        return None


def main():
    parser = argparse.ArgumentParser(
        description="CLI client for the Flask Inventory Management System"
    )
    parser.add_argument("--url", default=DEFAULT_URL, help="Base API URL")

    sub = parser.add_subparsers(dest="command", required=True)

    sub.add_parser("list", help="List all inventory items")

    get_parser = sub.add_parser("get", help="Get one inventory item")
    get_parser.add_argument("id", type=int)

    add_parser = sub.add_parser("add", help="Add an inventory item")
    add_parser.add_argument("--name", required=True)
    add_parser.add_argument("--price", required=True, type=float)
    add_parser.add_argument("--stock", required=True, type=int)
    add_parser.add_argument("--barcode")
    add_parser.add_argument("--category", default="")
    add_parser.add_argument("--brand", default="")

    update_parser = sub.add_parser("update", help="Update an inventory item")
    update_parser.add_argument("id", type=int)
    update_parser.add_argument("--name")
    update_parser.add_argument("--price", type=float)
    update_parser.add_argument("--stock", type=int)

    delete_parser = sub.add_parser("delete", help="Delete an inventory item")
    delete_parser.add_argument("id", type=int)

    find_parser = sub.add_parser("find", help="Find a product in Open Food Facts")
    find_parser.add_argument("query")

    import_parser = sub.add_parser(
        "import-product",
        help="Find an Open Food Facts product and add it to inventory",
    )
    import_parser.add_argument("query")
    import_parser.add_argument("--price", required=True, type=float)
    import_parser.add_argument("--stock", required=True, type=int)

    args = parser.parse_args()
    base = args.url.rstrip("/")

    if args.command == "list":
        api_request("GET", f"{base}/inventory")

    elif args.command == "get":
        api_request("GET", f"{base}/inventory/{args.id}")

    elif args.command == "add":
        payload = {
            "name": args.name,
            "price": args.price,
            "stock": args.stock,
            "barcode": args.barcode,
            "category": args.category,
            "brand": args.brand,
        }
        api_request("POST", f"{base}/inventory", json=payload)

    elif args.command == "update":
        payload = {
            key: value
            for key, value in {
                "name": args.name,
                "price": args.price,
                "stock": args.stock,
            }.items()
            if value is not None
        }
        api_request("PATCH", f"{base}/inventory/{args.id}", json=payload)

    elif args.command == "delete":
        api_request("DELETE", f"{base}/inventory/{args.id}")

    elif args.command == "find":
        api_request("GET", f"{base}/api/lookup", params={"query": args.query})

    elif args.command == "import-product":
        payload = {
            "query": args.query,
            "price": args.price,
            "stock": args.stock,
        }
        api_request("POST", f"{base}/inventory/import", json=payload)


if __name__ == "__main__":
    main()
