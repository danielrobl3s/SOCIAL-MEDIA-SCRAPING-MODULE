from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import csv
import time

username = 'dudedeveloper08@gmail.com'
password = 'Obaboyamamamama0987654321'

total_titles = []
total_likes = []
comments = []

#Create the web driver to GET request this instagram page https://www.instagram.com/postadurango:
website = input('Introduce el link de la pagina de instagram: ')
name = input('nombra tu archivo .csv: ')
driver = webdriver.Chrome()
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

time.sleep(60)

links = driver.find_elements(By.XPATH, '//div[@class="_ac7v xzboxd6 xras4av xgc1b0m"]/div/a')

for link in links:
    link.click()
    title = driver.find_element(By.XPATH, '//span[@class="_ap3a _aaco _aacu _aacx _aad7 _aade"]//span[@class="_ap3a _aaco _aacu _aacx _aad7 _aade"]').text
    total_titles.append(title)
    like = driver.find_element(By.XPATH, '//div[@class="x1i10hfl xjbqb8w x1ejq31n xd10rxx x1sy0etr x17r0tee x972fbf xcfux6l x1qhh985 xm0m39n x9f619 x1ypdohk xt0psk2 xe8uvvx xdj266r x11i5rnm xat24cr x1mh8g0r xexx8yu x4uap5 x18d9i69 xkhd6sd x16tdsg8 x1hl2dhg xggy1nq x1a2a7pz"]//span[@class="html-span xdj266r x11i5rnm xat24cr x1mh8g0r xexx8yu x4uap5 x18d9i69 xkhd6sd x1hl2dhg x16tdsg8 x1vvkbs"]').text
    total_likes.append(like)
    comment = driver.find_element(By.XPATH, '//div[@class="x9f619 xjbqb8w x78zum5 x168nmei x13lgxp2 x5pf9jr xo71vjh x1xmf6yo x1uhb9sk x1plvlek xryxfnj x1c4vz4f x2lah0s xdt5ytf xqjyukv x1qjc9v5 x1oa3qoh x1nhvcw1"]/span[@class="x1lliihq x1plvlek xryxfnj x1n2onr6 x193iq5w xeuugli x1fj9vlw x13faqbe x1vvkbs x1s928wv xhkezso x1gmr53x x1cpjm7i x1fgarty x1943h6x x1i0vuye x1fhwpqd xo1l8bm x5n08af x1s3etm8 x676frb x10wh9bi x1wdrske x8viiok x18hxmgj"]').text
    comments.append(comment)
    go_back = driver.find_element(By.XPATH, '//div[@class="x10l6tqk x1nc75zl xi3dyvs x1mywscw"]/div')
    go_back.click()
    time.sleep(3)

with open(f'{name}.csv', 'w', encoding='utf-8') as file:
    fieldnames = ['Title', 'Likes', 'Comments']
    writer = csv.DictWriter(file, fieldnames=fieldnames)
    writer.writeheader()

    for data in zip(total_titles, total_likes, comments):
        writer.writerow({"Title": data[0], "Likes": data[1], "Comments": data[2]})