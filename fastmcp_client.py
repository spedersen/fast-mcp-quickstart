"""FastMCP client demonstrating MCP server interaction.

This client connects to an MCP server using JWT authentication and demonstrates
how to list available tools, resources, and prompts, as well as execute tool calls.
It uses RSA key-based authentication to secure the connection.
"""

import asyncio
import os
import time

import jwt
from fastmcp import Client

# Load private key from environment variable or file
PRIVATE_KEY_PEM = os.getenv("PRIVATE_KEY_PEM")
if PRIVATE_KEY_PEM:
    private_key = PRIVATE_KEY_PEM.encode()
else:
    with open("./private.pem", "rb") as f:
        private_key = f.read()

# Generate a JWT token for authentication
payload = {
    "iat": int(time.time()),  # issued at
    "exp": int(time.time()) + 3600,  # expires in 1 hour
}

TOKEN = jwt.encode(payload, private_key, algorithm="RS256")

# Use environment variable for endpoint, default to localhost
MCP_ENDPOINT = os.getenv("MCP_ENDPOINT", "http://localhost:8000/mcp")
client = Client(MCP_ENDPOINT, auth=TOKEN)


async def main():
    """Connect to MCP server and demonstrate available operations."""
    async with client:
        # Ensure client can connect
        await client.ping()

        # List available operations
        tools = await client.list_tools()
        print(f"Available tools: {tools}")
        resources = await client.list_resources()
        print(f"Available resources: {resources}")
        prompts = await client.list_prompts()
        print(f"Available prompts: {prompts}")

        # Ex. execute a tool call
        result = await client.call_tool("greet", {"name": "World"})
        print(result)


asyncio.run(main())
