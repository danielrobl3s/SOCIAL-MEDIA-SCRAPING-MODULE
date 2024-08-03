from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import undetected_chromedriver as uc
from selenium_stealth import stealth
import csv
import time

options = webdriver.ChromeOptions()
driver = webdriver.Chrome(options=options)

username = "dudedeveloper08@gmail.com"
password = "Obaboyamama@12"
prefix = "https://www.tiktok.com/@"
titles = []
likes = []
comments = []
saved = []

def login_with_email():

    time.sleep(10)

    login_with_mail = driver.find_element(By.XPATH, '//div[@class="css-102dq55-DivLoginOptionContainer exd0a434"]/div[2]')
    login_with_mail.click()

    time.sleep(10)


stealth(driver,
        languages=["en-US", "en"],
        vendor="Google Inc.",
        platform="Win32",
        webgl_vendor="Intel Inc.",
        renderer="Intel Iris OpenGL Engine",
        fix_hairline=True,
       )


website = prefix + input('Introduce la cuenta de tiktok a la que quieres acceder: ')
name = input('Nombra tu archivo .csv: ')
driver.get(website)

time.sleep(20)

login_button = driver.find_element(By.XPATH, '//button[@id="header-login-button"]')
login_button.click()

time.sleep(30)

login_with_email()

get_email_link = driver.find_element(By.XPATH, '//a[@href="/login/phone-or-email/email"]')
get_email_link.click()

""" email = driver.find_element(By.XPATH, '//input[@name="username"]').send_keys(username)
password = driver.find_element(By.XPATH, '//input[@type="password"]').send_keys(password)

submit = driver.find_element(By.XPATH, '//button[@data-e2e="login-button"]')
submit.click() """

time.sleep(30)

posts = driver.find_elements(By.XPATH, '//div[@data-e2e="user-post-item-list"]/div')

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

    time.sleep(2)


with open(f'{name}.csv', 'w', encoding='utf-8') as file:
    fieldnames = ['Title', 'Likes', 'Comments', 'Saved']
    writer = csv.DictWriter(file, fieldnames=fieldnames)
    writer.writeheader()

    for data in zip(titles, likes, comments, saved):
        writer.writerow({"Title": data[0], "Likes": data[1], "Comments": data[2], "Saved": data[3]})


