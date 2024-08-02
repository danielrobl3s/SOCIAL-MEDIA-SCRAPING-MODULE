from selenium import webdriver
from selenium_stealth import stealth
import time

options = webdriver.ChromeOptions()
driver = webdriver.Chrome(options=options)

stealth(driver,
        languages=["en-US", "en"],
        vendor="Google Inc.",
        platform="Win32",
        webgl_vendor="Intel Inc.",
        renderer="Intel Iris OpenGL Engine",
        fix_hairline=True,
       )

driver.get("https://www.tiktok.com/@losdelnido")

time.sleep(400)
