from bs4 import BeautifulSoup
import requests

website='https://www.facebook.com/POSTADurango'
response = requests.get(website)
content = response.text

soup = BeautifulSoup(content, 'lxml')
bdy = soup.find('body')
print(bdy.prettify())


from facebook_scraper import get_posts

posts = get_posts('POSTA Durango', pages= 10)

for post in posts:
    print(post)




