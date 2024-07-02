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

headers = input("Which Imperva Tenant are you working on? Wex Health/Wex Inc? :""\n")

if headers == "Wex Health" or headers == "wex health" or headers == "Wex health" or headers == "wex Health" or headers == "Wex Helth":
    headers = Wex_Health_headers

elif headers == "Wex Inc" or headers == "wex inc" or headers == "Wex inc" or headers == "Wex Corp":
    headers = Wex_Inc_headers


rule_ids = []
kill_input = ""
print("Please provide the rule ids you wish to delete :" "\n")

while True:
    line = input()
    if line == kill_input:
        break
    rule_ids.extend(line.strip().split(","))


for rule_id in rule_ids:

    api_url = (f"https://my.imperva.com/api/prov/v1/sites/incapRules/delete?rule_id={rule_id}")

    response = requests.post(api_url, headers=headers, verify=False)

    print(f"Rule ID {rule_id} DELETED, response status code {response.status_code}")
    print(response.content)
    