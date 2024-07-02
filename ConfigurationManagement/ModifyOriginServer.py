import requests


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


server_ids = []
kill_input = ""
print("Please provide the Server IDs :" "\n")

while True:
    line = input()
    if line == kill_input:
        break
    server_ids.extend(line.strip().split(","))


appgw_cname = input("Please provide the new IP/CNAME :""\n")

for server_id in server_ids:
    
    api_url = (f"https://my.imperva.com/api/prov/v1/sites/dataCenters/servers/edit?server_id={server_id}&server_address={appgw_cname}&is_enabled=true&is_standby=false")

    response = requests.post(api_url,headers=headers,verify=False)

    print(f"Server ID {server_id} response status code {response.status_code}")

