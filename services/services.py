SERVICES = {
    "nakrutka": {
        "name": "Instagram xizmat",
        "price_per_1000": 17499
    }
}


def calculate_price(service: str, quantity: int):
    service_data = SERVICES.get(service)

    if not service_data:
        return None

    return round(
        quantity * service_data["price_per_1000"] / 1000
    )