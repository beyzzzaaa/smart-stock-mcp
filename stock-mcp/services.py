import httpx
from typing import List, Optional
from models import Product, Replenishment, IncomingOrder

class ProductService:
    def __init__(self, base_url: str = "http://localhost:8081"):
        self.base_url = base_url

    async def get_all_products(self) -> List[Product]:
        """Fetch all products from the Spring Boot API."""
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{self.base_url}/api/products")
            response.raise_for_status()
            return [Product(**item) for item in response.json()]

    async def search_products(self, query: str) -> List[Product]:
        """Search products by name, SKU, or description."""
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{self.base_url}/api/products/search", params={"query": query})
            response.raise_for_status()
            return [Product(**item) for item in response.json()]

    async def get_out_of_stock_products(self) -> List[Product]:
        """Fetch out-of-stock products (quantity = 0)."""
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{self.base_url}/api/products/out-of-stock")
            response.raise_for_status()
            return [Product(**item) for item in response.json()]

    async def get_low_stock_products(self) -> List[Product]:
        """Fetch low-stock products (quantity <= min_stock)."""
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{self.base_url}/api/products/low-stock")
            response.raise_for_status()
            return [Product(**item) for item in response.json()]

    async def calculate_replenishment(self) -> List[Replenishment]:
        """Calculate quantity to order for products below minimum stock."""
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{self.base_url}/api/products/replenishment")
            response.raise_for_status()
            return [Replenishment(**item) for item in response.json()]

    async def create_incoming_order(self, product_id: int, quantity: int, expected_delivery_date: Optional[str] = None) -> IncomingOrder:
        """Create a pending incoming/replenishment order."""
        async with httpx.AsyncClient() as client:
            payload = {"productId": product_id, "quantity": quantity}
            if expected_delivery_date:
                payload["expectedDeliveryDate"] = expected_delivery_date
            
            response = await client.post(f"{self.base_url}/api/orders", json=payload)
            response.raise_for_status()
            return IncomingOrder(**response.json())

    async def receive_order(self, order_id: int) -> IncomingOrder:
        """Mark an incoming order as received, increasing product stock."""
        async with httpx.AsyncClient() as client:
            response = await client.post(f"{self.base_url}/api/orders/{order_id}/receive")
            response.raise_for_status()
            return IncomingOrder(**response.json())
