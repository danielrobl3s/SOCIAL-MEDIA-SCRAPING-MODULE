import json
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

# Set up Chrome options
chrome_options = Options()
chrome_options.add_argument("--enable-logging")
chrome_options.add_argument("--v=1")
chrome_options.set_capability("goog:loggingPrefs", {"performance": "ALL", "browser": "ALL"})

# Initialize ChromeDriver service
driver_service = Service("chromedriver-mac-arm64/chromedriver")
driver = webdriver.Chrome(service=driver_service, options=chrome_options)

# Navigate to the website
driver.get("https://facebook.com/DuaLipa")
time.sleep(60)  # Allow time for interactions (login, etc.)

# Fetch performance logs
log_entries = driver.get_log("performance")

# Extract headers, payloads, URLs, and other details
for entry in log_entries:

    with open("logs2.txt", "a", newline="") as file:
        file.write(str(entry)+"\n")
    try:
        obj_serialized = entry.get("message")
        obj = json.loads(obj_serialized)
        message = obj.get("message")
        method = message.get("method")

        # Capture request details
        if method == "Network.requestWillBeSent":
            params = message.get("params", {})
            request = params.get("request", {})
            request_headers = request.get("headers", {})
            post_data = request.get("postData", None)  # Contains POST payload if available
            url = request.get("url", "")  # URL of the request
            
            print(f"Request URL: {url}")
            print("Request Headers:", request_headers)
            if post_data:
                print("POST Payload:", post_data)

        # Capture response details
        elif method == "Network.responseReceived":
            response = message.get("params", {}).get("response", {})
            response_headers = response.get("headers", {})
            url = response.get("url", "")  # URL of the response
            print(f"Response URL: {url}")
            print("Response Headers:", response_headers)

        print("Method:", method)
        print("--------------------------------------")

    except Exception as e:
        print("Error processing entry:", e)

# Clean up
driver.quit()
