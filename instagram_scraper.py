
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
    else:
        like = '0'

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

driver.implicitly_wait(20) #wait 60 seconds or until everything is found

login_button = driver.find_element(By.XPATH, '//a[@class="x1i10hfl xjqpnuy xa49m3k xqeqjp1 x2hbi6w x972fbf xcfux6l x1qhh985 xm0m39n xdl72j9 x2lah0s xe8uvvx xdj266r x11i5rnm xat24cr x1mh8g0r x2lwn1j xeuugli xexx8yu x18d9i69 x1hl2dhg xggy1nq x1ja2u2z x1t137rt x1q0g3np x1lku1pv x1a2a7pz x6s0dn4 xjyslct x1lq5wgf xgqcy7u x30kzoy x9jhf4c x1ejq31n xd10rxx x1sy0etr x17r0tee x9f619 x9bdzbf x1ypdohk x1f6kntn xwhw2v2 x10w6t97 xl56j7k x17ydfre x1swvt13 x1pi30zi x1n2onr6 x2b8uid xlyipyv x87ps6o x14atkfc xcdnw81 x1i0vuye x1tu34mt xzloghq xe81s16 x3nfvp2"]')
login_button.click()

time.sleep(5)

username = driver.find_element(By.XPATH, '//input[@type="text"]').send_keys(username)
password = driver.find_element(By.XPATH, '//input[@type="password"]').send_keys(password)

submit_button = driver.find_element(By.XPATH, '//button[@class=" _acan _acap _acas _aj1- _ap30"]')
submit_button.click()

time.sleep(3)

not_now_button = driver.find_element(By.XPATH, '//div[@role="button"]')
not_now_button.click()

time.sleep(10)

links = driver.find_elements(By.XPATH, '//div[@class="_ac7v xzboxd6 xras4av xgc1b0m"]/div/a')


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