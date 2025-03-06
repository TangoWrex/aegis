#!/usr/bin/env python3
import os
import subprocess
import threading
from http.server import SimpleHTTPRequestHandler, HTTPServer
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

    # Function to run the client.py
    def start_client():
        print("Starting client...")
        client_result = subprocess.run(["python", "client.py"], env={**os.environ, "AEGIS_API_KEY": api_key})
        if client_result.returncode != 0:
            print("Client failed to start—check output above for errors")

    # Function to start the local web server for GUI
    def start_web_server():
        print("Starting local web server for GUI on http://localhost:8001...")
        os.chdir(client_dir)  # Ensure server runs from client directory
        handler = SimpleHTTPRequestHandler
        server = HTTPServer(('localhost', 8001), handler)
        server.serve_forever()

    # Start client in a separate thread
    client_thread = threading.Thread(target=start_client, daemon=True)
    client_thread.start()

    # Start web server in a separate thread
    web_thread = threading.Thread(target=start_web_server, daemon=True)
    web_thread.start()

    # Keep the main thread alive to allow threads to run
    try:
        client_thread.join()
        web_thread.join()
    except KeyboardInterrupt:
        print("Shutting down...")
        # Optionally terminate subprocesses if needed
        import signal
        os.killpg(os.getpgid(client_result.pid), signal.SIGTERM) if 'client_result' in locals() else None

if __name__ == "__main__":
    run_client()