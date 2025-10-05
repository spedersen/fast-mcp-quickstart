"""MCP client for testing the FastMCP server.

This client demonstrates how to connect to and call tools on an MCP server
using JWT authentication. It generates a signed JWT token using an RSA private
key and uses it to authenticate requests to the server.
"""

import asyncio
import os
import time

import jwt  # type: ignore
from fastmcp import Client  # type: ignore

# Load private key from environment variable or file
PRIVATE_KEY_PEM = os.getenv("PRIVATE_KEY_PEM")
if PRIVATE_KEY_PEM:
    private_key = PRIVATE_KEY_PEM.encode()
else:
    with open("private.pem", "rb") as f:
        private_key = f.read()

# Generate a JWT token for authentication
payload = {
    "iat": int(time.time()),  # issued at
    "exp": int(time.time()) + 3600,  # expires in 1 hour
}

TOKEN = jwt.encode(payload, private_key.decode(), algorithm="RS256")

# Use environment variable for endpoint, default to localhost
MCP_ENDPOINT = os.getenv("MCP_ENDPOINT", "http://localhost:8000/mcp")
client = Client(MCP_ENDPOINT, auth=TOKEN)


async def call_tool(name: str):
    """Call the greet tool on the MCP server."""
    async with client:
        result = await client.call_tool("greet", {"name": name})
        print(result)


asyncio.run(call_tool("Ford"))
