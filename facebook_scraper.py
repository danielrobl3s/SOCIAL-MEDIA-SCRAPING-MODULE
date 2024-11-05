from cdriver import Driver
import requests

driver = Driver.get("https://www.facebook.com/elbebeto.com.mx", headless=True, capture=True)

print(driver.page_source)
