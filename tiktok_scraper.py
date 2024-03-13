from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.actions.wheel_input import ScrollOrigin
from bs4 import BeautifulSoup
import urllib3
import csv
import re
import time

username = "dudedeveloper08@gmail.com"
password = "Obaboyamama@12"
prefix = "https://www.tiktok.com/@"
titles = []
likes = []
comments = []
saved = []

website = prefix + input('Introduce la cuenta de tiktok a la que quieres acceder: ')
name = input('Nombra tu archivo .csv: ')

chrome_options = webdriver.ChromeOptions()
prefs = {"profile.default_content_setting_values.notifications" : 2}
chrome_options.add_experimental_option("prefs",prefs)
driver = webdriver.Chrome(options=chrome_options)
driver.get(website)

#We make driver wait until all elements are on screen

time.sleep(30) #wait 60 seconds or until everything is found

#Get email and password from the facebook login popup to later send them
login_with_mail_button = driver.find_element(By.XPATH, '(//div[@class="css-7u35li-DivBoxContainer e1cgu1qo0"])[2]')
login_with_mail_button.click()

time.sleep(5)

get_email_link = driver.find_element(By.XPATH, '//a[@class="ep888o80 css-1mgli76-ALink-StyledLink epl6mg0"]')
get_email_link.click()

time.sleep(10)

email = driver.find_element(By.XPATH, '//input[@name="username"]').send_keys(username)
password = driver.find_element(By.XPATH, '//input[@type="password"]').send_keys(password)
submit = driver.find_element(By.XPATH, '//button[@data-e2e="login-button"]')
submit.click()

time.sleep(30)

posts = driver.find_elements(By.XPATH, '//div[@class="css-x6y88p-DivItemContainerV2 e19c29qe8"]')

for post in posts:
    post.click()

    title = driver.find_element(By.XPATH, '//div[@class="css-1nst91u-DivMainContent e1mecfx01"]').text
    titles.append(title)

    like = driver.find_element(By.XPATH, '//strong[@data-e2e="browse-like-count"]').text
    likes.append(like)

    comments_number = driver.find_element(By.XPATH, '//strong[@data-e2e="browse-comment-count"]').text
    comments.append(comments_number)

    saved_number = driver.find_element(By.XPATH, '//strong[@data-e2e="undefined-count"]').text
    saved.append(saved_number)

    close = driver.find_element(By.XPATH, '//button[@aria-label="Close"]')
    close.click()


with open(f'{name}.csv', 'w', encoding='utf-8') as file:
    fieldnames = ['Title', 'Likes', 'Comments', 'Saved']
    writer = csv.DictWriter(file, fieldnames=fieldnames)
    writer.writeheader()

    for data in zip(titles, likes, comments, saved):
        writer.writerow({"Title": data[0], "Likes": data[1], "Comments": data[2], "Saved": data[3]})