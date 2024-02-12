from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup

# Facebook URL of the page you want to scrape
url = "https://www.facebook.com/POSTADurango"

# Credentials
email = "your_email@example.com"
password = "your_password"

# Start a Selenium webdriver session (make sure you have chromedriver or geckodriver installed)
driver = webdriver.Chrome()  # You may need to change this path according to where your chromedriver is located
driver.get(url)

# Log in
login_button = driver.find_element(By.ID, "loginbutton")
login_button.click()

email_input = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.ID, "email")))
email_input.send_keys(email)

password_input = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.ID, "pass")))
password_input.send_keys(password)
password_input.send_keys(Keys.RETURN)

# Wait for the page to load
wait = WebDriverWait(driver, 10)
wait.until(EC.visibility_of_element_located((By.XPATH, "//div[@data-testid='post_message']")))

# Get page source
html = driver.page_source
soup = BeautifulSoup(html, "html.parser")

# Scraping example: Get all post messages
posts = soup.find_all("div", {"data-testid": "post_message"})
for post in posts:
    print(post.text)

# Close the Selenium webdriver session
driver.quit()
