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
print("Please provide the site ids you wish to fetch this delivery setting from :" "\n")

while True:
    line = input()
    if line == kill_input:
        break
    site_ids.extend(line.strip().split(","))
    
for site_id in site_ids:

    api_url = (f"https://my.imperva.com/api/prov/v1/sites/performance/advanced/get?site_id={site_id}&param=redirect_http_to_https")

    response = requests.post(api_url, headers=headers, verify=False)

    print(f"Site ID {site_id} response status code {response.status_code}")

    with open("HTTPtoHTTPSredirectSettings.txt", "a") as f:
        f.write(f"Site ID {site_id} " + str(response.content) + "\n")
