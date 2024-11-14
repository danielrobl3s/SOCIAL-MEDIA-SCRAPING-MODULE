import json
import requests

links = []
headers = []
params = []

with open("params.json", "r") as file:
   json_data = json.load(file)

   for entry in json_data:
      if str(entry["url"]).startswith("https://www.facebook.com/api/graphql/"):
         links.append(entry["url"])
         headers.append(entry["headers"])
         params.append(entry["post_data"])


   rango = range(len(links))

   header = {}

   # Loop through the requests
try:
    for x in range(len(links)):
        print(f"Request {x} to URL: {links[x]}")
        
        # Send POST request
        response = requests.request("POST", url=links[x], headers=headers[x], data=params[x])
        
        # Check if the response status code is 200
        if response.status_code == 200:
            try:
                # Attempt to parse JSON response
                print(response.json())
            except json.JSONDecodeError:
                print("Response is not in JSON format:", response.text)
        else:
            print(f"Request failed with status code {response.status_code}: {response.text}")


        print(links[x], headers[x], params[x])

except Exception as e:
    print(f"NooOoOOoOo: {e}")