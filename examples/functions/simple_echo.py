#!/usr/bin/env python3
"""
Simple Echo Function - Python Example
Demonstrates the simplest possible Endercom agent function.
"""

from endercom import AgentFunction

# Create a simple function that echoes back whatever it receives
function = AgentFunction(
    name="Simple Echo",
    description="Echoes back any input it receives",
    capabilities=["echo", "test"]
)

@function.handler
def echo_handler(input_data):
    """
    Simple handler that echoes the input back.
    """
    return {
        "original_input": input_data,
        "message": "Echo from Python function!",
        "type": type(input_data).__name__
    }

if __name__ == "__main__":
    # Start the function on port 3001
    function.run(port=3001)