import requests
import re
import pandas as pd
#The below libaries allow for the creation of a custom HTTP Adapter which I have found necessary working from certain environment and versions of python. I suggest trying to run this script normally with the requests library before proceeding to disable ssl with this custom adapter if you get an ssl error.
from requests import Session
from requests import adapters
from urllib3 import poolmanager
from ssl import create_default_context, Purpose, CERT_NONE

class CustomHttpAdapter (adapters.HTTPAdapter):
    def __init__(self, ssl_context=None, **kwargs):
        self.ssl_context = ssl_context
        super().__init__(**kwargs)

    def init_poolmanager(self, connections, maxsize, block=False):
        self.poolmanager = poolmanager.PoolManager(
            num_pools=connections, maxsize=maxsize,
            block=block, ssl_context=self.ssl_context)

def ssl_supressed_session():
    ctx = create_default_context(Purpose.SERVER_AUTH)
    # to bypass verification after accepting Legacy connections
    ctx.check_hostname = False
    ctx.verify_mode = CERT_NONE
    # accepting legacy connections
    ctx.options |= 0x4    
    session = Session()
    session.mount('https://', CustomHttpAdapter(ctx))
    return session


# Set your API credentials
Imperva_Headers_Account1 = {
    "Content-Type": "application/json",
    "Accept-Encoding": "gzip, deflate, br",
    "Connection": "keep-alive",
    "x-api-id": "",
    "x-api-key": ""
    
}

Imperva_Headers_Account2 = {
    "Content-Type": "application/json",
    "Accept-Encoding": "gzip, deflate, br",
    "Connection": "keep-alive",
    "x-api-id": "",
    "x-api-key": ""
    
}

# Adjust the header variable names to reflect the name of the accounts you will most commonly be working on and the credentials you will need for them.

headers = input("Which Imperva Tenant are you working with? :""\n")

# Giving a few variations of common typos will help mitigate errors and breaks when running the script, eg lowercase, missed last letter etc.
if headers == "Imperva_Headers_Account1" or headers == "imperva_headers_account1":
    headers = Imperva_Headers_Account1

elif headers == "Imperva_Headers_Account2" or headers == "imperva_headers_account2":
    headers = Imperva_Headers_Account2

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

    # If using an ssl suppresed session, comment out the requests.post() and uncomment the ssl_supressed_session().post() 
    #response = ssl_supressed_session().post(api_url, headers=headers, verify=False)
    
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
