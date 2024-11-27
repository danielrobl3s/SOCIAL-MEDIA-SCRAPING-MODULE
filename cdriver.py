from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver import ActionChains
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import subprocess
from mitmproxy import ctx
import json
from csv import DictReader

import random, time, zipfile
from selenium_stealth import stealth


class Driver:

   @staticmethod
   def get_proxy(proxy):
      manifest_json = """
        {
            "version": "1.2.6",
            "manifest_version": 2,
            "name": "chemaExtension",
            "permissions": [
                "proxy",
                "tabs",
                "unlimitedStorage",
                "storage",
                "<all_urls>",
                "webRequest",
                "webRequestBlocking"
            ],
            "background": {
                "scripts": ["background.js"]
            },
            "minimum_chrome_version":"22.0.1"
        }
        """
      if len(proxy) == 4:
            background_js = """
            var config = {
                    mode: "fixed_servers",
                    rules: {
                    singleProxy: {
                        scheme: "http",
                        host: "%s",
                        port: parseInt(%s)
                    },
                    bypassList: ["localhost"]
                    }
                };

            chrome.proxy.settings.set({value: config, scope: "regular"}, function() {});

            function callbackFn(details) {
                return {
                    authCredentials: {
                        username: "%s",
                        password: "%s"
                    }
                };
            }

            chrome.webRequest.onAuthRequired.addListener(
                        callbackFn,
                        {urls: ["<all_urls>"]},
                        ['blocking']
            );
            """ % (proxy[0], proxy[1], proxy[2], proxy[3])
      elif len(proxy) == 2:
                    background_js = """
            var config = {
                    mode: "fixed_servers",
                    rules: {
                    singleProxy: {
                        scheme: "http",
                        host: "%s",
                        port: parseInt(%s)
                    },
                    bypassList: ["localhost"]
                    }
                };

            chrome.proxy.settings.set({value: config, scope: "regular"}, function() {});
            """ % (proxy[0], proxy[1])
      else:
            raise Exception("Invalid proxy list length...")
           
      pluginfile = "proxy_auth_plugin.zip"

      with zipfile.ZipFile(pluginfile, "w") as zp:
             zp.writestr("manifest.json", manifest_json)
             zp.writestr("background.js", background_js)

      return pluginfile
   
   @staticmethod
   def get_user_cookies_values(file):
    with open(file, encoding='utf-8') as f:
        dict_reader = DictReader(f)
        list_of_dicts = list(dict_reader)
   
    return list_of_dicts
   

   @staticmethod
   def get(url='https://google.com', headless=False, proxy=False, scroll=False, cookies_fb=False, cookies_tk=False, capture_traffic=False):
      
      capabilities = DesiredCapabilities.CHROME

      capabilities["goog:loggingPrefs"] = {"performance": "ALL"}
      
      options = Options()
      
      if headless:
         options.add_argument("--headless=chrome")

      options.add_argument("--start-maximized")
      viewport = random.choice(['2560,1440', '1920,1080', '1536,864'])
      options.add_argument("--window-size="+viewport)
      options.add_experimental_option("excludeSwitches", ["enable-automation"])
      options.add_experimental_option('useAutomationExtension', False)

      options.add_argument("--enable-logging")
      options.add_argument("--v=1")
      options.set_capability("goog:loggingPrefs", {"performance": "ALL", "browser": "ALL"})

        
      if proxy:
         if type(proxy != list):
            raise Exception("Proxy needs to be a list")
         if len(proxy) == 2 or len(proxy) == 4:
            options.add_extension(Driver.get_proxy(proxy))

         else:
            raise Exception("Invalid proxy list")
         

      driver_service = Service('chromedriver-mac-x64/chromedriver')
      driver = webdriver.Chrome(options=options, service=driver_service)

      
      if random.randint(0, 1) == 1:
           w_vendor = 'Intel Inc.'
           render = 'Intel Iris OpenGL Engine'
      else:
           w_vendor = 'Google Inc. (Apple)'
           render = 'ANGLE (Apple, ANGLE Metal Renderer: Apple M2, Unspecified Version)'

      stealth(driver, languages=['en-US', 'en', 'de-DE', 'de'], vendor='Google Inc.', platform='x64', webgl_vendor= w_vendor, renderer=render, fix_hairline=True)
      driver.get(url)

      time.sleep(random.uniform(0.4, 0.8))

      if cookies_tk:
            cookies_ = Driver.get_user_cookies_values('/Users/postadurango/Desktop/social_media_scraping/tiktok_session.csv')

            for i in cookies_:
                 driver.add_cookie(i)
            
            driver.refresh()
            
      if cookies_fb:
            cookies_fb_ = Driver.get_user_cookies_values('facebook_cookies.csv')

            for i in cookies_fb_:
                 driver.add_cookie(i)

            driver.refresh()

      if scroll:
            actions = ActionChains(driver)
            for _ in range(50):  
                actions.send_keys('\ue00f').perform() 
                time.sleep(1)
      
      if capture_traffic:
            
            # Fetch performance logs
            log_entries = driver.get_log("performance")

            traffic_data = []  # List to hold all captured traffic entries

            # Extract headers, payloads, URLs, and other details
            for entry in log_entries:
                try:
                    obj_serialized = entry.get("message")
                    obj = json.loads(obj_serialized)
                    message = obj.get("message")
                    method = message.get("method")

                    # Initialize a dictionary for the current traffic entry
                    traffic_entry = {"method": method}

                    # Capture request details
                    if method == "Network.requestWillBeSent":
                        params = message.get("params", {})
                        request = params.get("request", {})
                        request_headers = request.get("headers", {})
                        post_data = request.get("postData", None)  # Contains POST payload if available
                        url = request.get("url", "")  # URL of the request

                        traffic_entry["type"] = "request"
                        traffic_entry["url"] = url
                        traffic_entry["headers"] = request_headers
                        traffic_entry["payload"] = post_data

                    # Capture response details
                    elif method == "Network.responseReceived":
                        response = message.get("params", {}).get("response", {})
                        response_headers = response.get("headers", {})
                        url = response.get("url", "")  # URL of the response

                        traffic_entry["type"] = "response"
                        traffic_entry["url"] = url
                        traffic_entry["headers"] = response_headers

                    # Append the entry to the traffic data list
                    traffic_data.append(traffic_entry)

                except Exception as e:
                    print("Error processing entry:", e)

            # Write the captured traffic data to a JSON file
            try:
                with open("params.json", "w") as outfile:
                    json.dump(traffic_data, outfile, indent=4)
                print("Traffic data successfully written to 'traffic_data.json'")
            except Exception as e:
                print("Error writing to JSON file:", e)

            return driver
      return driver
   
