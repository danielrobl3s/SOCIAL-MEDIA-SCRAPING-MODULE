from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time

#Create the web driver to GET request this facebook page:
website = 'https://www.facebook.com/POSTADurango'
driver = webdriver.Chrome()
driver.get(website)

#We make driver wait until all elements are on screen

driver.implicitly_wait(60) #wait 60 seconds or until everything is found

#Get email and password from the facebook login popup to later send them
try:
    email = driver.find_element(By.XPATH, '//input[@class="x1i10hfl xggy1nq x1s07b3s x1kdt53j x1a2a7pz xjbqb8w x76ihet xwmqs3e x112ta8 xxxdfa6 x9f619 xzsf02u x1uxerd5 x1fcty0u x132q4wb x1a8lsjc x1pi30zi x1swvt13 x9desvi xh8yej3 x15h3p50 x10emqs4"]').send_keys("dudedeveloper08@gmail.com")
    pw = driver.find_element(By.XPATH, '//input[@type="password"]')
    login = driver.find_element(By.XPATH, '//div[@class="x1n2onr6 x1ja2u2z x78zum5 x2lah0s xl56j7k x6s0dn4 xozqiw3 x1q0g3np xi112ho x17zwfj4 x585lrc x1403ito x972fbf xcfux6l x1qhh985 xm0m39n x9f619 xn6708d x1ye3gou xtvsq51 x1fq8qgq"]').send_keys("Este es el correo del dude developer 89")
    login.click()
    time.sleep(5)
except:
    print("Algo salio mal, revisa que los elementos si sean interactivos")

print(driver.current_url)

