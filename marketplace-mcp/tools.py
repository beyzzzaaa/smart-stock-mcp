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
            
            






        
    ]
