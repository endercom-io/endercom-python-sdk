#!/usr/bin/env python3
"""
Data Processor Function - Python Example
Demonstrates data processing capabilities.
"""

from endercom import AgentFunction
import json
import statistics
import datetime

# Create a data processing function
function = AgentFunction(
    name="Data Processor",
    description="Processes and analyzes data arrays",
    capabilities=["analyze", "process", "statistics", "data"]
)

@function.handler
def process_data(input_data):
    """
    Process data and return analytics.
    Expects input like: {"data": [1,2,3,4,5]} or {"numbers": [1,2,3]}
    """
    try:
        # Extract data array from various input formats
        data = None
        if isinstance(input_data, dict):
            data = input_data.get('data') or input_data.get('numbers') or input_data.get('values')
        elif isinstance(input_data, list):
            data = input_data

        if not data:
            return {
                "error": "No data found. Expected format: {'data': [1,2,3,4,5]}",
                "example": {"data": [1, 2, 3, 4, 5]}
            }

        # Convert to numbers if possible
        try:
            numbers = [float(x) for x in data]
        except (ValueError, TypeError):
            return {
                "error": "Data must be an array of numbers",
                "received": data
            }

        if not numbers:
            return {"error": "Empty data array"}

        # Calculate statistics
        result = {
            "input_data": data,
            "processed_at": datetime.datetime.now().isoformat(),
            "statistics": {
                "count": len(numbers),
                "sum": sum(numbers),
                "mean": statistics.mean(numbers),
                "min": min(numbers),
                "max": max(numbers),
                "range": max(numbers) - min(numbers)
            }
        }

        # Add additional stats for larger datasets
        if len(numbers) > 1:
            result["statistics"]["median"] = statistics.median(numbers)
            result["statistics"]["std_dev"] = statistics.stdev(numbers)

        return result

    except Exception as e:
        return {
            "error": f"Processing failed: {str(e)}",
            "input_received": input_data
        }

if __name__ == "__main__":
    print("Starting Data Processor function...")
    print("Example usage:")
    print('  POST http://localhost:3002/execute')
    print('  Body: {"input": {"data": [1, 2, 3, 4, 5]}}')

    function.run(port=3002)