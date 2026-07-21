from dns import name
from mcp.server import Server
from mcp.types import Tool, TextContent
import asyncio
from services import MarketplaceService

# Initialize Server and Service
server = Server("marketplace-server")
service = MarketplaceService()

@server.list_tools()
async def list_tools() -> list[Tool]:
    """List all available tools."""
    return [
             Tool(
            name="list_sellers",
            description="List all marketplace sellers.",
            inputSchema={
                "type": "object",
                "properties": {},
            }
        ),
        Tool(
            name="search_offers",
            description="Search marketplace offers by product name or category and return matching sellers, prices, stock availability, shipping fees, and estimated delivery times.",
            inputSchema={
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "Product name or category to search for.",
                    },
                },
                "required": ["query"],
            }
        ),
        Tool(
            name="compare_offers",
            description="Compare marketplace offers using the TOPSIS multi-criteria decision-making algorithm based on price, shipping fee, delivery time, and stock availability.",
            inputSchema={
                "type": "object",
                "properties": {
                    "product_id": {
                        "type": "integer",
                        "description": "Product ID to compare offers for.",
                    },
                },
                "required": ["product_id"],
            }
        ),
        Tool(
            name="check_availability",
            description="Check whether the requested quantity of a marketplace offer is currently available.",
            inputSchema={
                "type": "object",
                "properties": {
                    "offer_id": {
                        "type": "integer",
                        "description": "Offer ID to check availability for."
                    },
                        "quantity": {
                            "type": "integer",
                            "description": "Quantity to check availability for."
                            
                        },
                        
                },
                "required": ["offer_id", "quantity"],
            }
        ),
        Tool(
            name="create_purchase_draft",
            description="Create a purchase draft for one or more marketplace offers. The draft will be created only for offers that have sufficient stock available. The draft will include all the necessary information for placing the order.",
            inputSchema={
                "type": "object",
                "properties": {
                    "offer_id": {
                        "type": "integer",
                        "description": "Offer ID to create a purchase draft for."
                    },
                        "quantity": {
                            "type": "integer",
                            "description": "Quantity to create a purchase draft for."
                            
                        },
                        
                },
                "required": ["offer_id", "quantity"],
            }
        ),
        Tool(
            name="place_order",
            description="Place the order for the purchase draft.",
            inputSchema={
                "type": "object",
                "properties": {
                    "purchase_draft_id": {
                        "type": "integer",
                        "description": "Purchase draft ID to place the order for."
                    },
                },
                "required": ["purchase_draft_id"],
            }
        ),
        Tool(
            name="get_order_status",
            description="Get the status of an order.",
            inputSchema={
                "type": "object",
                "properties": {
                    "order_id" :{
                        "type" : "integer",
                        "description" : "The ID of the order to get the status of."
                    }
                },
                "required": ["order_id"],
            }
        ),    
    ]
@server.tool_call()
async def handle_call_tool(name: str, arguments: dict | None) -> list[TextContent]:
    """Execute the tool selected by LLM using MarketplaceService"""
    arguments = arguments or {}
    try : 
        if name=="list_sellers" :
            sellers = await service.list_sellers()
            if not sellers:
        return [
            TextContent(
                type="text",
                text="No marketplace sellers found."
            )
        ]

    lines = []

    for seller in sellers:
        lines.append(
            f"Seller ID: {seller.id}\n"
            f"Name: {seller.name}\n"
            f"Rating: {seller.rating:.1f}/5\n"
            f"Base Delivery Time: {seller.baseDeliveryDays} day(s)\n"
        )

    return [
        TextContent(
            type="text",
            text="Marketplace Sellers:\n\n" + "\n".join(lines)
        )
    ]
    elif name=="search_offers" :
        query = arguments.get("query")
        if not query:
            return [TextContent(type="text", text="No query provided.")]
        offers = await service.search_offers(query)
        if not offers:
            return [TextContent(type="text", text=f"No offers found for query: {query}")]
        lines = []
        for offer in offers:
            lines.append(
                f"Offer ID: {offer.id}\n"
                f"Product ID: {offer.productId}\n"
                f"Seller ID: {offer.sellerId}\n"
                f"Price: {offer.price}\n"
                f"Stock Availability: {offer.stockAvailability}\n"
                f"Shipping Fee: {offer.shippingFee}\n"
                f"Estimated Delivery Time: {offer.estimatedDeliveryTime}\n"
            )
        return [TextContent(type="text", text="\n".join(lines))]
       elif name == "compare_offers" : 
        product_id = arguments.get("product_id")
        if not product_id: 
            return [TextContent(type="text", text="No product ID provided.")]
        offers = await service.compare_offers(product_id)
        if not offers: 
            return [TextContent(type="text", text=f"No offers found for product ID: {product_id}")]
        lines = []
        for offer in offers:
            lines.append(
                f"Offer ID: {offer.id}\n"
                f"Product ID: {offer.productId}\n"
                f"Seller ID: {offer.sellerId}\n"
                f"Price: {offer.price}\n"
                f"Stock Availability: {offer.stockAvailability}\n"
                f"Shipping Fee: {offer.shippingFee}\n"
                f"Estimated Delivery Time: {offer.estimatedDeliveryTime}\n"
            ) 
        return [TextContent(type="text", text="\n".join(lines))]
    elif name == "check_availability":
        
