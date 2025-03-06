#!/usr/bin/env python3
import os
import subprocess
import time
from dotenv import load_dotenv

# Load environment variables from .env in parent directory
env_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), ".env")
load_dotenv(env_path)

def run_server():
    # Use current directory (server/) as working directory
    server_dir = os.path.dirname(__file__)
    os.chdir(server_dir)

    # Get API key from .env
    api_key = os.getenv("AEGIS_API_KEY")
    if not api_key:
        print("Error: AEGIS_API_KEY not set in .env (expected in project root)")
        return

    # Stop the running container if it exists
    print("Stopping aegis container...")
    subprocess.run(["docker", "stop", "aegis"], capture_output=True, text=True)

    # Remove the container if it exists
    print("Removing aegis container...")
    subprocess.run(["docker", "rm", "aegis"], capture_output=True, text=True)

    # Build the Docker image
    print("Building aegis-server image...")
    build_result = subprocess.run(["docker", "build", "-t", "aegis-server", "."], capture_output=True, text=True)
    if build_result.returncode != 0:
        print("Build failed:", build_result.stderr)
        return

    # Run the container with volume mount and API key
    print("Starting aegis container...")
    run_cmd = [
        "docker", "run", "-d", "-p", "8000:8000",
        "-v", f"{os.getcwd()}:/app",
        "-e", f"AEGIS_API_KEY={api_key}",
        "--name", "aegis", "aegis-server"
    ]
    run_result = subprocess.run(run_cmd, capture_output=True, text=True)
    if run_result.returncode != 0:
        print("Failed to start aegis:", run_result.stderr)
        return

    # Wait and check if it's running
    time.sleep(2)
    check_result = subprocess.run(["docker", "ps"], capture_output=True, text=True)
    if "aegis" in check_result.stdout:
        print("Aegis server is running on http://localhost:8000")
    else:
        print("Failed to start aegis—check Docker logs with 'docker logs aegis'")

if __name__ == "__main__":
    run_server()