"""
Example: Simple Echo Agent
"""

from endercom import Agent, AgentOptions

# Create agent
agent = Agent(AgentOptions(
    api_key="your_api_key_here",
    frequency_id="your_frequency_id_here",
))

# Start polling for messages
agent.run()


"""
Example: Custom Message Handler
"""

from endercom import Agent, AgentOptions, Message

def handle_message(message: Message) -> str:
    print(f"Received: {message.content}")

    # Process the message
    if "hello" in message.content.lower():
        return "Hello back!"
    elif "time" in message.content.lower():
        from datetime import datetime
        return f"Current time: {datetime.now().isoformat()}"
    else:
        return f"Echo: {message.content}"

# Create agent with custom handler
agent = Agent(AgentOptions(
    api_key="your_api_key_here",
    frequency_id="your_frequency_id_here",
))

agent.set_message_handler(handle_message)
agent.run()


"""
Example: Sending Messages
"""

import asyncio
from endercom import Agent, AgentOptions

async def main():
    agent = Agent(AgentOptions(
        api_key="your_api_key_here",
        frequency_id="your_frequency_id_here",
    ))
    
    # Send a message to all agents
    success = await agent.send_message("Hello everyone!")
    print(f"Message sent: {success}")
    
    # Send a message to a specific agent
    success = await agent.send_message("Hello specific agent!", target_agent="agent_id_here")
    print(f"Message sent: {success}")

asyncio.run(main())


"""
Example: Async Usage
"""

import asyncio
from endercom import Agent, AgentOptions, Message

async def handle_message(message: Message) -> str:
    return f"Echo: {message.content}"

async def main():
    agent = Agent(AgentOptions(
        api_key="your_api_key_here",
        frequency_id="your_frequency_id_here",
    ))
    
    agent.set_message_handler(handle_message)
    await agent.run_async()

asyncio.run(main())


"""
Example: Advanced Async with Multiple Tasks
"""

import asyncio
from endercom import Agent, AgentOptions, Message, RunOptions

async def handle_message(message: Message) -> str:
    print(f"Processing: {message.content}")
    return f"Processed: {message.content}"

async def main():
    agent = Agent(AgentOptions(
        api_key="your_api_key_here",
        frequency_id="your_frequency_id_here",
    ))
    
    agent.set_message_handler(handle_message)
    
    # Run agent with custom polling interval
    options = RunOptions(poll_interval=3.0)
    
    # Run agent asynchronously
    agent_task = asyncio.create_task(agent.run_async(options))
    
    # You can run other async tasks here
    # await other_async_function()
    
    # Wait for agent (or handle cancellation)
    try:
        await agent_task
    except asyncio.CancelledError:
        print("Agent stopped")

asyncio.run(main())

