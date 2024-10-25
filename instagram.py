#Instagram scraper:
import requests

x_rapidapi_key = "37d85c399fmshb52f0807513aa3ap13b12cjsne68930e15cfa"


def get_similar_users(username):

   url = f"https://instagram-scraper-20231.p.rapidapi.com/similarusers/{username}"

   headers = {
      "x-rapidapi-key": "37d85c399fmshb52f0807513aa3ap13b12cjsne68930e15cfa",
      "x-rapidapi-host": "instagram-scraper-20231.p.rapidapi.com"
   }

   response = requests.get(url, headers=headers)

   data = response.json()

   similar_users = []


   for similar_user in data['data']['edges']:
      user = {"username" : similar_user['node']['username'], "id": similar_user['node']['id'], "is_private": similar_user['node']['is_private'], "is_verified": similar_user['node']['is_verified']}
      similar_users.append(user)

   return similar_users



def post_details(code):

   url = f"https://instagram-scraper-20231.p.rapidapi.com/postdetail/{code}"

   headers = {
      "x-rapidapi-key": x_rapidapi_key,
      "x-rapidapi-host": "instagram-scraper-20231.p.rapidapi.com"
   }

   response = requests.get(url, headers=headers)
   data = response.json()

   try:
      data = data['data']['is_video']
   except:
      data = 'not found'

   return data



def get_comments_by_shortcode(code):

   users = []
   comments = []

   url = f"https://instagram-scraper-20231.p.rapidapi.com/postcomments/{code}/%7Bend_cursor%7D"

   headers = {
      "x-rapidapi-key": x_rapidapi_key,
      "x-rapidapi-host": "instagram-scraper-20231.p.rapidapi.com"
   }

   response = requests.get(url, headers=headers)
   data = response.json()

   print(data['data'])

   try:

      for comment in data['data']['comments']:
         comment_user = comment['user']['username']
         text = comment['text']

         users.append(comment_user)
         comments.append(text)
   except:
      return "No comments"

   
   return {"user_that_commented": users, 
           "comment": comments,
   }






def get_user_posts(userid, id, posts_count):

   """
   :param userid: Must be the userid from instagram
   :param id: Must be the id from the instagram_stats table not artist_id
   :param posts_count: Is the posts_count variable returned from select_from_table(conn, "instagram_stats", "posts_count, username", f"artist_id= '{id}' ")
   """

   posts = []

   url = f"https://instagram-scraper-20231.p.rapidapi.com/userposts/{userid}/12/%7Bend_cursor%7D"

   headers = {
      "x-rapidapi-key": x_rapidapi_key,
      "x-rapidapi-host": "instagram-scraper-20231.p.rapidapi.com"
   }

   response = requests.get(url, headers=headers)
   data = response.json()

   for post in data['data']['items']:
      code = post['code']
      id = id
      posts_count = posts_count

      try:
         caption = post['caption']['text']
      except:
         caption = "No caption"

      like_count = post['like_count']
      comment_count = post['comment_count']
      comments = str(get_comments_by_shortcode(code))
      is_video = str(post_details(code))
      taken_at = post['taken_at']

      posts.append({"id": id, "posts_count": posts_count, "caption": caption, "like_count": like_count, "comments_count": comment_count, "comments": comments, "is_video": is_video, "taken_at": taken_at})

   return posts




def get_user_info_by_id(username):

   id = get_userid_by_username(username)

   url = f"https://instagram-scraper-20231.p.rapidapi.com/usercontact/{id}"

   headers = {
      "x-rapidapi-key": x_rapidapi_key,
      "x-rapidapi-host": "instagram-scraper-20231.p.rapidapi.com"
   }

   response = requests.get(url, headers=headers)

   data = response.json()

   user =  data['data']['username']
   follower_count = data['data']['follower_count']
   posts_count = data['data']['media_count']
   link_profile = f"https://instagram.com/{username}"
   similar_users = get_similar_users(username)

   return id, user, follower_count, posts_count, link_profile





def get_userid_by_username(username):

   url = f"https://instagram-scraper-20231.p.rapidapi.com/userid/{username}"

   headers = {
	   "x-rapidapi-key": x_rapidapi_key,
	   "x-rapidapi-host": "instagram-scraper-20231.p.rapidapi.com"
   }

   response = requests.get(url, headers=headers)

   data = response.json()

   id = data['data']

   return id