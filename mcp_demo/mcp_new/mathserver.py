from mcp.server.fastmcp import FastMCP

mcp = FastMCP()

@mcp.tool("add", description="Add two numbers")
def add(a: int, b: int) -> int:
    """Add two numbers and return the result."""

    return a + b

@mcp.tool("subtract", description="Subtract two numbers")
def subtract(a: int, b: int) -> int:
    """Subtract two numbers and return the result."""

    return a - b

@mcp.tool("multiply", description="Multiply two numbers")
def multiply(a: int, b: int) -> int:   
    """Multiply two numbers and return the result."""

    return a * b

# The arguement transport tells the server how to communicate with the client.
# In this case, we are using stdio, which means that the server will read from
# standard input and write to standard output.
if __name__ == "__main__":
    mcp.run(transport="stdio")