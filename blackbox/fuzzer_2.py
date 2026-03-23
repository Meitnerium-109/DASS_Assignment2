import requests

BASE_URL = "http://localhost:8080/api/v1"
headers = {"X-Roll-Number": "12345", "X-User-ID": "1"}
bugs = []

def check(condition, desc):
    if not condition:
        bugs.append(desc)

def probe():
    # 8. Checkout
    # Clear cart
    requests.delete(f"{BASE_URL}/cart/clear", headers=headers)
    r = requests.post(f"{BASE_URL}/checkout", headers=headers, json={"payment_method": "COD"})
    check(r.status_code == 400, f"Checkout: Empty cart returned {r.status_code} instead of 400")

    # Add expensive item (assuming prod 1 is cheap, maybe prod > 5000?)
    # Just try payment_method INVALID
    r = requests.post(f"{BASE_URL}/checkout", headers=headers, json={"payment_method": "XYZ"})
    check(r.status_code == 400, f"Checkout: Invalid payment method returned {r.status_code} instead of 400")

    # 9. Loyalty
    r = requests.post(f"{BASE_URL}/loyalty/redeem", headers=headers, json={"points": 0})
    check(r.status_code == 400, f"Loyalty: Redeem 0 points returned {r.status_code} instead of 400")
    r = requests.post(f"{BASE_URL}/loyalty/redeem", headers=headers, json={"points": -10})
    check(r.status_code == 400, f"Loyalty: Redeem -10 points returned {r.status_code} instead of 400")

    # 10. Support
    r = requests.post(f"{BASE_URL}/support/ticket", headers=headers, json={"subject": "Abc", "message": "Valid message"})
    check(r.status_code == 400, f"Support: Subject < 5 chars returned {r.status_code} instead of 400")

    r = requests.post(f"{BASE_URL}/support/ticket", headers=headers, json={"subject": "Valid Subject", "message": ""})
    check(r.status_code == 400, f"Support: Empty message returned {r.status_code} instead of 400")

    # 11. Custom logic tests
    r = requests.post(f"{BASE_URL}/coupon/apply", headers=headers, json={"code": "INVALID_COUPON"})
    # What does invalid coupon return? Usually 400 or 404
    check(r.status_code in [400, 404], f"Coupon: Invalid coupon returned {r.status_code} instead of 400/404")

    print("\nMore Bugs found:")
    for b in bugs:
        print("BUG:", b)

if __name__ == "__main__":
    probe()
