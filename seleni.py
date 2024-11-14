from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import mitmproxy.ctx
from mitmproxy import ctx
import json
import time
import subprocess
import os
import random
from csv import DictReader, DictWriter

# Custom mitmproxy addon to capture requests
class RequestCapture:
    def __init__(self):
        self.captured_requests = []
    
    def request(self, flow):
        request_data = {
            'url': flow.request.pretty_url,
            'method': flow.request.method,
            'headers': dict(flow.request.headers),
            'params': dict(flow.request.query),
        }
        
        if flow.request.method == 'POST' and flow.request.content:
            try:
                request_data['post_data'] = flow.request.get_text()
            except:
                request_data['post_data'] = str(flow.request.content)
        
        self.captured_requests.append(request_data)
        
        with open('params.json', 'w') as f:
            json.dump(self.captured_requests, f, indent=2)


def get_user_cookies_values(file):
    with open(file, encoding='utf-8') as f:
        dict_reader = DictReader(f)
        list_of_dicts = list(dict_reader)
   
    return list_of_dicts

def setup_selenium(headless=False, cookies=False, cookies_fb=False):
    options = Options()
    options.add_argument('--proxy-server=http://127.0.0.1:8080')
    
    # Create driver
    service = Service('chromedriver-mac-arm64/chromedriver')  # Update path
    driver = webdriver.Chrome(service=service, options=options)
    
    return driver

    

def start_mitmproxy():
    print("Starting mitmproxy...")
    mitmproxy_proc = subprocess.Popen(['mitmdump', '-s', 'request_capture.py'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    return mitmproxy_proc

def stop_mitmproxy(mitmproxy_proc):
    print("Stopping mitmproxy...")
    mitmproxy_proc.terminate()
    mitmproxy_proc.wait()

def main():
    mitmproxy_proc = start_mitmproxy()
    
    try:
        driver = setup_selenium(cookies_fb=True)
        driver.get('https://www.facebook.com')

        time.sleep(10)
        
        # Wait for page load
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, "body"))
        )
        
        # Give some time for requests to be captured
        time.sleep(10)
        
    except Exception as e:
        print(f"An error occurred: {e}")
    
    finally:
        stop_mitmproxy(mitmproxy_proc)

if __name__ == "__main__":
    main()