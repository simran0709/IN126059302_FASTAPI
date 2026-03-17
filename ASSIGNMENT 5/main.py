from fastapi import FastAPI, Query

app = FastAPI()

# ------------------ DATA ------------------

products = [
    {"id": 1, "name": "Wireless Mouse", "price": 499, "category": "Electronics", "in_stock": True},
    {"id": 2, "name": "Notebook", "price": 99, "category": "Stationery", "in_stock": True},
    {"id": 3, "name": "USB Hub", "price": 799, "category": "Electronics", "in_stock": False},
    {"id": 4, "name": "Pen Set", "price": 49, "category": "Stationery", "in_stock": True},
    {"id": 5, "name": "Laptop Stand", "price": 1299, "category": "Electronics", "in_stock": True},
    {"id": 6, "name": "Sticky Notes", "price": 49, "category": "Stationery", "in_stock": True},
]

orders = [
    {"id": 1, "customer_name": "Simran", "total": 499},
    {"id": 2, "customer_name": "Rahul", "total": 799},
]

# ------------------ Q1 SEARCH ------------------

@app.get("/products/search")
def search_products(keyword: str = Query(...)):
    result = [p for p in products if keyword.lower() in p["name"].lower()]

    if not result:
        return {"message": "No products found"}

    return {
        "keyword": keyword,
        "total_found": len(result),
        "products": result
    }

# ------------------ Q2 SORT ------------------

@app.get("/products/sort")
def sort_products(sort_by: str = "price", order: str = "asc"):

    if sort_by not in ["price", "name"]:
        return {"error": "sort_by must be 'price' or 'name'"}

    sorted_products = sorted(
        products,
        key=lambda x: x[sort_by],
        reverse=(order == "desc")
    )

    return {
        "sort_by": sort_by,
        "order": order,
        "products": sorted_products
    }

# ------------------ Q3 PAGINATION ------------------

@app.get("/products/page")
def paginate_products(page: int = 1, limit: int = 2):

    start = (page - 1) * limit
    end = start + limit

    return {
        "page": page,
        "limit": limit,
        "total": len(products),
        "total_pages": (len(products) + limit - 1) // limit,
        "products": products[start:end]
    }

# ------------------ Q4 SEARCH ORDERS ------------------

@app.get("/orders/search")
def search_orders(customer_name: str = Query(...)):

    result = [
        o for o in orders
        if customer_name.lower() in o["customer_name"].lower()
    ]

    if not result:
        return {"message": "No orders found"}

    return {
        "customer_name": customer_name,
        "total_found": len(result),
        "orders": result
    }

# ------------------ Q5 SORT BY CATEGORY ------------------

@app.get("/products/sort-by-category")
def sort_by_category():

    result = sorted(products, key=lambda x: (x["category"], x["price"]))

    return {
        "products": result
    }

# ------------------ Q6 BROWSE ------------------

@app.get("/products/browse")
def browse_products(
    keyword: str = None,
    sort_by: str = "price",
    order: str = "asc",
    page: int = 1,
    limit: int = 2
):

    result = products

    # SEARCH
    if keyword:
        result = [p for p in result if keyword.lower() in p["name"].lower()]

    # SORT
    if sort_by not in ["price", "name"]:
        return {"error": "Invalid sort_by"}

    result = sorted(
        result,
        key=lambda x: x[sort_by],
        reverse=(order == "desc")
    )

    # PAGINATION
    start = (page - 1) * limit
    end = start + limit
    paginated = result[start:end]

    return {
        "keyword": keyword,
        "page": page,
        "total_found": len(result),
        "products": paginated
    }

# ------------------ BONUS ------------------

@app.get("/orders/page")
def orders_pagination(page: int = 1, limit: int = 2):

    start = (page - 1) * limit
    end = start + limit

    return {
        "page": page,
        "total_orders": len(orders),
        "orders": orders[start:end]
    }
