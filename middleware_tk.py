from browsermobproxy import Server
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
   driver, file = Driver.get(f"https://tiktok.com/@{username}", headless=False, capture_har=True, cookies=True)
   
   print(driver.page_source)

   return file


def get_queryString(username):

   f = 'params.json'

   delete_file(f)
   file= get_user_cookies(username)
   params = read_json(file)

   entries = params['log']['entries']

   url = any
   query_string = any

   links = []

   for entry in entries:
      
      if str(entry['request']['url']).startswith('https://www.tiktok.com/api/post/item_list/'):

         url = entry['request']['url']
         #query_string = entry['request']['queryString']

         links.append(url)

   return links


def main():
   pass


#Entry point ------------->
if __name__ == '__main__':
   main()
