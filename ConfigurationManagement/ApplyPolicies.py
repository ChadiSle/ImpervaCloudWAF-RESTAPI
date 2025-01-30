import requests

#This script can be adjusted for any number of policies and will work for applying/removing said policy from any number of sites at once

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
print("Please provide the site ID(s) you wish to Add/Remove a policy too." "\n")

while True:
    line = input()
    if line == kill_input:
        break
    site_ids.extend(line.strip().split(","))

site_ids = [int(num) for num in site_ids]

# Adjust the variable names to coincide with the ACL/Allowlist names in the tenant. Adjust the values for each to reflect the corresponding Policy ID
ACL_ID_1 =
ACL_ID_2 =
ACL_ID_3 =

#If applying ACL to a site in a subaccount, you will need to specify the account ID in the api_url by appending "?caid={SubAccountID}"
SubAccountID = input("Is this site in a subaccount? Yes/No:""\n")
if SubAccountID == "Yes" or SubAccountID == "yes":
    SubAccountID = input("What is the SubaccountID?:""\n")
    ACL_ID_1 = f"{ACL_ID_1}?caid={SubAccountID}"
    ACL_ID_2 = f"{ACL_ID_2}?caid={SubAccountID}"
    #Add additional variables for additional ACLs

Action_Input = input("Would you like to Add/Remove a Policy?""\n")
Policy_Input = input("Is it ACL1/ACL2/ACL3?""\n")

if Action_Input == "Add" and Policy_Input == "ACL1":
    for site_id in site_ids:

        api_url = (f"https://api.imperva.com/policies/v2/assets/WEBSITE/{site_id}/policies/{ACL_ID_1}")

        response = ssl_supressed_session().post(api_url, headers=headers)

        print(f"Site ID {site_id} response status code {response.status_code}")

        if response.status_code == 200 :
            print("Policy Applied Successfully")

        else: 
            print(response.content)


if Action_Input == "Add" and Policy_Input == "ACL2":
    for site_id in site_ids:

        api_url = (f"https://api.imperva.com/policies/v2/assets/WEBSITE/{site_id}/policies/{ACL_ID_2}")

        response = ssl_supressed_session().post(api_url, headers=headers, verify=False)

        print(f"Site ID {site_id} response status code {response.status_code}")

        if response.status_code == 200 :
            print("Policy Applied Successfully")

        else: 
            print(response.content)

if Action_Input == "Remove" and Policy_Input == "ACL1":
    
    for site_id in site_ids:

        api_url = (f"https://api.imperva.com/policies/v2/assets/WEBSITE/{site_id}/policies/{ACL_ID_1}")

        response = ssl_supressed_session().delete(api_url, headers=headers, verify=False)

        print(f"Site ID {site_id} response status code {response.status_code}")

        if response.status_code == 200 :
            print("Policy Removed Successfully")

        else: 
            print(response.content)


if Action_Input == "Remove" and Policy_Input == "ACL2":
    
    for site_id in site_ids:

        api_url = (f"https://api.imperva.com/policies/v2/assets/WEBSITE/{site_id}/policies/{ACL_ID_2}")

        response = ssl_supressed_session().delete(api_url, headers=headers, verify=False)

        print(f"Site ID {site_id} response status code {response.status_code}")

        if response.status_code == 200 :
            print("Policy Removed Successfully")

        else: 
            print(response.content)

if Action_Input == "Add" and Policy_Input == "ACL3":
    for site_id in site_ids:

        api_url = (f"https://api.imperva.com/policies/v2/assets/WEBSITE/{site_id}/policies/{ACL_ID_3}")

        response = ssl_supressed_session().post(api_url, headers=headers, verify=False)

        print(f"Site ID {site_id} response status code {response.status_code}")

        if response.status_code == 200 :
            print("Policy Applied Successfully")

        else: 
            print(response.content)

if Action_Input == "Remove" and Policy_Input == "ACL3":
    
    for site_id in site_ids:

        api_url = (f"https://api.imperva.com/policies/v2/assets/WEBSITE/{site_id}/policies/{ACL_ID_3}")

        response = ssl_supressed_session().delete(api_url, headers=headers, verify=False)

        print(f"Site ID {site_id} response status code {response.status_code}")

        if response.status_code == 200 :
            print("Policy Removed Successfully")

        else: 
            print(response.content)
