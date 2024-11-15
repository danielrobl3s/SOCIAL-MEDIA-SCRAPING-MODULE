import os
import signal
import subprocess
import time
from pathlib import Path

def start_mitmproxy(script_name):
    """Start mitmproxy with the specified script."""
    print("Starting mitmproxy...")
    process = subprocess.Popen(
        ["mitmproxy", "-s", script_name],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    return process

def stop_mitmproxy(process):
    """Stop mitmproxy gracefully."""
    print("Stopping mitmproxy...")
    os.kill(process.pid, signal.SIGTERM)  # Send a termination signal
    process.wait()  # Ensure the process has terminated
    print("mitmproxy stopped.")

def install_certificate():
    """Install mitmproxy certificate on macOS."""
    cert_path = Path.home() / ".mitmproxy/mitmproxy-ca-cert.pem"
    if not cert_path.exists():
        print(f"Certificate not found at {cert_path}. Did you start mitmproxy at least once?")
        return

    try:
        print("Installing mitmproxy certificate...")
        # Copy the certificate to the system keychain
        subprocess.run(
            ["sudo", "security", "add-trusted-cert", "-d", "-r", "trustRoot", "-k", 
             "/Library/Keychains/System.keychain", str(cert_path)],
            check=True
        )
        print("mitmproxy certificate installed successfully!")
    except subprocess.CalledProcessError as e:
        print(f"Failed to install certificate: {e}")

def main():
    script_name = "request_capture.py"
    duration = 30  # Time in seconds to run mitmproxy

    # Start mitmproxy
    process = start_mitmproxy(script_name)

    try:
        # Wait for the specified duration
        time.sleep(duration)
    except KeyboardInterrupt:
        print("Interrupted by user.")
    finally:
        # Stop mitmproxy and clean up
        stop_mitmproxy(process)
        # Install the certificate
        install_certificate()

if __name__ == "__main__":
    main()
