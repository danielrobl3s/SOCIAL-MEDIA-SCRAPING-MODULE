from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from csv import DictReader
import random, time, zipfile, json
from selenium_stealth import stealth
from mitmproxy import http, ctx
import time
import subprocess

class CaptureTraffic:
    def __init__(self):
        self.counter = 0

    def response(self, flow: http.HTTPFlow) -> None:
        
        self.counter += 1
        filename = f"response_{self.counter}.json"
        with open(filename, "w") as f:
            f.write(flow.response.text)
        ctx.log.info(f"Saved response to {filename}")


def start_mitmproxy():

    mitmproxy_process = subprocess.Popen([
        "mitmdump", "-s", __file__ 
    ])
    time.sleep(5)
    return mitmproxy_process

class Driver:
   
   @staticmethod
   def get_user_cookies_values(file):
    with open(file, encoding='utf-8') as f:
        dict_reader = DictReader(f)
        list_of_dicts = list(dict_reader)
   
    return list_of_dicts
   
   
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
   def get(url='https://google.com', headless=False, proxy=False, capture=False, cookies=False):
        options = Options()
        
        if headless:
            options.add_argument("--headless=chrome")

        options.add_argument("--start-maximized")
        viewport = random.choice(['2560,1440', '1920,1080', '1536,864'])
        options.add_argument("--window-size="+viewport)
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option('useAutomationExtension', False)

        prox = "http://127.0.0.1:8080"

        if capture:
             mitmproxy_process = start_mitmproxy()
             options.add_argument(f"--proxy-server=http://{proxy}")

        elif proxy:
            if not isinstance(proxy, list):
                raise Exception("Proxy needs to be a list")
            if len(proxy) in [2, 4]:
                options.add_extension(Driver.get_proxy(proxy))
            else:
                raise Exception("Invalid proxy list")

        driver_service = Service('chromedriver-win64/chromedriver.exe')
        driver = webdriver.Chrome(options=options, service=driver_service)

        if random.randint(0, 1) == 1:
            w_vendor = 'Intel Inc.'
            render = 'Intel Iris OpenGL Engine'
        else:
            w_vendor = 'Google Inc. (Apple)'
            render = 'ANGLE (Apple, ANGLE Metal Renderer: Apple M2, Unspecified Version)'

        stealth(driver, languages=['en-US', 'en', 'de-DE', 'de'], vendor='Google Inc.', platform='x64', webgl_vendor=w_vendor, renderer=render, fix_hairline=True)


        driver.get(url)

        if cookies:
            cookies_ = Driver.get_user_cookies_values('tiktok_session.csv')

            for i in cookies_:
                 driver.add_cookie(i)
            
            driver.refresh()

        print("Go 'head and pass the captcha")
        time.sleep(60)
        print('Now!')

        if capture:
            driver.quit()
            mitmproxy_process.terminate()


        return driver