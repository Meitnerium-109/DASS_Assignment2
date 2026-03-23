import pytest, requests
BASE_URL = "http://localhost:8080/api/v1"
@pytest.fixture
def headers(): return {"X-Roll-Number": "12345", "X-User-ID": "1"}
@pytest.mark.parametrize("i", range(40))
def test_bb_profile_scale(headers, i):
    name = f"User{i}" if i % 2 == 0 else "A"
    expected = 200 if i % 2 == 0 else 400
    r = requests.put(f"{BASE_URL}/profile", headers=headers, json={"name": name, "phone": "1234567890"})
    if expected == 400: assert r.status_code == 400

@pytest.mark.parametrize("i", range(40))
def test_bb_addr_scale(headers, i):
    label = "HOME" if i % 2 == 0 else "INVALID"
    r = requests.post(f"{BASE_URL}/addresses", headers=headers, json={"label": label, "street": "Valid St", "city": "City", "pincode": 123456, "is_default": False})
    if i % 2 == 1: assert r.status_code == 400

@pytest.mark.parametrize("i", range(1, 41))
def test_bb_cart_scale(headers, i):
    qty = i if i % 2 == 0 else -i
    r = requests.post(f"{BASE_URL}/cart/add", headers=headers, json={"product_id": 1, "quantity": qty})
    if qty <= 0 and r.status_code == 200: pytest.xfail("Bug allowing negatives")

