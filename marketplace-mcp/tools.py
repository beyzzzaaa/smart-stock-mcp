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
            description="List all marketplace sellers with their rating and base delivery times.",
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
            description="Compare marketplace offers for a product ID using the TOPSIS multi-criteria decision-making algorithm based on price, shipping fee, delivery time, and stock availability.",
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
            description="Check whether the requested quantity of a marketplace offer is currently available by its offer ID.",
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
    description="Create a purchase draft for one or more marketplace offers.",
    inputSchema={
        "type": "object",
        "properties": {
            "items": {
                "type": "array",
                "description": "Marketplace offers to add to the purchase draft.",
                "items": {
                    "type": "object",
                    "properties": {
                        "offer_id": {
                            "type": "integer",
                            "description": "Marketplace offer ID."
                        },
                        "quantity": {
                            "type": "integer",
                            "description": "Quantity to purchase."
                        }
                    },
                    "required": ["offer_id", "quantity"]
                }
            }
        },
        "required": ["items"]
    }
),
        Tool(
            name="place_order",
            description="Place the order for the purchase draft.",
            inputSchema={
                "type": "object",
                "properties": {
                    "draft_id": {
                        "type": "integer",
                        "description": "Purchase draft ID to place the order for."
                    },
                },
                "required": ["draft_id"],
            }
        ),
        Tool(
            name="get_order_status",
            description="Get the status of an order.",
            inputSchema={
                "type": "object",
                "properties": {
                    "order_id": {
                        "type": "integer",
                        "description": "The ID of the order to get the status of."
                    }
                },
                "required": ["order_id"],
            }
        ),    
    ]

@server.call_tool()
async def handle_call_tool(name: str, arguments: dict | None) -> list[TextContent]:
    """Execute the tool selected by LLM using MarketplaceService"""
    arguments = arguments or {}
    try: 
        if name == "list_sellers":
            sellers = await service.get_all_sellers()
            if not sellers:
                return [TextContent(type="text", text="No marketplace sellers found.")]

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

        elif name == "search_offers":
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
                    f"Product SKU: {offer.product.sku} | Name: {offer.product.name}\n"
                    f"Seller: {offer.seller.name} (ID: {offer.seller.id}, Rating: {offer.seller.rating:.1f}/5)\n"
                    f"Price: {offer.price} TL | Shipping Fee: {offer.shippingFee} TL\n"
                    f"Estimated Delivery Time: {offer.deliveryTimeDays} day(s) | Stock: {offer.stockQuantity}\n"
                )
            return [TextContent(type="text", text="Matching Offers:\n\n" + "\n".join(lines))]

        elif name == "compare_offers":
            product_id = arguments.get("product_id")
            if not product_id: 
                return [TextContent(type="text", text="No product ID provided.")]
            result = await service.compare_offers(product_id)
            if not result or not result.offers: 
                return [TextContent(type="text", text=f"No offers found for product ID: {product_id}")]
            
            lines = ["--- Offers Ranked by TOPSIS ---"]
            for offer in result.offers:
                lines.append(
                    f"TOPSIS Score: {offer.topsisScore:.4f} | Offer ID: {offer.id}\n"
                    f"  - Seller: {offer.seller.name} | Price: {offer.price} TL | Shipping: {offer.shippingFee} TL\n"
                    f"  - Delivery: {offer.deliveryTimeDays} day(s) | Stock: {offer.stockQuantity}\n"
                )
            
            if result.bestChoice:
                best = result.bestChoice
                lines.append("\n TOPSIS BEST CHOICE RECOMMENDATION:")
                lines.append(
                    f"Seller: {best.seller.name} (Price: {best.price} TL, "
                    f"Shipping: {best.shippingFee} TL, Delivery: {best.deliveryTimeDays} days, TOPSIS Score: {best.topsisScore:.4f})"
                )
            return [TextContent(type="text", text="\n".join(lines))]

        elif name == "check_availability":
            offer_id = arguments.get("offer_id")
            quantity = arguments.get("quantity")
            if not offer_id or not quantity:
                return [TextContent(type="text", text="No offer ID or quantity provided.")]
            available = await service.check_availability(offer_id,quantity)
            if available:
                return [TextContent(type="text", text=f"Offer ID: {offer_id} is available for {quantity} items.")]
            else:
                return [TextContent(type="text", text=f"Offer ID: {offer_id} is not available for {quantity} items.")]
        elif name == "create_purchase_draft":
            items = arguments.get("items")
            if not items:
                return [TextContent(type="text", text="No items provided.")]
            draft = await service.create_purchase_draft(items)
            return [TextContent(type="text", text=f"Purchase draft created with ID: {draft.id}.")]
        elif name == "place_order":
            draft_id = arguments.get("draft_id")
            if not draft_id:
                return [TextContent(type="text", text="No draft ID provided.")]
            try:
                order = await service.place_order(draft_id)
                return [TextContent(type="text", text=f"Order created with ID: {order.id}.")]
            except Exception as e:
                return [TextContent(type="text", text=f"Error placing order: {str(e)}")]  
        elif name == "get_order_status":
            order_id = arguments.get("order_id")
            if not order_id:
                return [TextContent(type="text", text="No order ID provided.")]
            try:
                status = await service.get_order_details(order_id)
                if not status:
                    return [TextContent(type="text", text=f"Order with ID {order_id} not found.")]
                return [TextContent(type="text", text=f"Order with ID {order_id} has status {status.status}.")]
            except Exception as e:
                return [TextContent(type="text", text=f"Error getting order status: {str(e)}")]
    except Exception as e:
        return [TextContent(type="text", text=f"Error executing tool: {str(e)}")]
    return [TextContent(type="text", text="Invalid tool name.")]

if __name__ == "__main__":
    from mcp.server.stdio import stdio_server
    from mcp.server.models import InitializationOptions
    import mcp.types as types

    async def main():
        async with stdio_server() as (read_stream, write_stream):
            await server.run(
                read_stream,
                write_stream,
                InitializationOptions(
                    server_name="marketplace-server",
                    server_version="0.1.0",
                    capabilities=server.get_capabilities(
                        notification_options=types.NotificationOptions(),
                        experimental_capabilities={},
                    ),
                ),
            )

    asyncio.run(main())

            