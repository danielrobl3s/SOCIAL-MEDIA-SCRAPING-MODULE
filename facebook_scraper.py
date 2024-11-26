import gzip
from urllib.parse import quote
import zstandard as zstd
import zlib
import brotli
import requests
from cdriver import Driver
import time
import os
from bs4 import BeautifulSoup
from lxml import etree
import json
import re
import csv

def fix_json(json_file):
   file_path = json_file
   json_objects = []

   with open(file_path, "r") as file:
      for line in file:
         try:
               # Parse each line as a separate JSON object
               json_obj = json.loads(line.strip())
               json_objects.append(json_obj)
         except json.JSONDecodeError as e:
               print(f"Error parsing line: {e}")

   return json_objects

def catch_reactions(reactions_i):

   like_count = "not found"
   love_count = "not found"
   care_count = "not found"
   haha_count = "not found"
   surprise_count = "not found"
   sad_count = "not found"
   angry_count = "not found"

   for i in reactions_i:
      
      try:
         if i["node"]["localized_name"] == "Me gusta":

            like_count = i["reaction_count"]
      except:
         pass

      try:
         if i["node"]["localized_name"] == "Me encanta":

            love_count = i["reaction_count"]
      except:
            pass
      
      try:
         if i["node"]["localized_name"] == "Me importa":

            care_count = i["reaction_count"]
      except:
            pass

      try:

         if i["node"]["localized_name"] == "Me divierte":

            haha_count = i["reaction_count"]
      except:

            pass
      
      try:
         if i["node"]["localized_name"] == "Me asombra":

            surprise_count = i["reaction_count"]
      except:
            pass

      try:      
         if i["node"]["localized_name"] == "Me entristece":

            sad_count = i["reaction_count"]
      except:
            pass

      try:
         if i["node"]["localized_name"] == "Me enoja":

            angry_count = i["reaction_count"]
      except:
            pass

   return like_count, love_count, care_count, haha_count, surprise_count, sad_count, angry_count



def read_logs(username):
   i = range(0,51)

   pack_data = []

   for x in i:

      try:
         with open(f'{username}_output_{x}.json', 'r') as f:

            data = json.load(f)
                
            try:   
               title = data["data"]["node"]["timeline_list_feed_units"]["edges"][0]["node"]["comet_sections"]["content"]["story"]["message"]["text"]
            except:
               title = "not found"


            try:
               reactions_count = data["data"]["node"]["timeline_list_feed_units"]["edges"][0]["node"]["comet_sections"]["feedback"]["story"]["story_ufi_container"]["story"]["feedback_context"]["feedback_target_with_context"]["comet_ufi_summary_and_actions_renderer"]["feedback"]["reaction_count"]["count"]
            except:
               reactions_count = "not found"

            
            reactions_i = data["data"]["node"]["timeline_list_feed_units"]["edges"][0]["node"]["comet_sections"]["feedback"]["story"]["story_ufi_container"]["story"]["feedback_context"]["feedback_target_with_context"]["comet_ufi_summary_and_actions_renderer"]["feedback"]["top_reactions"]["edges"]

            like_count, love_count, care_count, haha_count, surprise_count, sad_count, angry_count = catch_reactions(reactions_i)

            try:   
               comments_count = data["data"]["node"]["timeline_list_feed_units"]["edges"][0]["node"]["comet_sections"]["feedback"]["story"]["story_ufi_container"]["story"]["feedback_context"]["feedback_target_with_context"]["comment_rendering_instance"]["comments"]["total_count"]
            except:
               comments_count = "not found"


            try:
               comments =  data["data"]["node"]["timeline_list_feed_units"]["edges"][0]["node"]["comet_sections"]["feedback"]["story"]["story_ufi_container"]["story"]["feedback_context"]["interesting_top_level_comments"][0]["comment"]["body"]["text"]
               user_that_commented = data["data"]["node"]["timeline_list_feed_units"]["edges"][0]["node"]["comet_sections"]["feedback"]["story"]["story_ufi_container"]["story"]["feedback_context"]["interesting_top_level_comments"][0]["comment"]["author"]["name"]

               commentz = {"user_that_commented": user_that_commented, "comment": comments}
            except:
               commentz = "not found"
            

            is_video = data["data"]["node"]["timeline_list_feed_units"]["edges"][0]["node"]["comet_sections"]["feedback"]["story"]["story_ufi_container"]["story"]["feedback_context"]["feedback_target_with_context"]["comet_ufi_summary_and_actions_renderer"]["feedback"]["video_view_count"]
            if is_video == None:
               is_video = False
            else:
               is_video = True
         
            pack_data.append({
               "title": str(title),
               "reactions_count": reactions_count,
               "like_count": like_count,
               "love_count": love_count,
               "care_count": care_count,
               "haha_count": haha_count,
               "surprise_count": surprise_count,
               "sad_count": sad_count,
               "angry_count": angry_count,
               "comments_count": comments_count,
               "comments": str(commentz),
               "is_video": is_video
            })
         

      except Exception as e:
         print("No existing file in here: "+str(e))

   return pack_data
   



def delete_file(f_path):

   # Check if the file exists before attempting to delete
   if os.path.exists(f_path):
      os.remove(f_path)
      print(f"{f_path} has been deleted successfully.")
   else:
      print(f"{f_path} does not exist, creating a new one")



def turn_numbers(number):
   if '\xa0mill.' in number[0]:
      if "seguidores" in number[0]:

         number[0] = number[0].replace("\xa0mill. seguidores", "")
         number[0] = number[0].replace(",", ".")
      else:
         number[0] = number[0].replace("\xa0mill. Me gusta")
         number[0] = number[0].replace(",", ".")

      new_number = float(number[0])
      new_number = int(new_number)

      print(new_number)

      new_number = new_number * 1000000

      return new_number

   elif '\xa0mil' in number[0]:
      if "seguidores" in number[0]:

         number[0] = number[0].replace("\xa0mil seguidores", "")
         number[0] = number[0].replace(",", ".")
      else:
         number[0] = number[0].replace("\xa0mil Me gusta", "")
         number[0] = number[0].replace(",", ".")

      new_number = float(number[0])
      new_number = int(new_number)

      print(new_number)

      new_number = new_number * 1000

      return new_number
   else:
      print(number[0])
      print("Nope")


def get_user_cookies_values(file):
    with open(file, encoding='utf-8') as f:
        dict_reader = csv.DictReader(f)
        list_of_dicts = list(dict_reader)
   
    return list_of_dicts



def get_user_posts(username):
   
   driver = Driver.get(f"https://facebook.com/{username}", capture_traffic=True, cookies_fb=True, scroll=True)
   html = driver.page_source

   with open("params.json", "r") as f:
      json_data = json.load(f)

      pack_data = []

      x = 0

      for entry in json_data:
         try:
            if str(entry['type']) == "request":
               try:
                  if str(entry['url']).startswith('https://www.facebook.com/api/graphql/'):

                     cookies_fb = get_user_cookies_values("facebook_cookies.csv")

                     cookies_fb_ = {}
                     for i in cookies_fb:
                        cookies_fb_[str(i["name"])] = str(i["value"])

                     headers = entry["headers"]
                     headers["Sec-Fetch-Site"] = "same-origin"

                     r = requests.request("POST", entry["url"], headers=headers, data=entry["payload"], cookies=cookies_fb_)

                     json_data = r.json()

                     print(json_data)

                     with open(f"ouput_link_{x}.txt", "a", newline="") as f:
                        f.write(json_data)

                     data = fix_json(f"ouput_link_{x}")

                     print(data["data"]["node"]["__typename"])


                     x += 1




               except Exception as e:
                  print(e)
                  continue
         except:
            continue


   """ rango = range(len(links))

   payload = []

   try:
      for x in rango:
         print(x)

         print(headers)

            # Convert headers to a dictionary
         header = headers[x]

         #print(links[x], header, params)

         if "Accept-Encoding" in header:
            header.pop('Accept-Encoding')
            print(header)

         print(header)
         
         response = requests.request("POST", url=links[x], headers=headers[x], data=paramets[x])
         
         json_data = json.loads(response.text)

         with open(f"{username}_output_{x}", "w", newline="") as f:
            f.write(response.text)
         
   except Exception as e: 
     print(f'something went wrong :( : {e}') """
          

   


def get_user(username):
   

   driver, file = Driver.get(f"https://facebook.com/{username}", capture_traffic=True, cookies_fb=True)
   html = driver.page_source

   soup = BeautifulSoup(html, "lxml")

   dom = etree.HTML(str(soup))

   try:
      if dom.xpath('(//div[@class="x78zum5 x15sbx0n x5oxk1f x1jxijyj xym1h4x xuy2c7u x1ltux0g xc9uqle"]//span//a//text())[2]') == " Me gusta":
         followers_count = dom.xpath('(//div[@class="x78zum5 x15sbx0n x5oxk1f x1jxijyj xym1h4x xuy2c7u x1ltux0g xc9uqle"]//span//a//text())[3]')
      else:
         followers_count = dom.xpath('(//div[@class="x78zum5 x15sbx0n x5oxk1f x1jxijyj xym1h4x xuy2c7u x1ltux0g xc9uqle"]//span//a//text())[1]')

   except:
      followers_count = dom.xpath('(//div[@class="x78zum5 x15sbx0n x5oxk1f x1jxijyj xym1h4x xuy2c7u x1ltux0g xc9uqle"]//span//a//text())[1]')

   turned_number = turn_numbers(followers_count)
   print(turned_number)

   data = []
   data.append({"username": username,
                "followers_count": turned_number,
                "profile_link": f"https://facebook.com/{username}"})
   
   print(data)
   
   return data


def main():
   username = input("Introduce the Facebook account you want to scrape: ")

   #get_user(username)

   delete_file('params.json')
   get_user_posts(username)

   """ data = read_logs(username)

   with open(f"{username}_posts_fb.csv", "w", newline="") as f:
      writer = csv.DictWriter(f, fieldnames=["title", "reactions_count", "like_count", "love_count", "care_count", "haha_count", "surprise_count", "sad_count", "angry_count", "comments_count", "comments", "is_video"])
      writer.writeheader()

      for d in data:

         writer.writerow({"title":d["title"], "reactions_count": d["reactions_count"], "like_count": d["like_count"], "love_count": d["love_count"], "care_count": d["care_count"], "haha_count": d["haha_count"], "surprise_count": d["surprise_count"], "sad_count": d["sad_count"], "angry_count": d["angry_count"], "comments_count": d["comments_count"], "comments": d["comments"], "is_video": d["is_video"]}) """

if __name__ == "__main__":
   main()
