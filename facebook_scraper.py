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


def extract_json(username, response_text, x):
      # Find the first occurrence of "]}}}}}"
   end_index = response_text.find("]}}}}}") + len("]}}}}}")

   if end_index > -1:
      # Slice the string up to the first complete JSON segment
      first_section = response_text[:end_index]
      
      try:
         # Load the JSON from this first section
         parsed_data = json.loads(first_section)
         
         # Now you can write it to a file or process it as needed
         with open(f"{username}_output_{x}.json", "w", newline='') as f:
               json.dump(parsed_data, f, indent=4)
      
      except json.JSONDecodeError as e:
         print(f"JSON decoding error: {e}")
   else:
      print("The end sequence was not found in the response.")


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



def get_Querystring(filename="params.json"):
   with open(filename, "r") as file:
        params = json.load(file)

        entries = params["log"]["entries"]
        
        url = any
        links = []
        headers = []
        paramets = []

        for entry in entries:
      
            if str(entry['request']['url']).startswith('https://www.facebook.com/api/graphql/'):

               url = entry['request']['url']
               header= entry['request']['headers']
               parameters = entry['request']['postData']

               links.append(url)
               headers.append(header)
               paramets.append(parameters)

   return links, headers, paramets


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



def get_user_posts(username):
   
   driver, file = Driver.get(f"https://facebook.com/{username}", headless=True, capture_har=True, cookies_fb=True, scroll=True)
   html = driver.page_source
   links, headers, paramets = get_Querystring()

   rango = range(len(links))

   payload = []

   try:
      for x in rango:
         print(x)

            # Convert headers to a dictionary
         header = {item['name']: item['value'] for item in headers[x]}
            
            # Convert paramets to a dictionary
         params = {param['name']: param['value'] for param in paramets[x]['params']}

         #print(links[x], header, params)

         if "Accept-Encoding" in header.keys():
            header.pop('Accept-Encoding')
            print(header)

         pload = ''

         for key, value in params.items():
            pload = pload + str(key) + '=' + str(value) + '&'
         
         if pload.endswith('&'):
            pload = pload[:-1]

         print(pload)
         
         response = requests.request("POST", url=links[x], headers=header, data=pload)
         
         json_data = response.text

         extract_json(username, json_data, x)
         
   except Exception as e: 
     print(f'something went wrong :( : {e}')
          

   


def get_user(username):
   

   driver, file = Driver.get(f"https://facebook.com/{username}", capture_har=True, cookies_fb=True)
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
   pass

if __name__ == "__main__":
   username = input("Introduce the Facebook account you want to scrape: ")

   delete_file('params.json')
   get_user_posts(username)
   data = read_logs(username)

   for e in data:
      print(e["title"]+" love_count: "+str(e["love_count"]))