#tiktok scraper:

import requests
import psycopg2
from psycopg2 import sql
import sys

#Get posts from user from tiktok
def get_posts(username):
   
   #Call to the api on rapid api website

    url = f"https://tiktok-scrapper-videos-music-challenges-downloader.p.rapidapi.com/user/{username}/feed"

    headers = {
	    "x-rapidapi-key": "b95c5263e0mshe2fa1ab69050b63p1e7eb9jsn901e0bb5bc41",
	    "x-rapidapi-host": "tiktok-scrapper-videos-music-challenges-downloader.p.rapidapi.com"
    }

    response = requests.get(url, headers=headers)

    data = response.json()

    for post in data['data']['aweme_list']:
        print(post['aweme_id'], post['desc'], post['statistics']['digg_count'], post['statistics']['comment_count'], post['region'])


#Get user stats from tiktok
def get_user(username):

    url = "https://tiktok-scraper2.p.rapidapi.com/user/info"

    querystring = {"user_name":f"{username}"}

    headers = {
	    "x-rapidapi-key": "b95c5263e0mshe2fa1ab69050b63p1e7eb9jsn901e0bb5bc41",
	    "x-rapidapi-host": "tiktok-scraper2.p.rapidapi.com"
    }

    response = requests.get(url, headers=headers, params=querystring)

    userData = response.json()

    secuid = userData['user']['secUid']
    user_id = userData['user']['id']
    user = userData['user']['nickname']
    follower_count = userData['stats']['followerCount']
    profile_link = f"https://tiktok.com/@{username}"

    print(secuid, user_id, user, follower_count, profile_link)


if __name__ == "__main__":
    #get_user('losdelnido')
    get_posts('losdelnido')