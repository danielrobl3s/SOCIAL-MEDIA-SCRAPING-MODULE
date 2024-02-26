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
website = 'https://www.facebook.com/Contactohoy'
driver = webdriver.Chrome()
driver.get(website)

#We make driver wait until all elements are on screen

driver.implicitly_wait(60) #wait 60 seconds or until everything is found


#Get email and password from the facebook login popup to later send them
email = driver.find_element(By.XPATH, '//input[@class="x1i10hfl xggy1nq x1s07b3s x1kdt53j x1a2a7pz xjbqb8w x76ihet xwmqs3e x112ta8 xxxdfa6 x9f619 xzsf02u x1uxerd5 x1fcty0u x132q4wb x1a8lsjc x1pi30zi x1swvt13 x9desvi xh8yej3 x15h3p50 x10emqs4"]').send_keys(username)
pw = driver.find_element(By.XPATH, '//input[(@aria-invalid="false") and (@name="pass")]').send_keys(password)
login = driver.find_element(By.XPATH, '//div[@class="x1c436fg"]/div[(@aria-label="Accessible login button") and (@role="button")]')
login.click()

time.sleep(60)


feed = driver.find_element(By.XPATH, '//div[@data-pagelet="ProfileTimeline"]')

with open('postsFB.txt', 'w', newline='', encoding='utf-8') as txtfile:
    txtfile.write(feed.text)







""" posts = driver.find_elements(By.XPATH, '//div[@style="text-align: start;"]')
titles = [element.text for element in posts]

reacts = driver.find_elements(By.XPATH, '//span[@class="x1e558r4"]')
reactions = [element.text for element in reacts]

coments = driver.find_elements(By.XPATH, '//div[@class="x9f619 x1n2onr6 x1ja2u2z x78zum5 xdt5ytf x2lah0s x193iq5w xeuugli xg83lxy x1h0ha7o x10b6aqq x1yrsyyn"]')
comments = [element.text for element in coments]

share = driver.find_elements(By.XPATH, '(//div[@class="x9f619 x1n2onr6 x1ja2u2z x78zum5 xdt5ytf x2lah0s x193iq5w xeuugli xg83lxy x1h0ha7o x10b6aqq x1yrsyyn"]//span)[position() mod 2 = 0]')
shares = [element.text for element in share]

print(shares)

with open('postsFB.csv', 'w', newline='', encoding='utf-8') as csvfile:
    fieldnames = ['title', 'reactions', 'comments', 'shares']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()

    for data in zip(titles, reactions, comments):
        writer.writerow({"title": data[0], "reactions": data[1], "comments": data[2]}) """
    
