from selenium import webdriver

website = 'https://www.adamchoi.co.uk/overs/detailed'
driver = webdriver.Chrome()
driver.get(website)

driver.quit()

