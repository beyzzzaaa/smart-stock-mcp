import httpx
from typing import List, Optional
from models import MarketplaceSeller, MarketplaceOffer, MarketplacePurchaseDraft, MarketplaceOrder

class MarketplaceService:
    def __init__(self, base_url: str = "http://localhost:8081"):
        self.base_url = base_url

    async def get_all_sellers(self) -> List[MarketplaceSeller]:
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{self.base_url}/api/marketplace/sellers")
            response.raise_for_status()
            return [MarketplaceSeller(**item) for item in response.json()]

    async def search_offers(self, query: Optional[str] = None) -> List[MarketplaceOffer]:
        async with httpx.AsyncClient() as client:
            params = {}
            if query:
                params["query"] = query
            response = await client.get(f"{self.base_url}/api/marketplace/offers", params=params)
            response.raise_for_status()
            return [MarketplaceOffer(**item) for item in response.json()]

    async def get_offers_for_sku(self, sku: str) -> List[MarketplaceOffer]:
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{self.base_url}/api/marketplace/offers/compare", params={"sku": sku})
            response.raise_for_status()
            return [MarketplaceOffer(**item) for item in response.json()]

    async def check_availability(self, sku: str, seller_id: int, quantity: int) -> bool:
        async with httpx.AsyncClient() as client:
            params = {"sku": sku, "sellerId": seller_id, "quantity": quantity}
            response = await client.get(f"{self.base_url}/api/marketplace/check-availability", params=params)
            response.raise_for_status()
            return response.json()

    async def create_draft(self, items: List[dict]) -> MarketplacePurchaseDraft:
        # Map python style seller_id to Java style sellerId
        payload_items = []
        for item in items:
            payload_items.append({
                "sku": item["sku"],
                "quantity": item["quantity"],
                "sellerId": item.get("seller_id") or item.get("sellerId")
            })

        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self.base_url}/api/marketplace/drafts",
                json={"items": payload_items}
            )
            response.raise_for_status()
            return MarketplacePurchaseDraft(**response.json())

    async def place_order(self, draft_id: int) -> MarketplaceOrder:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self.base_url}/api/marketplace/orders",
                json={"draftId": draft_id}
            )
            response.raise_for_status()
            return MarketplaceOrder(**response.json())

    async def get_order_details(self, order_id: int) -> MarketplaceOrder:
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{self.base_url}/api/marketplace/orders/{order_id}")
            response.raise_for_status()
            return MarketplaceOrder(**response.json())
