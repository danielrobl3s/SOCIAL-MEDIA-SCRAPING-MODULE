from connection_package import connect_to_nas_postgres, insert_into_table, select_from_table, update_table, delete_from_table, close_connection
from instagram import get_userid_by_username, get_user_info_by_id, get_user_posts, get_comments_by_shortcode, post_details

def connect():
   conn = connect_to_nas_postgres()
   if not conn:
      return
   else:
      return conn
   

#insert_into_table(conn, "singers", ["name", "platform_links", "genre"], ["Matisse MX", "https://www.facebook.com/matisseMxOficial, https://www.instagram.com/matisse_mx, https://tiktok.xom/@matisse_mx", "Regional mexicano, Pop, Folk"])

#id, user, follower_count, posts_count, link_profile = get_user_info_by_id("matisse_mx")


#insert_into_table(conn, "instagram_stats", ["artist_id", "username", "followers_count", "posts_count", "profile_link"], ["3", str(user), str(follower_count), str(posts_count), str(link_profile)])


   
conn = connect()


results = select_from_table(conn, "singers", "artist_id", "name = 'Andrea Nuñez' ")
id = results[0][0]

results2 = select_from_table(conn, "instagram_stats", "posts_count, username", f"artist_id= '{id}' ")

print(results2)

""" posts_count = results2[0][0]
username = results2[0][1]


userid = get_userid_by_username(username)

posts = get_user_posts(userid, 4, posts_count)

for post in posts:
   insert_into_table(conn, "ig_posts_stats", ["instagram_stats_id", "posts_count", "caption", "like_count", "comments_count", "comments", "is_video"], [post['id'], post['posts_count'], post['caption'], post['like_count'], post['comments_count'], post['comments'], post['is_video']]) """


close_connection(conn)

