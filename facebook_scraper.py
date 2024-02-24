from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.actions.wheel_input import ScrollOrigin
from bs4 import BeautifulSoup
import csv
import re
import time

username = 'dudedeveloper08@gmail.com'
password = 'Este es el correo del dude developer 89'
text = ''

#Create the web driver to GET request this facebook page:
website = input('Introduce the website to be scraped: ')
name = input('Name your csv file: ')
driver = webdriver.Chrome()
driver.get(website)

#We make driver wait until all elements are on screen

driver.implicitly_wait(60) #wait 60 seconds or until everything is found


#Get email and password from the facebook login popup to later send them
email = driver.find_element(By.XPATH, '//input[@class="x1i10hfl xggy1nq x1s07b3s x1kdt53j x1a2a7pz xjbqb8w x76ihet xwmqs3e x112ta8 xxxdfa6 x9f619 xzsf02u x1uxerd5 x1fcty0u x132q4wb x1a8lsjc x1pi30zi x1swvt13 x9desvi xh8yej3 x15h3p50 x10emqs4"]').send_keys(username)
pw = driver.find_element(By.XPATH, '//input[(@aria-invalid="false") and (@name="pass")]').send_keys(password)
login = driver.find_element(By.XPATH, '//div[@class="x1c436fg"]/div[(@aria-label="Accessible login button") and (@role="button")]')
login.click()

time.sleep(30)

soup = BeautifulSoup(driver.page_source, 'html.parser')
 
posts = driver.find_elements(By.XPATH, '//div[@data-pagelet="ProfileTimeline"]/div//div[@class="x1iorvi4 x1pi30zi x1l90r2v x1swvt13"]/*')
titles = [element.text for element in posts]


reacts = driver.find_elements(By.XPATH, '//div[@class="x6s0dn4 xi81zsa x78zum5 x6prxxf x13a6bvl xvq8zen xdj266r xktsk01 xat24cr x1d52u69 x889kno x4uap5 x1a8lsjc xkhd6sd xdppsyt"]//span[@class="xt0b8zv x1e558r4"]')
reactions = [element.text for element in reacts]

comments_and_shares = driver.find_elements(By.XPATH, '//div[@class="x6s0dn4 xi81zsa x78zum5 x6prxxf x13a6bvl xvq8zen xdj266r xktsk01 xat24cr x1d52u69 x889kno x4uap5 x1a8lsjc xkhd6sd xdppsyt"]//div[@class="x1i10hfl x1qjc9v5 xjqpnuy xa49m3k xqeqjp1 x2hbi6w x1ypdohk xdl72j9 x2lah0s xe8uvvx x2lwn1j xeuugli x1hl2dhg xggy1nq x1t137rt x1o1ewxj x3x9cwd x1e5q0jg x13rtm0m x3nfvp2 x1q0g3np x87ps6o x1a2a7pz xjyslct xjbqb8w x13fuv20 xu3j5b3 x1q0q8m5 x26u7qi x972fbf xcfux6l x1qhh985 xm0m39n x9f619 x1heor9g xdj266r x11i5rnm xat24cr x1mh8g0r xexx8yu x4uap5 x18d9i69 xkhd6sd x1n2onr6 x16tdsg8 x1ja2u2z xt0b8zv"]')
comments_shares = [element.text for element in comments_and_shares]
shares = comments_shares[::2]

print(comments_shares, shares)

""" coments = driver.find_elements(By.XPATH, '//div[@class="x6s0dn4 xi81zsa x78zum5 x6prxxf x13a6bvl xvq8zen xdj266r xktsk01 xat24cr x1d52u69 x889kno x4uap5 x1a8lsjc xkhd6sd xdppsyt"]//div[@id=":r1nc:"]//span')
comments = [element.text for element in coments] """

""" share = driver.find_elements(By.XPATH, '(/html/body/div[1]/div/div[1]/div/div[3]/div/div/div[1]/div[1]/div/div/div[4]/div[2]/div/div[2]/div[3]/div[1]/div/div/div/div/div/div/div/div/div/div/div[2]/div/div/div[4]/div/div/div[1]/div/div[1]/div/div[2]/div[3]/span/div/div/div[1]/span')
shares = [element.text for element in share] """


with open(f'{name}.csv', 'w', newline='', encoding='utf-8') as csvfile:
    fieldnames = ['title', 'reactions', 'comments']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    

    for data in zip(titles, reactions):
        writer.writerow({"title": data[0], "reactions": data[1]})
    
