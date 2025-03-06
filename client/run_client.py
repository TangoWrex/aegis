#!/usr/bin/env python3
import os
import subprocess
from dotenv import load_dotenv

# Load environment variables from .env in parent directory
env_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), ".env")
load_dotenv(env_path)

def run_client():
    # Use current directory (client/) as working directory
    client_dir = os.path.dirname(__file__)
    os.chdir(client_dir)

    # Get API key from .env
    api_key = os.getenv("AEGIS_API_KEY")
    if not api_key:
        print("Error: AEGIS_API_KEY not set in .env (expected in project root)")
        return

    # Check if dependencies are installed
    print("Checking client dependencies...")
    deps = ["gpsd-py3", "requests", "python-dotenv"]
    for dep in deps:
        check_result = subprocess.run(["pip", "show", dep], capture_output=True, text=True)
        if check_result.returncode != 0:
            print(f"Installing {dep}...")
            subprocess.run(["pip", "install", dep], check=True)

    # Run the client
    print("Starting client...")
    client_result = subprocess.run(["python", "client.py"], env={**os.environ, "AEGIS_API_KEY": api_key})
    if client_result.returncode != 0:
        print("Client failed to start—check output above for errors")

if __name__ == "__main__":
    run_client()