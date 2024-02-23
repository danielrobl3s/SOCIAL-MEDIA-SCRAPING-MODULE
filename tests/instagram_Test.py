from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time

username = 'dudedeveloper08@gmail.com'
password = 'Obaboyamamamama0987654321'

#Create the web driver to GET request this facebook page:
website = 'https://www.instagram.com/postadurango/'
driver = webdriver.Chrome()
driver.get(website)

#We make driver wait until all elements are on screen

driver.implicitly_wait(60) #wait 60 seconds or until everything is found

login_button = driver.find_element(By.XPATH, '//a[@class="x1i10hfl xjqpnuy xa49m3k xqeqjp1 x2hbi6w x972fbf xcfux6l x1qhh985 xm0m39n xdl72j9 x2lah0s xe8uvvx xdj266r x11i5rnm xat24cr x1mh8g0r x2lwn1j xeuugli xexx8yu x18d9i69 x1hl2dhg xggy1nq x1ja2u2z x1t137rt x1q0g3np x1lku1pv x1a2a7pz x6s0dn4 xjyslct x1lq5wgf xgqcy7u x30kzoy x9jhf4c x1ejq31n xd10rxx x1sy0etr x17r0tee x9f619 x9bdzbf x1ypdohk x1f6kntn xwhw2v2 x10w6t97 xl56j7k x17ydfre x1swvt13 x1pi30zi x1n2onr6 x2b8uid xlyipyv x87ps6o x14atkfc xcdnw81 x1i0vuye x1tu34mt xzloghq xe81s16 x3nfvp2"]')
login_button.click()

time.sleep(5)

username = driver.find_element(By.XPATH, '//input[@type="text"]').send_keys(username)
password = driver.find_element(By.XPATH, '//input[@type="password"]').send_keys(password)

submit_button = driver.find_element(By.XPATH, '//button[@class=" _acan _acap _acas _aj1- _ap30"]')
submit_button.click()

time.sleep(10)

not_now_button = driver.find_element(By.XPATH, '//div[@role="button"]')
not_now_button.click()

time.sleep(30)