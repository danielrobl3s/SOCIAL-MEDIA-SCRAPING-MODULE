from fastapi import FastAPI
from connection_package import connect_to_nas_postgres, close_connection, insert_into_table, select_from_table, delete_from_table
from instagram_scraper import get_user_info_by_id, get_id_by_username, get_user_posts, get_post_comments, get_similar_users
from datetime import datetime
import pytz

app = FastAPI()

def connect():
   conn = connect_to_nas_postgres()
   if not conn:
      return
   else:
      return conn
   

def get_user_info_by_username(username):
   id, user, follower_count, posts_count, link_profile = get_user_info_by_id(username)

   return id, user, follower_count, posts_count, link_profile



@app.get("/tables/singers/insert")
async def insert_into_singers(name: str, platform_links: str, genre: str):
   """
   name: name of the artist, remember it, it will help you to use the next endpoints \n
   platform_links: links of the artist's social media \n
   genre: the genre the artist focuses on \n
   """

   conn = connect()

   insert_into_table(conn, "singers", ["name", "platform_links", "genre"], [name, platform_links, genre])

   
   return {"singer data": {"name": name, "platform_links": platform_links, "genre": genre}}



@app.get("/tables/singers/delete")
async def delete_from_singers(id: int):
   """
   id: Must be the artist_id from singers table
   """ 

   conn = connect()

   name = select_from_table(conn, "singers", "name", f"artist_id = '{id}' ")
   delete_from_table(conn, "singers", f"artist_id = '{id}'")

   close_connection(conn)

   return {"successfully deleted id: ": id, "name": name}



@app.get("/tables/instagram_stats/insert")
async def insert_into_instagram_stats(name: str, username: str ):

   """
   Name: Must be artist name on table singers, otherwise will throw SQL exception \n
   Username: Must be artist instagram username 
   """

   artist_id, user, follower_count, posts_count, link_profile = get_user_info_by_username(username)

   conn = connect()

   results = select_from_table(conn, "singers", "artist_id", f"name = '{name}' ")
   artist_id = results[0][0]

   insert_into_table(conn, "instagram_stats", ["artist_id", "username", "followers_count", "posts_count", "profile_link"], [artist_id, str(user), str(follower_count), str(posts_count), str(link_profile)])

   close_connection(conn)

   return {"instagram_stats_data": {"artist_id": artist_id, "username": user, "followers_count": follower_count, "posts_count": posts_count, "profile_link": link_profile}}


@app.get("/tables/instagram_stats/delete")
async def delete_from_instagram_stats(id: int):
   """
   id: Must be the id from instagram_stats table, (not artist_id)
   """ 

   conn = connect()

   delete_from_table(conn, "instagram_stats", f"id = '{id}'")

   close_connection(conn)

   return {"deleted successfully, id: ": id}


@app.get("/tables/ig_posts_stats/insert")
async def insert_into_ig_posts_stats(name: str):

   conn = connect()

   results = select_from_table(conn, "singers", "artist_id", f"name = '{name}' ")
   artist_id = results[0][0]

   results2 = select_from_table(conn, "instagram_stats", "posts_count, username, id", f"artist_id= '{artist_id}' ")
   posts_count = results2[0][0]
   username = results2[0][1]
   instagram_stats_id = results2[0][2]

   posts = get_user_posts(username, instagram_stats_id, posts_count)

   for post in posts:

      taken_at_datetime = datetime.fromtimestamp(post['taken_at'], tz=pytz.UTC)
      
      insert_into_table(conn, "ig_posts_stats", ["instagram_stats_id", "posts_count", "caption", "like_count", "comments_count", "comments", "is_video", "taken_at"], [post['id'], post['posts_count'], post['title'], post['likes_count'], post['comment_count'], post['comments'], post['is_video?'], taken_at_datetime])

   close_connection(conn)

   return {"Data inserted successfully my bro!"}


@app.get("/tables/ig_posts_stats/delete")
async def delete_from_ig_posts_stats(id: int):
   """
   id: Must be the instagram_stats_id from instagram_stats table
   """ 

   conn = connect()

   name = select_from_table(conn, "instagram_stats", "username", f"id = '{id}' ")
   delete_from_table(conn, "ig_posts_stats", f"instagram_stats_id = '{id}'")

   close_connection(conn)

   return {"successfully deleted all posts stats with id: ": id, "username": name}



@app.get("/utils/similarusers/insert")
async def find_similar_users(username: str):
   
   similar_users = get_similar_users(username)

   conn = connect()

   stats = select_from_table(conn, "instagram_stats", "id", f"username = '{username}' ")

   print(stats)


   for user in similar_users:
      insert_into_table(conn, "similar_users", ["instagram_stats_id", "username", "instagram_user_id", "is_private", "is_verified"], [stats[0][0], user["username"], user["id"], user["is_private"], user["is_verified"]])

   close_connection(conn)

   return {"Successfully inserted in similar_users!!"}


@app.get("/utils/similarusers/delete")
async def delete_from_similar_users(id: int):
   """
   id: Must be the instagram_stats_id as integer from instagram_stats table
   """ 

   conn = connect()

   delete_from_table(conn, "similar_users", f"instagram_stats_id = '{id}'")

   close_connection(conn)

   return {"successfully deleted all similar_users from a user with id: ": id}