from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.actions.wheel_input import ScrollOrigin
from bs4 import BeautifulSoup
import csv
import re
import time

username = input('Tell me your email: ')
password = input('Tell me your password: ')
text = ''

#Create the web driver to GET request this facebook page:
website = 'https://www.facebook.com/POSTADurango'
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

soup = BeautifulSoup(driver.page_source, 'html.parser')

posts = soup.find_all('div', {'style':'text-align: start;'})
#Extract text from every element of the resultset object thrown by beautiful soup
titles = [element.get_text(strip=True) for element in posts]

reacts = soup.find_all('span', {'class':'x1e558r4'})
#Extract text but from reactions resultset
reactions = [element.get_text(strip=True) for element in reacts]

comments = soup.find_all('div', {'data-visualcompletion':'ignore-dynamic', 'class':'x168nmei x13lgxp2 x30kzoy x9jhf4c x6ikm8r x10wlt62'})
shares = '' #soup.find_all('')

""" with open('test.html', 'w', encoding='utf-8') as f:
    f.write(str(reactions)) """

with open('postsFB.csv', 'w', newline='', encoding='utf-8') as csvfile:
    fieldnames = ['title', 'reactions', 'comments', 'shares']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()

    for data in zip(titles, reactions):
        writer.writerow({"title": data[0], "reactions": data[1]})
    
