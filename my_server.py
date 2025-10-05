"""MCP server implementation with JWT authentication.

This server uses the FastMCP library to create an MCP server with JWT-based
authentication. It automatically generates RSA key pairs for development if
they don't exist, and provides a simple 'greet' tool for demonstration purposes.
"""

import os

from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from fastmcp import FastMCP  # type: ignore
from fastmcp.server.auth.providers.jwt import JWTVerifier  # type: ignore

# Try to load public key from environment variable first (for cloud deployment)
# Fall back to file-based keys for local development
PUBLIC_KEY_PEM = os.getenv("PUBLIC_KEY_PEM")
PRIVATE_KEY_PEM = os.getenv("PRIVATE_KEY_PEM")

if PUBLIC_KEY_PEM:
    # Cloud deployment: use environment variables
    public_key_data = PUBLIC_KEY_PEM.encode()
else:
    # Local development: use or generate file-based keys
    if not os.path.exists("private.pem") or not os.path.exists("public.pem"):
        # Generate RSA key pair
        private_key = rsa.generate_private_key(public_exponent=65537, key_size=2048)

        # Get private key PEM
        private_pem = private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.NoEncryption(),
        )

        # Get public key PEM
        public_key = private_key.public_key()
        public_pem = public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo,
        )

        # Save keys
        with open("private.pem", "wb") as f:
            f.write(private_pem)
        with open("public.pem", "wb") as f:
            f.write(public_pem)

    # Load public key from file
    with open("public.pem", "rb") as f:
        public_key_data = f.read()

auth = JWTVerifier(public_key=public_key_data.decode("utf-8"), algorithm="RS256")
mcp = FastMCP("My MCP Server", auth=auth)


@mcp.tool
def greet(name: str) -> str:
    """Greet a person by name."""
    return f"Hello, {name}!"


if __name__ == "__main__":
    mcp.run(transport="http", host="0.0.0.0", port=8000)
