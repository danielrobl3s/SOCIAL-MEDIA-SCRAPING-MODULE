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

username = 'dudedeveloper08@gmail.com'
password = 'Este es el correo del dude developer 89'
prefix = 'https://www.facebook.com/'
texts = []
images = []

#Scroll function
def scroll():
    scroll_origin = ScrollOrigin.from_viewport(10, 10)

    ActionChains(driver)\
        .scroll_from_origin(scroll_origin, 0, 10000)\
        .perform()

#Create the web driver to GET request this facebook page:
website = prefix + input('Introduce the website to be scraped: ')
name = input('Name your csv file: ')

chrome_options = webdriver.ChromeOptions()
prefs = {"profile.default_content_setting_values.notifications" : 2}
chrome_options.add_experimental_option("prefs",prefs)
driver = webdriver.Chrome(options=chrome_options)
driver.get(website)

#We make driver wait until all elements are on screen

driver.implicitly_wait(60) #wait 60 seconds or until everything is found


#Get email and password from the facebook login popup to later send them
email = driver.find_element(By.XPATH, '//input[@type="text"]').send_keys(username)
pw = driver.find_element(By.XPATH, '//label[@aria-label="Contraseña"]/input').send_keys(password)
time.sleep(5)
login = driver.find_element(By.XPATH, '//div[@class="x1n2onr6 x1ja2u2z x78zum5 x2lah0s xl56j7k x6s0dn4 xozqiw3 x1q0g3np xi112ho x17zwfj4 x585lrc x1403ito x972fbf xcfux6l x1qhh985 xm0m39n x9f619 xn6708d x1ye3gou xtvsq51 x1fq8qgq"]')
login.click()

timeline = driver.find_elements(By.XPATH, '//div[@data-pagelet="ProfileTimeline"]')
time.sleep(10)

for element in timeline:
    print(element.text)




""" soup = BeautifulSoup(driver.page_source, 'html.parser')

posts = driver.find_elements(By.XPATH, '//div[@class="xdj266r x11i5rnm xat24cr x1mh8g0r x1vvkbs x126k92a"]')
titles = [element.text for element in posts]

reacts = driver.find_elements(By.XPATH, '//span[(@aria-hidden) and (@class="xrbpyxo x6ikm8r x10wlt62 xlyipyv x1exxlbk")]')
reactions = [element.text for element in reacts]

parent_div = driver.find_elements(By.XPATH, '//div[@class="x9f619 x1n2onr6 x1ja2u2z x78zum5 x2lah0s x1qughib x1qjc9v5 xozqiw3 x1q0g3np xykv574 xbmpl8g x4cne27 xifccgj"]')

for parent in parent_div:
   
   try:
    text_span = parent.find_elements(By.XPATH, './/span[@class="x193iq5w xeuugli x13faqbe x1vvkbs x1xmvt09 x1lliihq x1s928wv xhkezso x1gmr53x x1cpjm7i x1fgarty x1943h6x xudqn12 x3x7a5m x6prxxf xvq8zen xo1l8bm xi81zsa"]')
    for element in text_span:
       texts.append(element.text)
   except:
        texts.append('0')

   try:
    image_tag = parent.find_elements(By.XPATH, './/i')
    for element in image_tag:
         images.append(element.get_attribute("style"))
   except:
      images.append("No element")

print(titles, reactions, texts, images, len(titles), len(reactions), len(texts), len(images))

shares = []
comments = texts[::2]

index = 0
for comment in texts:    
    if index%2 != 0:
        shares.append(comment)
    index += 1

with open(f'{name}.csv', 'w', newline='', encoding='utf-8') as csvfile:
    fieldnames = ['Title', 'Likes', 'Comments', 'Shares']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()    

    for data in zip(titles, reactions, comments, shares):
        writer.writerow({"Title": data[0], "Likes": data[1], "Comments": data[2], "Shares": data[3]})
 """