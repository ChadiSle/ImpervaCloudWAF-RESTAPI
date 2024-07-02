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

#add account and subaccount IDs here and adjust the rest of the script accordingly
account_id = 1745073
extra_config_flag = "disable-js-client-classification"
api_url = (f"https://my.incapsula.com/api/internal/sites/v1/config/list_extra_config?caid={account_id}&extra_config={extra_config_flag}")

response = requests.post(api_url, headers=headers, verify=False)

print(response.content)