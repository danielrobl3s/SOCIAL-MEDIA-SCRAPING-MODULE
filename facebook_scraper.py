import gzip
import zlib
import requests
from cdriver import Driver
import time
import os
from bs4 import BeautifulSoup
from lxml import etree
import json
import re

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



def get_user_posts():
   username = input("Introduce the Facebook account you want to scrape: ")

   driver, file = Driver.get(f"https://facebook.com/{username}", capture_har=True, cookies_fb=True, scroll=True)
   html = driver.page_source
   links, headers, paramets = get_Querystring()

   for i in range(len(links)):
      url = links[i]
      header = {item['name']: item['value'] for item in headers[i]} 
      params = {param['name']: param['value'] for param in paramets[i]['params']}

      print(url, header, params)

      try:
        response = requests.post(url, headers=header, data=params)
        
        # Check if the response is compressed
        if response.headers.get('Content-Encoding') == 'gzip':
            response_data = gzip.decompress(response.content)
            print(response_data)
        elif response.headers.get('Content-Encoding') == 'deflate':
            response_data = zlib.decompress(response.content)
            print(response_data)
        else:
            response_data = response.content
            print(response_data)
      except:
         pass

   


def get_user():
   username = input("Introduce the Facebook account you want to scrape: ")

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
   delete_file('params.json')
   get_user_posts()