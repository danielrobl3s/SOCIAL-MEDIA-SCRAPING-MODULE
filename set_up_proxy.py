import os
import subprocess
import time
import shutil

def start_and_stop_mitmproxy():
    """
    Starts mitmproxy to generate certificates and stops it after a few seconds.
    """
    try:
        # Start mitmproxy in a subprocess
        process = subprocess.Popen(["mitmproxy"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        print("Starting mitmproxy to generate certificates...")
        time.sleep(5)  # Allow time for mitmproxy to generate the certificates
        process.terminate()  # Stop mitmproxy
        process.wait()
        print("Stopped mitmproxy.")
    except Exception as e:
        print(f"Error while running mitmproxy: {e}")
        process.terminate()
        process.wait()
        exit(1)

def install_mitmproxy_certificates():
    """
    Installs the mitmproxy certificates on Windows using certutil.
    """
    home_dir = os.path.expanduser("~")
    cert_source_path = os.path.join(home_dir, ".mitmproxy", "mitmproxy-ca-cert.cer")
    
    if not os.path.exists(cert_source_path):
        print(f"Certificate not found at {cert_source_path}.")
        return
    
    cert_dest_path = os.path.join(os.getcwd(), "mitmproxy-ca-cert.cer")
    shutil.copy(cert_source_path, cert_dest_path)
    print(f"Copied certificate to {cert_dest_path}.")

    try:
        # Install the certificate to the Windows root store
        print("Installing the certificate...")
        subprocess.run(
            ["certutil", "-addstore", "root", cert_dest_path],
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        print("Certificate installed successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Error during certificate installation: {e}")
    finally:
        # Clean up the copied certificate
        if os.path.exists(cert_dest_path):
            os.remove(cert_dest_path)
            print(f"Removed temporary certificate at {cert_dest_path}.")

if __name__ == "__main__":
    start_and_stop_mitmproxy()
    install_mitmproxy_certificates()
