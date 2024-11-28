from cdriver import Driver
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from csv import DictReader
import json
import time
import os

def get_user_cookies_values(file):
   with open(file, encoding='utf-8') as f:
      dict_reader = DictReader(f)
      list_of_dicts = list(dict_reader)
   
   return list_of_dicts


def delete_file(f_path):

   # Check if the file exists before attempting to delete
   if os.path.exists(f_path):
      os.remove(f_path)
      print(f"{f_path} has been deleted successfully.")
   else:
      print(f"{f_path} does not exist, creating a new one")



def read_json(file):

   with open(file, 'r') as f:
    data = json.load(f)

   return data


def get_user_cookies(username):
   Driver.get(f"https://tiktok.com/@{username}", headless=False, capture_traffic=True, cookies_tk=True, scroll=True)
   file = "params.json"

   time.sleep(100)

   return file


def get_queryString(username):

   f = 'params.json'

   delete_file(f)
   file= get_user_cookies(username)
   params = read_json(file)

   print(params)

   url = any
   query_string = any

   links = []


   for entry in params:

      print(entry)

      try:
      
         if entry['url'].startswith('https://www.tiktok.com/api/post/item_list/'):

            url = entry['url']
            #query_string = entry['request']['queryString']

            links.append(url)
      except:
         continue

   return links


def main():
   pass


#Entry point ------------->
if __name__ == '__main__':
   main()
