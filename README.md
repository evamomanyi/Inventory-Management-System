# Python REST API - Inventory Management System

A Flask-based inventory management system created for the Moringa School Summative Lab.

The project demonstrates:

- RESTful CRUD endpoints with Flask
- An in-memory Python list as simulated database storage
- Open Food Facts external API integration
- A command-line client
- A small browser-based administrator interface
- Unit/integration tests with pytest
- `unittest.mock` for external API tests

## Project Structure

```text
inventory_management_system/
├── app.py
├── models.py
├── external_api.py
├── cli.py
├── requirements.txt
├── README.md
├── .gitignore
├── templates/
│   └── index.html
└── tests/
    ├── conftest.py
    ├── test_api.py
    ├── test_external_api.py
    ├── test_import.py
    └── test_cli.py
```

## 1. Installation

Create and enter the project directory:

```bash
cd inventory_management_system
```

Create a virtual environment:

```bash
python -m venv .venv
```

Activate it on Linux/macOS:

```bash
source .venv/bin/activate
```

On Windows:

```powershell
.venv\Scripts\activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

## 2. Run the Flask API

```bash
python app.py
```

The application runs at:

```text
http://127.0.0.1:5000
```

Open the address in a browser to use the administrator interface.

## 3. REST API Endpoints

| Method | Endpoint | Purpose |
|---|---|---|
| GET | `/inventory` | Get all inventory |
| GET | `/inventory/<id>` | Get one item |
| POST | `/inventory` | Create an item |
| PATCH | `/inventory/<id>` | Update an item |
| DELETE | `/inventory/<id>` | Delete an item |
| GET | `/api/lookup?query=...` | Find a product externally |
| POST | `/inventory/import` | Find an Open Food Facts product and add it to inventory |

### Get all inventory

```bash
curl http://127.0.0.1:5000/inventory
```

### Get one item

```bash
curl http://127.0.0.1:5000/inventory/1
```

### Create an item

```bash
curl -X POST http://127.0.0.1:5000/inventory \
  -H "Content-Type: application/json" \
  -d '{"name":"Orange Juice","price":3.50,"stock":20,"barcode":"1234567890123"}'
```

### Update an item

```bash
curl -X PATCH http://127.0.0.1:5000/inventory/1 \
  -H "Content-Type: application/json" \
  -d '{"price":5.25,"stock":15}'
```

### Delete an item

```bash
curl -X DELETE http://127.0.0.1:5000/inventory/1
```

## 4. Open Food Facts Integration

The application accepts either:

- a numeric barcode, or
- a product name.

Example:

```bash
curl "http://127.0.0.1:5000/api/lookup?query=3017620422003"
```

Or:

```bash
curl "http://127.0.0.1:5000/api/lookup?query=Nutella"
```

To import a product into the simulated inventory:

```bash
curl -X POST http://127.0.0.1:5000/inventory/import \
  -H "Content-Type: application/json" \
  -d '{"query":"3017620422003","price":8.50,"stock":15}'
```

The imported record contains inventory information plus data returned by Open Food Facts.

The application sends a custom `User-Agent` when calling Open Food Facts.

## 5. CLI Application

The Flask server must be running before using the CLI.

List inventory:

```bash
python cli.py list
```

Get an item:

```bash
python cli.py get 1
```

Add an item:

```bash
python cli.py add --name "Orange Juice" --price 3.50 --stock 20
```

Update an item:

```bash
python cli.py update 1 --price 5.25 --stock 10
```

Delete an item:

```bash
python cli.py delete 1
```

Find a product:

```bash
python cli.py find "Nutella"
```

Find by barcode:

```bash
python cli.py find 3017620422003
```

Import an external product:

```bash
python cli.py import-product 3017620422003 --price 8.50 --stock 15
```

If Flask is running on another address, use:

```bash
python cli.py --url http://localhost:5000 list
```

## 6. Testing

Run the complete test suite:

```bash
pytest -q
```

The tests cover:

- GET all inventory
- GET a single item
- POST/create
- PATCH/update
- DELETE
- validation errors
- Open Food Facts success/failure responses
- external product import
- CLI commands
- mocked network calls

The external API tests use `unittest.mock`, so they do not depend on the real Open Food Facts service.

## 7. Design Decisions

### Simulated database

The assignment specifically asks for temporary storage using an array. Therefore `models.py` uses a Python list called `inventory`.

This is intentionally not a production database.

### REST design

The main CRUD resource is `/inventory`.

- `GET` reads data
- `POST` creates data
- `PATCH` partially updates data
- `DELETE` removes data

### Error handling

The API returns appropriate HTTP status codes:

- `200` successful reads/updates/deletes
- `201` successful creation
- `400` invalid request
- `404` item/product not found
- `502` external API failure

## 8. Open Food Facts References

Official API documentation:

- https://openfoodfacts.github.io/documentation/docs/Product-Opener/api/
- https://openfoodfacts.github.io/documentation/docs/Product-Opener/v3/products/get-api-v3-product-code/
- https://openfoodfacts.github.io/documentation/docs/Product-Opener/v2/search/get-search/

Note: Open Food Facts currently documents API v3 as the current API, while API v2 is deprecated. The project uses the v3 product endpoint for barcode lookup. Name searching uses the documented legacy full-text search endpoint because the v2 structured search endpoint does not support general full-text `search_term` queries.
