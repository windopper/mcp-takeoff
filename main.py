from mcp.server.fastmcp import FastMCP
from typing import Any
import httpx

mcp = FastMCP('takeoff')

API_BASE = "https://ai-takeoff.dev/api"
USER_AGENT = "mcp-takeoff/1.0"

async def make_takeoff_request(endpoint: str) -> dict[str, Any] | None:
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(f"{API_BASE}/{endpoint}", headers={"User-Agent": USER_AGENT})
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(f"Error: {e}")
            return None

@mcp.tool()
async def get_latest_posts() -> str:
    """Get the latest AI issue posts from the Takeoff API"""
    result = await make_takeoff_request("posts")
    return str(result) if result else "Failed to fetch posts"

@mcp.tool()
async def get_latest_weekly_news() -> str:
    """Get the latest AI weekly news from the Takeoff API"""
    result = await make_takeoff_request("weeklynews")
    return str(result) if result else "Failed to fetch weekly news"

if __name__ == "__main__":
    mcp.run(transport='stdio')