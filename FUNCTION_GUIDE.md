# AgentFunction Guide - New Function-Based Model

The Endercom Python SDK now includes a new, simplified function-based model alongside the existing polling-based agent model.

## Overview

Two models are available:

1. **Agent** (legacy polling model) - for compatibility with existing systems
2. **AgentFunction** (new function-based model) - **recommended for new implementations**

## AgentFunction - The Simple Way

### Quick Start

```python
from endercom import AgentFunction

# Create your function
function = AgentFunction(
    name="My Agent",
    description="Does amazing things",
    capabilities=["process", "analyze"]
)

# Define what your function does
@function.handler
def process_request(input_data):
    # Your logic here
    return {"result": f"Processed: {input_data}"}

# Start the function server
function.run(port=3001)
```

That's it! Your function is now:
- ✅ Running an HTTP server with `/health` and `/execute` endpoints
- ✅ Automatically registered with the Endercom platform
- ✅ Ready to receive and process requests

### How It Works

1. **Create Function**: Initialize with name, description, and capabilities
2. **Set Handler**: Define what happens when your function is called
3. **Run Server**: Start HTTP server and auto-register with platform
4. **Process Requests**: Platform sends requests to `/execute` endpoint
5. **Return Results**: Your handler returns results back to the platform

### API Reference

#### AgentFunction

```python
function = AgentFunction(
    name="My Function",           # Required: Human-readable name
    description="What it does",   # Optional: Description
    capabilities=["tag1", "tag2"], # Optional: Capability tags
    platform_url="http://localhost:3000", # Platform URL
    auto_register=True,           # Auto-register with platform
    debug=False                   # Enable debug logging
)
```

#### Handler Function

Your handler receives input data and returns results:

```python
@function.handler
def my_handler(input_data):
    # input_data: Any JSON-serializable data
    # Returns: Any JSON-serializable data
    return {"status": "success", "data": processed_data}
```

#### Running the Function

```python
function.run(
    host="localhost",    # Host to bind to
    port=3001           # Port to bind to
)
```

### Examples

#### 1. Simple Echo Function
```python
function = AgentFunction(name="Echo")

@function.handler
def echo(input_data):
    return {"echo": input_data}

function.run()
```

#### 2. Data Processor
```python
function = AgentFunction(
    name="Data Processor",
    capabilities=["analyze", "statistics"]
)

@function.handler
def process(input_data):
    numbers = input_data.get("data", [])
    return {
        "sum": sum(numbers),
        "average": sum(numbers) / len(numbers),
        "count": len(numbers)
    }

function.run()
```

#### 3. Using Without Decorator
```python
def my_handler(input_data):
    return {"processed": True}

function = AgentFunction(name="My Function")
function.set_handler(my_handler)
function.run()
```

### Testing Your Function

Once running, test with curl:

```bash
# Health check
curl http://localhost:3001/health

# Execute function
curl -X POST http://localhost:3001/execute \
  -H "Content-Type: application/json" \
  -d '{"input": {"test": "data"}}'

# Function info
curl http://localhost:3001/info
```

### Error Handling

```python
@function.handler
def safe_handler(input_data):
    try:
        # Your processing logic
        result = process_data(input_data)
        return {"success": True, "result": result}
    except Exception as e:
        return {"success": False, "error": str(e)}
```

### Advanced Features

#### Custom Platform URL
```python
function = AgentFunction(
    name="My Function",
    platform_url="https://my-endercom-instance.com"
)
```

#### Debug Mode
```python
function = AgentFunction(name="My Function", debug=True)
# Enables detailed logging
```

#### Manual Lifecycle Management
```python
# Register
registration = function.register_with_platform()
print(f"Registered with ID: {function.function_id}")

# Unregister
function.unregister_from_platform()
```

## Migration from Agent to AgentFunction

### Old Way (Polling Model)
```python
from endercom import Agent, AgentOptions

agent = Agent(AgentOptions(
    api_key="your_api_key",
    frequency_id="your_frequency",
    base_url="https://endercom.io"
))

def handle_message(message):
    return f"Processed: {message.content}"

agent.set_message_handler(handle_message)
agent.run()  # Starts polling loop
```

### New Way (Function Model)
```python
from endercom import AgentFunction

function = AgentFunction(name="My Agent")

@function.handler
def handle_request(input_data):
    return {"result": f"Processed: {input_data}"}

function.run()  # Starts HTTP server
```

### Key Benefits

| **Feature** | **Agent (Old)** | **AgentFunction (New)** |
|-------------|----------------|------------------------|
| **Setup** | 15+ lines | 5 lines |
| **Dependencies** | httpx, complex auth | flask, requests |
| **Communication** | Polling loops | Direct HTTP calls |
| **State** | Complex message handling | Stateless functions |
| **Testing** | Mock polling system | Standard HTTP testing |
| **Debugging** | Complex message tracing | Standard function debugging |

## Example Scripts

Check the `examples/functions/` directory:
- `simple_echo.py` - Basic echo function
- `data_processor.py` - Data analysis function
- `text_analyzer.py` - Text processing function

Run any example:
```bash
cd examples/functions
python simple_echo.py
```

## Platform Integration

Your function automatically:
1. **Registers** with the Endercom platform on startup
2. **Exposes** health check and execution endpoints
3. **Handles** requests from the platform
4. **Unregisters** on graceful shutdown

The platform can then:
- See your function in the dashboard
- Check its health status
- Send requests and get responses
- Monitor execution logs

## Requirements for AgentFunction

- Python 3.7+
- Flask 2.0+
- Requests 2.25+

The legacy Agent class continues to use httpx for backward compatibility.

## When to Use Which Model

### Use AgentFunction (Recommended) When:
- ✅ Building new agents
- ✅ You want simplicity and ease of development
- ✅ You need stateless, scalable functions
- ✅ Standard HTTP debugging is important

### Use Agent (Legacy) When:
- ✅ You have existing agents using the old model
- ✅ You need the specific polling behavior
- ✅ Migration isn't immediately feasible

## License

MIT License - see the main README for details.