import requests
import json
import csv

# Set your API credentials
Wex_Health_headers = {
    "Content-Type": "application/json",
    "Accept-Encoding": "gzip, deflate, br",
    "Connection": "keep-alive",
    "x-api-id": "",
    "x-api-key": ""
    
}
Wex_Inc_headers = {
    "Content-Type": "application/json",
    "Accept-Encoding": "gzip, deflate, br",
    "Connection": "keep-alive",
    "x-api-id": "",
    "x-api-key": ""
    
}

headers = input("Which Imperva Tenant are you searching? Wex Health/Wex Inc? :""\n")

if headers == "Wex Health" or headers == "wex health" or headers == "Wex health" or headers == "wex Health" or headers == "Wex Helth":
    headers = Wex_Health_headers

elif headers == "Wex Inc" or headers == "wex inc" or headers == "Wex inc" or headers == "Wex Corp":
    headers = Wex_Inc_headers


site_ids = []
kill_input = ""
print("Please provide the site ids you wish to add this delivery setting too :" "\n")

while True:
    line = input()
    if line == kill_input:
        break
    site_ids.extend(line.strip().split(","))

print(site_ids)

for site_id in site_ids:

    data = {
  "network": {
    "enable_http2": True,
    "http2_to_origin": False
  }
}

    api_url = (f"https://my.imperva.com/api/prov/v2/sites/{site_id}/settings/delivery")

    response = requests.put(api_url, headers=headers, data=json.dumps(data), verify=False)

    print(f"Site ID {site_id} response status code {response.status_code}")