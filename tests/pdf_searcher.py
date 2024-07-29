from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.actions.wheel_input import ScrollOrigin
import time
from bs4 import BeautifulSoup
import urllib3
import csv
import re
import time

#Scroll function
def scroll():
    scroll_origin = ScrollOrigin.from_viewport(10, 10)

    ActionChains(driver)\
        .scroll_from_origin(scroll_origin, 0, 10000)\
        .perform()

prefix = 'https://www.google.com/search?q='
query = input('Introduce the query to be searched: ')

website = prefix + query

chrome_options = webdriver.ChromeOptions()
prefs = {"profile.default_content_setting_values.notifications" : 2}
chrome_options.add_experimental_option("prefs",prefs)
driver = webdriver.Chrome(options=chrome_options)
driver.get(website)

time.sleep(120)





