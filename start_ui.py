import subprocess
import webbrowser
import time

def start_mlflow_ui():
    """Starts the MLflow tracking server and opens the UI in a web browser."""
    host = "127.0.0.1"
    port = 5000
    url = f"http://{host}:{port}"

    print(f"Starting MLflow Tracking Server and UI...")
    
    try:
        # Start the MLflow server as a background process
        command = [
            "mlflow", "server",
            "--backend-store-uri", "sqlite:///mlruns.db",
            "--default-artifact-root", "./mlruns-artifacts",
            "--host", host,
            "--port", str(port)
        ]
        process = subprocess.Popen(command)
        
        print(f"MLflow server started with PID: {process.pid}")
        print(f"You can view the UI at {url}")
        
        # Give the server a moment to start up before opening the browser
        time.sleep(2)
        webbrowser.open(url)

        # Keep the script running until interrupted
        process.wait()

    except FileNotFoundError:
        print("\nError: 'mlflow' command not found.")
        print("Please make sure MLflow is installed and in your system's PATH.")
        print("You can install it with: pip install mlflow")
    except KeyboardInterrupt:
        print("\nStopping MLflow server...")
        process.terminate()
        process.wait()
        print("MLflow server stopped.")

if __name__ == "__main__":
    start_mlflow_ui()
