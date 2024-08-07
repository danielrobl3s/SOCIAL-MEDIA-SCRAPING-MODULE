from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import undetected_chromedriver as uc
from selenium_stealth import stealth
import csv
import time
import re

#Function to get the title and return it, otherwise returns no title
def get_title():
    try:
        title = driver.find_element(By.XPATH, '//h1[@class="_ap3a _aaco _aacu _aacx _aad7 _aade"]').text
    except:
        title = 'No title found'
    
    return title


#function to try and retrieve comments:
def get_comments(driver):
    
    try:
        comment = driver.find_elements(By.XPATH, '//ul[@class="_a9z6 _a9za"]/div[3]/div/div/div')
        comments = len(comment)
    except:
        comments = '0'

    return comments

#Function that retrieves likes:
def get_likes(driver):
    
    try:
        like = driver.find_element(By.XPATH, '//span[@class="x193iq5w xeuugli x1fj9vlw x13faqbe x1vvkbs xt0psk2 x1i0vuye xvs91rp x1s688f x5n08af x10wh9bi x1wdrske x8viiok x18hxmgj"]').text
    except:
        like = '0'

    likes_pattern = re.compile(r'^\d+ likes$')
    if likes_pattern.match(like):
        like = like.replace(' likes', '')

    return like


username = "danielrobl3s"
password = "Don't fucking scam me 89"

total_titles = []
total_likes = []
comments = []
prefix = 'https://www.instagram.com/'
site = input('Type the instagram profile you want to scrape: ')
name = input('Name your csv file: ')

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

driver.get(prefix)

time.sleep(10)

username = driver.find_element(By.XPATH, '//input[@type="text"]').send_keys(username)
password = driver.find_element(By.XPATH, '//input[@type="password"]').send_keys(password)

time.sleep(5)

submit_button = driver.find_element(By.XPATH, '//button[@class=" _acan _acap _acas _aj1- _ap30"]')
submit_button.click()

time.sleep(10)

not_now_button = driver.find_element(By.XPATH, '//div[@role="button"]')
not_now_button.click()

time.sleep(10)

not_now_again = driver.find_element(By.XPATH, '//button[@class="_a9-- _ap36 _a9_1"]')
not_now_again.click()

time.sleep(5)

search = driver.find_element(By.XPATH, '//div[@class="x1iyjqo2 xh8yej3"]/div[2]/span')
search.click()

time.sleep(5)

input_search = driver.find_element(By.XPATH, '//input[@aria-label="Search input"]').send_keys(site)
time.sleep(4)

profile = driver.find_element(By.XPATH, '//a[@class="x1i10hfl x1qjc9v5 xjbqb8w xjqpnuy xa49m3k xqeqjp1 x2hbi6w x13fuv20 xu3j5b3 x1q0q8m5 x26u7qi x972fbf xcfux6l x1qhh985 xm0m39n x9f619 x1ypdohk xdl72j9 x2lah0s xe8uvvx xdj266r x11i5rnm xat24cr x1mh8g0r x2lwn1j xeuugli xexx8yu x4uap5 x18d9i69 xkhd6sd x1n2onr6 x16tdsg8 x1hl2dhg xggy1nq x1ja2u2z x1t137rt x1q0g3np x87ps6o x1lku1pv x1a2a7pz x1dm5mii x16mil14 xiojian x1yutycm x1lliihq x193iq5w xh8yej3"][1]')
profile.click()

time.sleep(10)

links = driver.find_elements(By.XPATH, '//div[@style="display: flex; flex-direction: column; padding-bottom: 0px; padding-top: 0px; position: relative;"]//div/a')

for link in links:
    link.click()

    time.sleep(10)

    title = get_title()
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
