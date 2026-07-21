from mcp.server import Server
from mcp.types import Tool, TextContent
from services import ProductService
from models import Product
import asyncio

# Initialize Server and Service
server = Server("stock-server")
service = ProductService()


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
            description="Search for products by name or SKU.",
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
            description="List all products which are out of stock in the database.",
            inputSchema={
                "type": "object",
                "properties": {}
            }
        ),
        Tool(
            name="list_low_stock",
            description="List the products with the low stock in the database.",
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

                    "product_id" : {
                        "type":"integer",
                        "description" : "The database ID of the product"

                    },
                    "quantity" :{
                        "type" : "integer",
                        "description" : "Quantity to order"
                    },
                    "expected_delivery_date" : {
                        "type" : "string" ,
                        "description" : "Optional ISO-8601 delivery date string (e.g., '2026-07-25T14:00:00')"
                    }
                

                    
                }
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