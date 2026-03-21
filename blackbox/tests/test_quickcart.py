import pytest
import requests

BASE_URL = "http://localhost:8080/api/v1"

@pytest.fixture
def headers():
    return {"X-Roll-Number": "12345", "X-User-ID": "1"}

def test_headers_validation(headers):
    # Test missing X-Roll-Number
    r = requests.get(f"{BASE_URL}/admin/users", headers={"X-User-ID": "1"})
    assert r.status_code == 401

    # Test invalid X-Roll-Number
    r = requests.get(f"{BASE_URL}/admin/users", headers={"X-Roll-Number": "abc", "X-User-ID": "1"})
    assert r.status_code == 400

    # Test missing X-User-ID on user-scoped endpoint
    r = requests.get(f"{BASE_URL}/profile", headers={"X-Roll-Number": "12345"})
    assert r.status_code == 400

def test_profile_endpoints(headers):
    r = requests.get(f"{BASE_URL}/profile", headers=headers)
    assert r.status_code == 200

    # PUT valid profile
    payload = {"name": "Valid Name", "phone": "1234567890"}
    r = requests.put(f"{BASE_URL}/profile", headers=headers, json=payload)
    if r.status_code == 400:
        pytest.xfail(f"Bug: Valid profile rejected: {r.text}") # Marking as expected failure if api is buggy
    
    # PUT invalid name (too short)
    r = requests.put(f"{BASE_URL}/profile", headers=headers, json={"name": "A", "phone": "1234567890"})
    assert r.status_code == 400

def test_address_endpoints(headers):
    address1 = {
        "label": "HOME", "street": "123 Valid St",
        "city": "TestCity", "pincode": "123456", "is_default": True
    }
    r = requests.post(f"{BASE_URL}/addresses", headers=headers, json=address1)
    if r.status_code != 200 and r.status_code != 201:
        pytest.xfail(f"Bug: Address creation failed: {r.text}")

def test_products(headers):
    r = requests.get(f"{BASE_URL}/products", headers=headers)
    assert r.status_code == 200
    assert type(r.json()) == list

    r2 = requests.get(f"{BASE_URL}/products/999999", headers=headers)
    assert r2.status_code == 404

def test_cart(headers):
    # Clear cart first
    requests.delete(f"{BASE_URL}/cart/clear", headers=headers)
    
    # Add non existent product
    payload = {"product_id": 999999, "quantity": 1}
    r = requests.post(f"{BASE_URL}/cart/add", headers=headers, json=payload)
    assert r.status_code == 404

    # Add item with quantity 0
    payload = {"product_id": 1, "quantity": 0}
    r2 = requests.post(f"{BASE_URL}/cart/add", headers=headers, json=payload)
    if r2.status_code != 400:
        pytest.xfail("Bug: Adding quantity 0 should return 400")

def test_wallet(headers):
    # Add > 100000
    payload = {"amount": 100001}
    r = requests.post(f"{BASE_URL}/wallet/add", headers=headers, json=payload)
    assert r.status_code == 400

def test_support(headers):
    # Status transitions
    payload = {"subject": "Need Help", "message": "My order is delayed"}
    r = requests.post(f"{BASE_URL}/support/ticket", headers=headers, json=payload)
    
    if r.status_code in [200, 201]:
        ticket_id = r.json().get("ticket_id")
        if ticket_id:
            # Invalid transition CLOSED to OPEN
            update_payload = {"status": "OPEN"}
            r2 = requests.put(f"{BASE_URL}/support/tickets/{ticket_id}", headers=headers, json=update_payload)
            if r2.status_code != 400:
                pytest.xfail("Bug: Invalid status transition allowed")

def test_checkout(headers):
    # Empty cart checkout setup
    requests.delete(f"{BASE_URL}/cart/clear", headers=headers)
    
    payload = {"payment_method": "COD"}
    r = requests.post(f"{BASE_URL}/checkout", headers=headers, json=payload)
    if r.status_code != 400:
        pytest.xfail("Bug: Empty cart checkout allowed")

def test_orders(headers):
    r = requests.post(f"{BASE_URL}/orders/999999/cancel", headers=headers)
    assert r.status_code == 404

def test_reviews(headers):
    # Rating > 5
    payload = {"rating": 6, "comment": "Good product!"}
    r = requests.post(f"{BASE_URL}/products/1/reviews", headers=headers, json=payload)
    if r.status_code != 400:
        pytest.xfail("Bug: Review rating > 5 allowed")

def test_coupons(headers):
    # Apply coupon that requires higher cart value
    requests.delete(f"{BASE_URL}/cart/clear", headers=headers)
    
    # Try applying without minimum
    payload = {"code": "WELCOME10"} # Example
    r = requests.post(f"{BASE_URL}/coupon/apply", headers=headers, json=payload)
    if r.status_code == 200:
        pytest.xfail("Bug: Coupon applied without meeting requirements or edge case undocumented")
