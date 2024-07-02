import requests
import re
import pandas as pd
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

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
print("Please provide the Site IDs you want ServerIDs for :" "\n")
while True:
    line = input()
    if line == kill_input:
        break
    site_ids.extend(line.strip().split(","))

with open("server_ids.txt", "a") as f:
    f.write("ServerIDs" + "\n")

server_ids = []

for site_id in site_ids:
    
    api_url = (f"https://my.imperva.com/api/prov/v1/sites/dataCenters/list?site_id={site_id}")

    response = requests.post(api_url, headers=headers, verify=False)

    if response.status_code != 200:
        print(response.content)

    contentInSTR = str(response.content)

    pattern = re.compile(r'"id":"(\d+)"')
    
    match = pattern.search(contentInSTR)

    if match:
        server_id = match.group(1)
        server_ids.append(server_id)
        
    with open("server_ids.txt", "a") as f:
        f.write(str(server_id) + "\n")

    print(f"Site ID {site_id} response status code {response.status_code}")
    print("Origin Server ID " + server_id)