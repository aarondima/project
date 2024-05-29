import requests
import webbrowser

# CHANGE THE VARIABLE BELOW TO YOUR FLASK URL
FLASK_URL = "http://localhost:8888"


def http(method, path, data=None):
    print(f"Making {method} request to {FLASK_URL + path}...")
    if method not in ["GET", "POST", "PUT", "DELETE"]:
        raise RuntimeWarning("Invalid method")
    
    if method == "GET":
        response = requests.get(FLASK_URL + path)
    elif method == "POST":
        response = requests.post(FLASK_URL + path, json=data)
    elif method == "PUT":
        response = requests.put(FLASK_URL + path, json=data)
    elif method == "DELETE":
        response = requests.delete(FLASK_URL + path)
    
    print("Received status code:", response.status_code)
    return response

def get(path):
    return http("GET", path)


def post(path, data=None):
    return http("POST", path, data)


def put(path, data=None):
    return http("PUT", path, data)


def delete(path):
    return http("DELETE", path)


def demo():
    print("Adding a new product: 'salty nuts' (6.99)")
    post("/api/products/", {"name": "salty nuts", "price": 6.99, "available": 50})
    input("Check for salty nuts in the web page. Press Enter when ready.")
    # webbrowser.open(FLASK_URL + "/products")
    input("Press Enter to continue.")

    print("Adding a new product: 'ice cream' (4.99)")
    post("/api/products/", {"name": "ice cream", "price": 4.99, "available": 37})
    input("Check for ice cream in the web page. Press Enter when ready.")
    # webbrowser.open(FLASK_URL + "/products")
    input("Press Enter to continue.")

    print("Adding a new product: 'steak' (16.99)")
    post("/api/products/", {"name": "steak", "price": 16.99, "available": 7})
    input("Check for steak in the web page. Press Enter when ready.")
    webbrowser.open(FLASK_URL + "/products")
    input("Press Enter to continue.")

    print("Creating a new order: order_id: 101 items:[{name:steak, quantity: 4, name:ice cream, quantity: 30}]")
    post("/api/orders/", {"customer_id": "1", "items":[{"name":"steak", "quantity": 4, "name":"ice cream", "quantity": 30}]})
    input("Check for the new order in the web page. Press Enter when ready.")
    # webbrowser.open(FLASK_URL + "/orders")
    input("Press Enter to continue.")

    print("Creating a new order: order_id: 102 items:[{name:salty nuts, quantity: 60, name:ice cream, quantity: 30}]")
    post("/api/orders/", {"customer_id": "1", "items":[{"name":"salty nuts", "quantity": 60, "name":"ice cream", "quantity": 30}]})
    input("Check for the new order in the web page. Press Enter when ready.")
    # webbrowser.open(FLASK_URL + "/orders")
    input("Press Enter to continue.")

    print("Creating a new order: order_id: 103 items:[{name:steak, quantity: 10, name:ice cream, quantity: 30}]")
    post("/api/orders/", {"customer_id": "1", "items":[{"name":"steak", "quantity": 10, "name":"ice cream", "quantity": 30}]})
    input("Check for the new order in the web page. Press Enter when ready.")
    webbrowser.open(FLASK_URL + "/orders")
    input("Press Enter to continue.")

    # Ok order
    print("Processing an OK order: strategy: adjust")
    put("/api/orders/101", {"process":True})
    input("Check the order in the web page. Press Enter when ready.")
    webbrowser.open(FLASK_URL + "/orders/101")
    input("Press Enter to continue.")

    # NOK order 1
    print("Processing an NOK order: strategy: reject")
    put("/api/orders/102", {"process":True, "strategy": "reject"})
    input("Check the order in the web page. Press Enter when ready.")
    # webbrowser.open(FLASK_URL + "/orders/102")
    input("Press Enter to continue.")
    print("Processing a NOK order: strategy: ignore")
    put("/api/orders/102", {"process":True, "strategy": "ignore"})
    input("Check the order in the web page. Press Enter when ready.")
    webbrowser.open(FLASK_URL + "/orders/102")
    input("Press Enter to continue.")

    # NOK order 2
    print("Processing a NOK order: strategy: adjust")
    put("/api/orders/103", {"process":True})
    input("Check the order in the web page. Press Enter when ready.")
    webbrowser.open(FLASK_URL + "/orders/103")
    input("Press Enter to continue.")

    # Nonexisting product
    print("Creating a new order: NONEXISTING PRODUCT")
    post("/api/orders/", {"customer_id": "1", "items":[{"name":"dry aged steak", "quantity": 4}]})
    input("Check for the new order in the web page. Press Enter when ready.")
    webbrowser.open(FLASK_URL + "/orders")
    input("Press Enter to continue.")

    # Invalid quantity
    print("Creating a new order: INVALID VALUE")
    post("/api/orders/", {"customer_id": "1", "items":[{"name":"dry aged steak", "quantity": -3}]})
    input("Check for the new order in the web page. Press Enter when ready.")
    webbrowser.open(FLASK_URL + "/orders")
    input("Press Enter to continue.")

    # Invalid price
    print("Creating a new product: INVALID PRICE")
    post("/api/products/", {"name":"dry aged steak", "price": -400.00, "available": 20})
    input("Check for the new product in the web page. Press Enter when ready.")
    webbrowser.open(FLASK_URL + "/products")
    input("Press Enter to continue.")
if __name__ == "__main__":
    demo()
