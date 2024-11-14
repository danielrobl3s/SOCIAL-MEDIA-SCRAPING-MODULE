from builtins import WindowsError
import os
import subprocess
from pathlib import Path
import winreg

def install_cert():
    # Get the mitmproxy cert path
    cert_path = os.path.join(str(Path.home()), '.mitmproxy', 'mitmproxy-ca-cert.cer')
    
    if not os.path.exists(cert_path):
        print("Certificate not found. Please run mitmproxy first to generate certificates.")
        return False
    
    try:
        # Import the certificate using certutil
        result = subprocess.run(
            ['certutil', '-addstore', 'ROOT', cert_path],
            capture_output=True,
            text=True,
            shell=True  # Required for Windows
        )
        
        if result.returncode == 0:
            print("Certificate installed successfully!")
            return True
        else:
            print(f"Failed to install certificate: {result.stderr}")
            return False
            
    except Exception as e:
        print(f"Error installing certificate: {e}")
        return False

def check_cert_installed():
    try:
        # Open the ROOT certificates store
        key = winreg.OpenKey(
            winreg.HKEY_LOCAL_MACHINE,
            r"SOFTWARE\Microsoft\SystemCertificates\ROOT\Certificates",
            0,
            winreg.KEY_READ
        )
        
        # Check if mitmproxy cert exists
        try:
            winreg.OpenKey(key, "mitmproxy", 0, winreg.KEY_READ)
            return True
        except WindowsError:
            return False
            
    except Exception as e:
        print(f"Error checking certificate: {e}")
        return False

def main():
    print("Checking if mitmproxy certificate is already installed...")
    
    if check_cert_installed():
        print("Certificate is already installed!")
        return
    
    print("Installing mitmproxy certificate...")
    if install_cert():
        print("Certificate installation complete!")
    else:
        print("Please try manual installation:")
        print("1. Open mmc.exe")
        print("2. File -> Add/Remove Snap-in -> Certificates -> Add")
        print("3. Select 'Computer account' -> Next -> Local computer -> Finish -> OK")
        print("4. Navigate to Trusted Root Certification Authorities -> Certificates")
        print("5. Right-click -> All Tasks -> Import")
        print(f"6. Import the certificate from: {os.path.join(str(Path.home()), '.mitmproxy', 'mitmproxy-ca-cert.cer')}")

if __name__ == "__main__":
    # Need to run as administrator
    main()