from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver import ActionChains
import subprocess
from mitmproxy import ctx
import json
from csv import DictReader

import random, time, zipfile
from selenium_stealth import stealth

class RequestCapture:
    def __init__(self):
        self.captured_requests = []
    
    def capture_request(self, request):
        # Capture request details
        request_data = {
            'url': request.url,
            'method': request.method,
            'headers': dict(request.headers),
            'params': dict(request.params),
        }

        if request.method == 'POST' and request.body:
            try:
                request_data['post_data'] = request.body.decode()
            except:
                request_data['post_data'] = str(request.body)
        
        # Add initial request data to captured list
        captured_request = {'request': request_data}
        self.captured_requests.append(captured_request)
        return len(self.captured_requests) - 1  # Return index to match with the response later
    
    def capture_response(self, response, request_index):
        # Capture response details
        response_data = {
            'status_code': response.status_code,
            'headers': dict(response.headers),
        }

        try:
            response_data['content'] = response.text
        except:
            response_data['content'] = str(response.content)
        
        # Merge response into the corresponding request entry
        self.captured_requests[request_index]['response'] = response_data
        
        # Write to params.json
        with open('params.json', 'w') as f:
            json.dump(self.captured_requests, f, indent=2)




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
   def start_mitmproxy():
       print("Starting mitmproxy...")
       mitmproxy_proc = subprocess.Popen(['mitmdump', '-s', 'request_capture.py'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
       return mitmproxy_proc
   
   @staticmethod
   def stop_mitmproxy(mitmproxy_proc):
       print("Stopping mitmproxy...")
       mitmproxy_proc.terminate()
       mitmproxy_proc.wait()

   @staticmethod
   def get(url='https://google.com', headless=False, proxy=False, scroll=False, cookies_fb=False, cookies_tk=False, capture_traffic=False):
      options = Options()
      
      if headless:
         options.add_argument("--headless=chrome")

      options.add_argument("--start-maximized")
      viewport = random.choice(['2560,1440', '1920,1080', '1536,864'])
      options.add_argument("--window-size="+viewport)
      options.add_experimental_option("excludeSwitches", ["enable-automation"])
      options.add_experimental_option('useAutomationExtension', False)

      if capture_traffic:
        mitmproxy_proc = Driver.start_mitmproxy()
        options.add_argument('--proxy-server=http://127.0.0.1:8080')     

      elif proxy:
         if type(proxy != list):
            raise Exception("Proxy needs to be a list")
         if len(proxy) == 2 or len(proxy) == 4:
            options.add_extension(Driver.get_proxy(proxy))

         else:
            raise Exception("Invalid proxy list")
         

      driver_service = Service('chromedriver-mac-arm64/chromedriver')
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

            file = "params.json"

            Driver.stop_mitmproxy(mitmproxy_proc)

            return driver, file
      return driver
   
