"""
Example usage of the HackerNews Parser API.

This script demonstrates how to start the API server and make requests
with both v1 and v2 data formats.
"""

import json
import time
from pathlib import Path
from threading import Thread
from typing import Any

import requests

from hackernews_parser.server import run_server


def start_api_server():
    """Start the API server in a separate thread."""
    server_thread = Thread(target=run_server, kwargs={"port": 8000, "reload": False})
    server_thread.daemon = True
    server_thread.start()

    # Wait for server to start
    time.sleep(2)
    return server_thread


def load_example_data(version: str) -> Any:
    """Load example data from the data directory."""
    data_file = Path(__file__).parent.parent / "data" / f"hackernews_{version}.json"
    with open(data_file) as f:
        return json.load(f)


def test_api_endpoint(data: dict, version: str):
    """Test the API with the provided data."""
    url = "http://localhost:8000/parse"

    print(f"\n=== Testing API with version {version} data ===")
    print(f"Sending request to: {url}")

    try:
        response = requests.post(url, json=data, timeout=10)

        if response.status_code == 200:
            result = response.json()
            print(f"✅ Success! Parsed {len(result['stories'])} stories")
            print(f"Version: {result['version']}")
            print(f"First story title: {result['stories'][0]['title']}")

            if "metrics" in result:
                print(f"Dataset metrics: {result['metrics']}")
        else:
            print(f"❌ Error {response.status_code}: {response.text}")

    except requests.exceptions.RequestException as e:
        print(f"❌ Request failed: {e}")


def main():
    """Main function to demonstrate API usage."""
    print("🚀 Starting HackerNews Parser API Demo")

    # Start the API server
    print("Starting API server on http://localhost:8000...")
    start_api_server()

    # Test health endpoint
    try:
        health_response = requests.get("http://localhost:8000/health", timeout=5)
        if health_response.status_code == 200:
            print("✅ API server is healthy")
        else:
            print("❌ API server health check failed")
            return
    except requests.exceptions.RequestException:
        print("❌ Could not connect to API server")
        return

    # Load and test with v1 data
    v1_data = load_example_data("v1")
    test_api_endpoint(v1_data, "v1")

    # Load and test with v2 data
    v2_data = load_example_data("v2")
    test_api_endpoint(v2_data, "v2")

    print("\n📖 API Documentation available at: http://localhost:8000/docs")
    print("🔍 Interactive API testing at: http://localhost:8000/docs")
    print("\nPress Ctrl+C to stop the server")

    try:
        # Keep the main thread alive
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n👋 Shutting down...")


if __name__ == "__main__":
    main()
