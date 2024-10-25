from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
import json
import time

def get_cookies_(username):
    driver_service = Service("/Users/postadurango/Downloads/crawler/rapid api/chromedriver-mac-arm64/chromedriver")

    options = Options()
    options.add_argument('--headless')  
    options.add_argument('--disable-gpu')
    options.add_argument("--window-size=1920,1080")

    driver = webdriver.Chrome(service=driver_service, options=options)
    driver.get(f"https://tiktok.com/@{username}") 


    cookies = driver.get_cookies()
    print(cookies)

    driver.quit()

def main():
    get_cookies_("elbebeto")

# Entry point ------------->
if __name__ == "__main__":
    main()
