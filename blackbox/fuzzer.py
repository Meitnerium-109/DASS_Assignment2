import requests

BASE_URL = "http://localhost:8080/api/v1"
headers = {"X-Roll-Number": "12345", "X-User-ID": "1"}
bugs = []

def check(condition, desc):
    if not condition:
        bugs.append(desc)

def probe():
    # 1. Headers
    r = requests.get(f"{BASE_URL}/profile", headers={"X-User-ID": "1"})
    check(r.status_code == 401, f"Headers: Missing X-Roll-Number returned {r.status_code} instead of 401: {r.text}")
    r = requests.get(f"{BASE_URL}/profile", headers={"X-Roll-Number": "abc", "X-User-ID": "1"})
    check(r.status_code == 400, f"Headers: Invalid X-Roll-Number returned {r.status_code} instead of 400: {r.text}")
    r = requests.get(f"{BASE_URL}/profile", headers={"X-Roll-Number": "12345"})
    check(r.status_code == 400, f"Headers: Missing X-User-ID returned {r.status_code} instead of 400: {r.text}")
    r = requests.get(f"{BASE_URL}/profile", headers={"X-Roll-Number": "12345", "X-User-ID": "-1"})
    check(r.status_code == 400, f"Headers: Invalid X-User-ID (-1) returned {r.status_code} instead of 400: {r.text}")

    # 2. Profile
    r = requests.put(f"{BASE_URL}/profile", headers=headers, json={"name": "A", "phone": "1234567890"})
    check(r.status_code == 400, f"Profile: Name length < 2 returned {r.status_code} instead of 400")
    r = requests.put(f"{BASE_URL}/profile", headers=headers, json={"name": "Valid", "phone": "123"})
    check(r.status_code == 400, f"Profile: Phone < 10 digits returned {r.status_code} instead of 400")
    r = requests.put(f"{BASE_URL}/profile", headers=headers, json={"name": "Valid", "phone": "12345678901"})
    check(r.status_code == 400, f"Profile: Phone > 10 digits returned {r.status_code} instead of 400")

    # 3. Addresses
    r = requests.post(f"{BASE_URL}/addresses", headers=headers, json={"label": "INVALID", "street": "123 Valid St", "city": "City", "pincode": 123456, "is_default": False})
    check(r.status_code == 400, f"Addresses: Invalid label returning {r.status_code} instead of 400")
    r = requests.post(f"{BASE_URL}/addresses", headers=headers, json={"label": "HOME", "street": "St", "city": "City", "pincode": 123456, "is_default": False})
    check(r.status_code == 400, f"Addresses: Street len < 5 returning {r.status_code} instead of 400")
    r = requests.post(f"{BASE_URL}/addresses", headers=headers, json={"label": "HOME", "street": "123 Valid St", "city": "C", "pincode": 123456, "is_default": False})
    check(r.status_code == 400, f"Addresses: City len < 2 returning {r.status_code} instead of 400")
    r = requests.post(f"{BASE_URL}/addresses", headers=headers, json={"label": "HOME", "street": "123 Valid St", "city": "City", "pincode": 12345, "is_default": False})
    check(r.status_code == 400, f"Addresses: Pincode < 6 digits returning {r.status_code} instead of 400")
    r = requests.post(f"{BASE_URL}/addresses", headers=headers, json={"label": "HOME", "street": "123 Valid St", "city": "City", "pincode": 123456, "is_default": False})
    addr_id = None
    if r.status_code == 200 or r.status_code == 201:
        check("address_id" in r.json(), "Addresses: Did not return address_id on success")
        addr_id = r.json().get("address_id")
    else:
        check(False, f"Addresses: Valid address payload rejected with {r.status_code}: {r.text}")
    
    if addr_id:
        r = requests.put(f"{BASE_URL}/addresses/{addr_id}", headers=headers, json={"label": "OFFICE", "street": "Updated St", "city": "NewCity", "pincode": 654321, "is_default": False})
        if r.status_code == 200:
            data = r.json()
            check(data.get("label") == "HOME", f"Addresses: PUT allowed changing label to {data.get('label')}")
            check(data.get("city") == "City", f"Addresses: PUT allowed changing city to {data.get('city')}")
            check(data.get("pincode") in [123456, '123456'], f"Addresses: PUT allowed changing pincode to {data.get('pincode')}")

    r = requests.delete(f"{BASE_URL}/addresses/999999", headers=headers)
    check(r.status_code == 404, f"Addresses: Delete non-existent returned {r.status_code} instead of 404")

    # 4. Products
    r = requests.get(f"{BASE_URL}/admin/products", headers=headers)
    all_products = r.json() if r.status_code == 200 else []
    r = requests.get(f"{BASE_URL}/products", headers=headers)
    if r.status_code == 200:
        active_products = r.json()
        inactive = [p for p in all_products if not p.get("is_active", True)]
        if inactive:
            for p in active_products:
                check(p["product_id"] != inactive[0]["product_id"], "Products: Inactive products shown in /products list")
    
    r = requests.get(f"{BASE_URL}/products/999999", headers=headers)
    check(r.status_code == 404, f"Products: GET non-existent returned {r.status_code} instead of 404")

    # 5. Cart
    r = requests.post(f"{BASE_URL}/cart/add", headers=headers, json={"product_id": 1, "quantity": 0})
    check(r.status_code == 400, f"Cart Add: Qty 0 returned {r.status_code} instead of 400")
    r = requests.post(f"{BASE_URL}/cart/add", headers=headers, json={"product_id": 1, "quantity": -5})
    check(r.status_code == 400, f"Cart Add: Qty -5 returned {r.status_code} instead of 400")
    r = requests.post(f"{BASE_URL}/cart/add", headers=headers, json={"product_id": 999999, "quantity": 1})
    check(r.status_code == 404, f"Cart Add: Non-existent product returned {r.status_code} instead of 404")
    # We would need to know stock for next tests...

    # 6. Reviews
    r = requests.post(f"{BASE_URL}/products/1/reviews", headers=headers, json={"rating": 6, "comment": "Nice"})
    check(r.status_code == 400, f"Reviews: Rating 6 returned {r.status_code} instead of 400")
    r = requests.post(f"{BASE_URL}/products/1/reviews", headers=headers, json={"rating": 0, "comment": "Nice"})
    check(r.status_code == 400, f"Reviews: Rating 0 returned {r.status_code} instead of 400")

    # 7. Wallet
    r = requests.post(f"{BASE_URL}/wallet/add", headers=headers, json={"amount": 0})
    check(r.status_code == 400, f"Wallet Add: Amount 0 returned {r.status_code} instead of 400")
    r = requests.post(f"{BASE_URL}/wallet/add", headers=headers, json={"amount": -10})
    check(r.status_code == 400, f"Wallet Add: Amount -10 returned {r.status_code} instead of 400")
    r = requests.post(f"{BASE_URL}/wallet/add", headers=headers, json={"amount": 100001})
    check(r.status_code == 400, f"Wallet Add: Amount > 100000 returned {r.status_code} instead of 400")

    # Print bugs
    for b in bugs:
        print("BUG:", b)

if __name__ == "__main__":
    probe()
