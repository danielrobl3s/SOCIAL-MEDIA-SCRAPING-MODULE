from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time

username = 'dudedeveloper08@gmail.com' #input('Tell me your email: ')
password = 'Este es el correo del dude developer 89' #input('Tell me your password: ')

#Create the web driver to GET request this facebook page:
website = 'https://www.facebook.com/POSTADurango'
driver = webdriver.Chrome()
driver.get(website)

#We make driver wait until all elements are on screen

driver.implicitly_wait(60) #wait 60 seconds or until everything is found

try:
    #Get email and password from the facebook login popup to later send them
    email = driver.find_element(By.XPATH, '//input[@class="x1i10hfl xggy1nq x1s07b3s x1kdt53j x1a2a7pz xjbqb8w x76ihet xwmqs3e x112ta8 xxxdfa6 x9f619 xzsf02u x1uxerd5 x1fcty0u x132q4wb x1a8lsjc x1pi30zi x1swvt13 x9desvi xh8yej3 x15h3p50 x10emqs4"]').send_keys(username)
    pw = driver.find_element(By.XPATH, '//input[(@aria-invalid="false") and (@name="pass")]').send_keys(password)
    login = driver.find_element(By.XPATH, '//div[@class="x1c436fg"]/div[(@aria-label="Accessible login button") and (@role="button")]')
    login.click()

    time.sleep(20)
    feed = driver.find_element(By.XPATH, '//div[@data-pagelet="ProfileTimeline"]')
except:
    print("Algo salió mal, checa si los elementos son interactivos o si estan bien identificados")


with open('outputFB.txt', 'w', encoding='UTF-8') as f:
    f.write(feed.text)

