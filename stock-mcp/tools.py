from mcp.server import Server
from mcp.types import Tool, TextContent
from services import ProductService
import asyncio

# Initialize Server and Service
server = Server("stock-server")
service = ProductService()


def format_products(products):
    if not products:
        return "No products found."

    lines = []
    for p in products:
        cat = (
            p.subcategory.category.name
            if p.subcategory and p.subcategory.category
            else "N/A"
        )
        sub = (
            p.subcategory.name
            if p.subcategory
            else "N/A"
        )
        brand = (
            p.model.brand.name
            if p.model and p.model.brand
            else "N/A"
        )
        model_name = (
            p.model.name
            if p.model
            else "N/A"
        )

        lines.append(
            f"ID: {p.id} | SKU: {p.sku} | Name: {p.name}\n"
            f"  - Category: {cat} > {sub} | Brand: {brand} | Model: {model_name}\n"
            f"  - Stock: {p.stockQuantity} "
            f"(Min: {p.minimumStock}, Target: {p.targetStock})\n"
            f"  - Location: {p.warehouseInfo or 'N/A'}"
        )

    return "\n".join(lines)


@server.list_tools()
async def list_tools() -> list[Tool]:
    """List all available tools."""
    return [
        Tool(
            name="list_products",
            description="List all products with their SKU, stock levels, and warehouse location.",
            inputSchema={
                "type": "object",
                "properties": {},
            }
        ),
        Tool(
            name="search_products",
            description="Search for products by name or SKU or description.",
            inputSchema={
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "Search query text."
                    }
                },
                "required": ["query"]
            }
        ),
        Tool(
            name="list_out_of_stock",
            description="List all products which are currently completely out of stock (quantity = 0)",
            inputSchema={
                "type": "object",
                "properties": {}
            }
        ),
        Tool(
            name="list_low_stock",
            description="List the products whose stock levels are at or below their defined minimum thresholds (excluding out-of-stock).",
            inputSchema={
                "type": "object",
                "properties": {},
            }
        ),
        Tool(
            name="calculate_replenishment",
            description="Calculate replenishment quantities for products based on current stock levels and pending incoming orders.",
            inputSchema={
                "type": "object",
                "properties": {},
            }
        ),
        Tool(
            name="create_incoming_order",
            description="Create a pending incoming order to record expected stock replenishment.",
            inputSchema={
                "type": "object",
                "properties": {
                    "product_id": {
                        "type": "integer",
                        "description": "The database ID of the product"
                    },
                    "quantity": {
                        "type": "integer",
                        "description": "Quantity to order"
                    },
                    "expected_delivery_date": {
                        "type": "string",
                        "description": "Optional ISO-8601 delivery date string (e.g., '2026-07-25T14:00:00')"
                    }
                },
                "required": ["product_id", "quantity"]
            }
        ),
        Tool(
            name="receive_order",
            description="Mark a pending order as RECEIVED and add its quantity to current stock levels.",
            inputSchema={
                "type": "object",
                "properties": {
                    "order_id": {
                        "type": "integer",
                        "description": "ID of the pending order to receive."
                    }
                },
                "required": ["order_id"]
            }
        ),
        Tool(
            name="get_stock_replenishment_needed",
            description="Get a list of all products that need stock replenishment, with calculated order quantities.",
            inputSchema={
                "type": "object",
                "properties": {},
            }
        )
    ]


@server.tool_call()
async def handle_call_tool(name: str, arguments: dict | None) -> list[TextContent]:
    """Execute the tool selected by LLM using ProductService"""
    arguments = arguments or {}
    try:
        if name == "list_products":
            products = await service.get_all_products()
            return [
                TextContent(
                    type="text",
                    text=format_products(products)
                )
            ]

        elif name == "search_products":
            query = arguments.get("query", "")
            products = await service.search_products(query)
            if not products:
                return [TextContent(type="text", text=f"No products matched search query: '{query}'")]

            lines = []
            for p in products:
                lines.append(f"ID: {p.id} | SKU: {p.sku} | Name: {p.name} | Stock: {p.stockQuantity}")
            return [TextContent(type="text", text="\n".join(lines))]

        elif name == "list_out_of_stock":
            products = await service.get_out_of_stock_products()
            if not products:
                return [TextContent(type="text", text="No products are out of stock.")]

            lines = []
            for p in products:
                lines.append(f"ID: {p.id} | SKU: {p.sku} | Name: {p.name} | Stock: {p.stockQuantity}")
            return [TextContent(type="text", text="\n".join(lines))]

        elif name == "list_low_stock":
            products = await service.get_low_stock_products()
            if not products:
                return [TextContent(type="text", text="No products are low on stock.")]

            lines = []
            for p in products:
                lines.append(f"ID: {p.id} | SKU: {p.sku} | Name: {p.name} | Stock: {p.stockQuantity} (Min: {p.minimumStock})")
            return [TextContent(type="text", text="\n".join(lines))]

        elif name in ("calculate_replenishment", "get_stock_replenishment_needed"):
            replenishments = await service.calculate_replenishment()
            if not replenishments:
                return [TextContent(type="text", text="No replenishment is needed at this time.")]
            lines = []
            for r in replenishments:
                lines.append(
                    f"Product ID: {r.productId} | SKU: {r.sku} | Name: {r.productName} | "
                    f"Replenishment Needed: {r.replenishmentQuantityNeeded}"
                )
            return [TextContent(type="text", text="\n".join(lines))]

        elif name == "create_incoming_order":
            product_id = arguments.get("product_id")
            quantity = arguments.get("quantity")
            expected_delivery_date = arguments.get("expected_delivery_date")
            order = await service.create_incoming_order(product_id, quantity, expected_delivery_date)
            if order:
                return [TextContent(type="text", text=f"Incoming order created successfully with ID: {order.id}")]
            else:
                return [TextContent(type="text", text="Failed to create incoming order")]

        elif name == "receive_order":
            order_id = arguments.get("order_id")
            order = await service.receive_order(order_id)
            if order:
                return [TextContent(type="text", text=f"Order {order.id} received successfully.")]
            else:
                return [TextContent(type="text", text="Failed to receive order.")]

        else:
            return [TextContent(type="text", text=f"Unknown tool name: {name}")]

    except Exception as e:
        return [TextContent(type="text", text=f"Error executing tool {name}: {str(e)}")]


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
                    server_name="stock-server",
                    server_version="0.1.0",
                    capabilities=server.get_capabilities(
                        notification_options=types.NotificationOptions(),
                        experimental_capabilities={},
                    ),
                ),
            )

    asyncio.run(main())
