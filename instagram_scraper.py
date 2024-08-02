
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import csv
import time
import re

username = 'dudedeveloper08@gmail.com'
password = 'Obaboyamamamama0987654321'

total_titles = []
total_likes = []
comments = []
prefix = 'https://www.instagram.com/'

#function to try and get the comments:
def get_comments(driver):
    
    try:
        comment = driver.find_elements(By.XPATH, '//ul[@class="_a9ym"]')
        comments = len(comment)
    except:
        comments = '0'

    return comments

def get_likes(driver):
    
    try:
        like = driver.find_element(By.XPATH, '//span[@class="x193iq5w xeuugli x1fj9vlw x13faqbe x1vvkbs xt0psk2 x1i0vuye xvs91rp x1s688f x5n08af x10wh9bi x1wdrske x8viiok x18hxmgj"]').text
    except:
        like = '0'

    likes_pattern = re.compile(r'^\d+ likes$')
    if likes_pattern.match(like):
        like = like.replace(' likes', '')

    return like

#Create the web driver to GET request this instagram page https://www.instagram.com/postadurango:
website = prefix + input('Introduce el nombre de la pagina de instagram: ')
name = input('nombra tu archivo .csv: ')

chrome_options = webdriver.ChromeOptions()
prefs = {"profile.default_content_setting_values.notifications" : 2}
chrome_options.add_experimental_option("prefs",prefs)
driver = webdriver.Chrome(options=chrome_options)
driver.get(website)

#We make driver wait until all elements are on screen
time.sleep(10)

login_button = driver.find_element(By.XPATH, '//div[@class="x9f619 xjbqb8w x78zum5 x168nmei x13lgxp2 x5pf9jr xo71vjh x1d52u69 x1n2onr6 x1plvlek xryxfnj x1c4vz4f x2lah0s xdt5ytf xqjyukv x1qjc9v5 x1oa3qoh x1nhvcw1"][1]/a')
login_button.click()

time.sleep(5)

username = driver.find_element(By.XPATH, '//input[@type="text"]').send_keys(username)
password = driver.find_element(By.XPATH, '//input[@type="password"]').send_keys(password)

submit_button = driver.find_element(By.XPATH, '//button[@class=" _acan _acap _acas _aj1- _ap30"]')
submit_button.click()

time.sleep(10)

not_now_button = driver.find_element(By.XPATH, '//div[@role="button"]')
not_now_button.click()

time.sleep(10)

links = driver.find_elements(By.XPATH, '//div[@style="display: flex; flex-direction: column; padding-bottom: 0px; padding-top: 0px; position: relative;"]//div/a')


for link in links:
    link.click()
    title = driver.find_element(By.XPATH, '//div[@class="_a9zs"]').text
    total_titles.append(title)
    like = get_likes(driver)
    total_likes.append(like)
    comment = get_comments(driver)
    comments.append(comment)

    go_back = driver.find_element(By.XPATH, '//div[@class="x160vmok x10l6tqk x1eu8d0j x1vjfegm"]//div//div')
    go_back.click()
    time.sleep(3)

print(total_titles)
print(total_likes)
print(comments)

with open(f'{name}.csv', 'w', encoding='utf-8') as file:
    fieldnames = ['Title', 'Likes', 'Comments']
    writer = csv.DictWriter(file, fieldnames=fieldnames)
    writer.writeheader()

    for data in zip(total_titles, total_likes, comments):
        writer.writerow({"Title": data[0], "Likes": data[1], "Comments": data[2]})