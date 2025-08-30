"""Zenopay payment."""

from elusion.zenopay import ZenoPay
from elusion.zenopay.models.order import NewOrder
from elusion.zenopay.utils import generate_id

# Initialize client (uses environment variables)
client = ZenoPay()

# Create order (sync)
with client:
    order = NewOrder(
        order_id=generate_id(),
        buyer_email="customer@example.com",
        buyer_name="John Doe",
        buyer_phone="07XXXXXXXX",
        amount=1000,
    )
    response = client.orders.sync.create(order)
    print(f"Order ID: {response.results.order_id}")
