#!/usr/bin/env python3
"""
Example: Endercom Agent Server Wrapper

This example demonstrates how to use the Endercom Python SDK as a server wrapper
with heartbeat and a2a endpoints, similar to the master-orchestrator-endpoint.py structure.

To run this example:
1. Install dependencies: pip install fastapi uvicorn pydantic
2. Set environment variables:
   - FREQUENCY_API_KEY
   - FREQUENCY_ID
   - AGENT_NAME
3. Run: python server_wrapper_example.py
"""

import os
import logging
from endercom import AgentOptions, ServerOptions, create_server_agent, Message

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Example message handler
def custom_message_handler(message: Message) -> str:
    """
    Custom message handler that processes messages.

    Args:
        message: The received message

    Returns:
        Response string
    """
    logger.info(f"Processing message: {message.content}")

    # Example: Simple echo with processing
    if "hello" in message.content.lower():
        return f"Hello! You said: {message.content}"
    elif "analyze" in message.content.lower():
        return f"Analysis complete for: {message.content}"
    elif "status" in message.content.lower():
        return "Agent is running and ready to process requests."
    else:
        return f"Processed: {message.content}"

def main():
    """Main function to run the server wrapper example."""

    # Configuration
    agent_options = AgentOptions(
        frequency_api_key=os.getenv("FREQUENCY_API_KEY", "your-frequency-api-key"),
        frequency_id=os.getenv("FREQUENCY_ID", "your-frequency-id"),
        agent_name=os.getenv("AGENT_NAME", "your-agent-name"),
        base_url=os.getenv("BASE_URL", "https://endercom.io")
    )

    server_options = ServerOptions(
        host="0.0.0.0",
        port=8000,
        enable_heartbeat=True,
        enable_a2a=True,
        frequency_api_key=os.getenv("FREQUENCY_API_KEY")  # For authentication
    )

    try:
        # Create agent with server wrapper functionality
        agent = create_server_agent(
            agent_options=agent_options,
            server_options=server_options,
            message_handler=custom_message_handler
        )

        logger.info("Starting Endercom Agent Server Wrapper...")
        logger.info("Available endpoints:")
        logger.info("  - GET  /health or /heartbeat - Health check")
        logger.info("  - POST /a2a - Agent-to-agent communication")
        logger.info("  - GET  / - Service information")
        logger.info("")
        logger.info("Example API calls:")
        logger.info("  curl -H 'Authorization: Bearer YOUR_FREQUENCY_API_KEY' http://localhost:8000/health")
        logger.info("  curl -H 'Authorization: Bearer YOUR_FREQUENCY_API_KEY' -H 'Content-Type: application/json' \\")
        logger.info("       -d '{\"content\": \"Hello, agent!\"}' http://localhost:8000/a2a")

        # Run the server
        agent.run_server(server_options)

    except ImportError as e:
        logger.error(f"Missing dependencies: {e}")
        logger.error("Please install: pip install fastapi uvicorn pydantic")
    except Exception as e:
        logger.error(f"Error starting server: {e}")

if __name__ == "__main__":
    main()