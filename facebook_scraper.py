import requests
from cdriver import Driver
import time




driver = Driver.get("https://facebook.com/elbebeto.com.mx", capture_har=True)
print(driver.page_source)