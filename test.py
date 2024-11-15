import json
import requests

links = []
headers = []
params = []


def read_json():
   with open("params.json", "r") as file:
      json_data = json.load(file)

      for entry in json_data:
         if str(entry["url"]).startswith("https://www.facebook.com/api/graphql/"):
            response = entry["response"]["content"]

            print(response)

read_json()