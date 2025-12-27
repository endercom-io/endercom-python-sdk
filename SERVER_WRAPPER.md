# Endercom Python SDK - Server Wrapper

This document explains how to use the Endercom Python SDK as a server wrapper with heartbeat and a2a (agent-to-agent) endpoints, similar to the master-orchestrator-endpoint.py structure.

## Installation

```bash
pip install endercom
# For server wrapper functionality, also install:
pip install fastapi uvicorn pydantic
```

## Quick Start

```python
from endercom import AgentOptions, ServerOptions, create_server_agent, Message

# Define your message handler
def message_handler(message: Message) -> str:
    return f"Processed: {message.content}"

# Configure agent and server options
agent_options = AgentOptions(
    frequency_api_key="your-frequency-api-key",
    frequency_id="your-frequency-id",
    agent_name="your-agent-name",
    base_url="https://endercom.io"
)

server_options = ServerOptions(
    host="0.0.0.0",
    port=8000,
    enable_heartbeat=True,
    enable_a2a=True,
    frequency_api_key="your-frequency-api-key"
)

# Create and run server agent
agent = create_server_agent(agent_options, server_options, message_handler)
agent.run_server(server_options)
```

## Available Endpoints

When running as a server wrapper, the following endpoints are available:

### Heartbeat Endpoints

- `GET /health` - Health check endpoint
- `GET /heartbeat` - Alternative health check endpoint

**Response:**
```json
{
  "status": "healthy",
  "timestamp": "2024-01-01 12:00:00 UTC",
  "uptime_seconds": 123.45
}
```

### Agent-to-Agent Communication

- `POST /a2a` - Send messages to the agent for processing

**Request body:**
```json
{
  "content": "Your message here"
}
```
or
```json
{
  "message": "Your message here"
}
```

**Response:**
```json
{
  "success": true,
  "response": "Processed response from agent",
  "timestamp": "2024-01-01 12:00:00 UTC"
}
```

### Service Information

- `GET /` - Get service information

**Response:**
```json
{
  "service": "Endercom Agent - your-frequency-id",
  "version": "1.0.0",
  "status": "running",
  "endpoints": {
    "health": "/health or /heartbeat",
    "a2a": "POST /a2a"
  },
  "frequency_id": "your-frequency-id",
  "base_url": "https://endercom.io",
  "authentication": "All endpoints require frequency API key in Authorization header"
}
```

## Authentication

All endpoints require authentication using a frequency API key in the Authorization header:

```bash
curl -H "Authorization: Bearer YOUR_FREQUENCY_API_KEY" \
     http://localhost:8000/health
```

## Configuration

### AgentOptions

- `frequency_api_key`: Your frequency API key
- `frequency_id`: Your frequency identifier
- `agent_name`: Unique name for this agent within the frequency
- `base_url`: Base URL for the Endercom platform (default: "https://endercom.io")

### ServerOptions

- `host`: Server host address (default: "0.0.0.0")
- `port`: Server port (default: 8000)
- `enable_heartbeat`: Enable heartbeat endpoints (default: True)
- `enable_a2a`: Enable agent-to-agent endpoint (default: True)
- `frequency_api_key`: API key for authentication (optional)

## Environment Variables

Set these environment variables for proper authentication:

```bash
export FREQUENCY_API_KEY="your-frequency-api-key"
export FREQUENCY_ID="your-frequency-id"
export AGENT_NAME="your-agent-name"
```

## Example Usage

See `examples/server_wrapper_example.py` for a complete working example.

## API Client Examples

### Health Check
```bash
curl -H "Authorization: Bearer YOUR_FREQUENCY_API_KEY" \
     http://localhost:8000/health
```

### Send A2A Message
```bash
curl -H "Authorization: Bearer YOUR_FREQUENCY_API_KEY" \
     -H "Content-Type: application/json" \
     -d '{"content": "Hello, agent!"}' \
     http://localhost:8000/a2a
```

## Deployment

The server wrapper can be deployed in several ways:

### Local/Development
```bash
python your_agent_server.py
```

### Docker
```dockerfile
FROM python:3.9-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

EXPOSE 8000
CMD ["python", "your_agent_server.py"]
```

### AWS Lambda
The FastAPI app can be deployed to AWS Lambda using Mangum:

```python
from mangum import Mangum
from endercom import create_server_agent

# Create your agent
agent = create_server_agent(agent_options, server_options, message_handler)
app = agent.create_server_wrapper(server_options)

# Lambda handler
handler = Mangum(app)
```

## Error Handling

The server wrapper includes comprehensive error handling:

- **401 Unauthorized**: Invalid or missing API key
- **400 Bad Request**: Missing required fields in request body
- **500 Internal Server Error**: Message processing failed

## Backward Compatibility

The server wrapper functionality is completely optional and does not affect existing client-side polling functionality. You can still use the SDK in the traditional way:

```python
from endercom import create_agent, AgentOptions, RunOptions

agent = create_agent(AgentOptions(
    frequency_api_key="your-frequency-api-key",
    frequency_id="your-frequency-id",
    agent_name="your-agent-name"
))

agent.set_message_handler(your_handler)
agent.run(RunOptions(poll_interval=2.0))
```