from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from browsermobproxy import Server
from csv import DictReader
from selenium.webdriver import ActionChains
import random, time, zipfile, json
from selenium_stealth import stealth

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
   def get(url='https://google.com', headless=False, proxy=False, capture_har=False, cookies=False, cookies_fb=False,
           scroll=False):
        options = Options()
        
        if headless:
            options.add_argument("--headless=chrome")

        options.add_argument("--start-maximized")
        viewport = random.choice(['2560,1440', '1920,1080', '1536,864'])
        options.add_argument("--window-size="+viewport)
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option('useAutomationExtension', False)

        browsermob_proxy = None
        if capture_har:
            server = Server("browsermob-proxy-2.1.4/bin/browsermob-proxy")
            server.start()
            browsermob_proxy = server.create_proxy()
            options.add_argument(f'--proxy-server={browsermob_proxy.proxy}')
            options.add_argument('--ignore-certificate-errors') 
            options.add_argument('--disable-web-security') 

        elif proxy:
            if not isinstance(proxy, list):
                raise Exception("Proxy needs to be a list")
            if len(proxy) in [2, 4]:
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

        stealth(driver, languages=['en-US', 'en', 'de-DE', 'de'], vendor='Google Inc.', platform='x64', webgl_vendor=w_vendor, renderer=render, fix_hairline=True)

        if capture_har:
            browsermob_proxy.new_har("test", options={'captureHeaders': True, 'captureContent': True})

        driver.get(url)

        time.sleep(5)

        if cookies:
            cookies_ = Driver.get_user_cookies_values('tiktok_session.csv')

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
            for _ in range(25):  
                actions.send_keys('\ue00f').perform() 
                time.sleep(1)

        print("Go 'head and pass the captcha")
        time.sleep(60)
        print('Now!')

        if capture_har:
            har = browsermob_proxy.har

            result = json.dumps(har, indent=2)

            file = "params.json"
            with open(file, "w") as f:
                f.write(result)
            server.stop()

            return driver, file


        return driver