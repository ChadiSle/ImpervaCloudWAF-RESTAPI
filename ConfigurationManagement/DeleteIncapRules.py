import requests
import json
import csv
#The below libaries allow for the creation of a custom HTTP Adapter which I have found necessary working from certain environment and versions of python. I believe the "Unsafe Legacy Renegotiation Disabled" error is due to a CVE imperva may not be privy too regarding their latest SSL certificates on their API servers. Python has recently removed those unsecure certs from their ssl library. I suggest trying to run this script normally with the requests library before proceeding to disable ssl with this custom adapter if you get an ssl error.
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

    response = ssl_supressed_session().post(api_url, headers=headers, verify=False)

    print(f"Rule ID {rule_id} DELETED, response status code {response.status_code}")
    print(response.content)
    
