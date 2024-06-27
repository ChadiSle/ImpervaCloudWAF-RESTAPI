import requests

#The Following libraries are required to disable SSL verification if using latest Python version with Imperva API
#If you are using Python 3.11 or below, you can use the requests library without the following libraries, and remove the ssl_supressed_session function, and only use the requests.put, requests.post, requests.get, etc.
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
print("Please provide the site ID(s) you wish to Add/Remove a policy too." "\n")

while True:
    line = input()
    if line == kill_input:
        break
    site_ids.extend(line.strip().split(","))

site_ids = [int(num) for num in site_ids]

print(site_ids)

Wex_Prod_ACL_ID = 526290
Wex_Internal_ACL_ID = 493695
MG4_Temp_Block_All_ACL_ID = 1247968

#If applying ACL to a site in the subaccount, you will need to specify the account ID in the api_url by appending "?caid={Partner_Vanities_AccountID}"
Partner_Vanities_AccountID = input("Is this the Partner Vanities subaccount? Yes/No""\n")
if Partner_Vanities_AccountID == "Yes":
    Wex_Internal_ACL_ID = "493695?caid=2014828"
    Wex_Prod_ACL_ID = "526290?caid=2014828"

Action_Input = input("Would you like to Add/Remove a Policy?""\n")
Policy_Input = input("Is it the Internal/Prod/Temp ACL?""\n")

if Action_Input == "Add" and Policy_Input == "Temp":
    for site_id in site_ids:

        api_url = (f"https://api.imperva.com/policies/v2/assets/WEBSITE/{site_id}/policies/{MG4_Temp_Block_All_ACL_ID}")

        response = ssl_supressed_session().post(api_url, headers=headers)

        print(f"Site ID {site_id} response status code {response.status_code}")

        if response.status_code == 200 :
            print("Policy Applied Successfully")

        else: 
            print(response.content)


if Action_Input == "Add" and Policy_Input == "Internal":
    for site_id in site_ids:

        api_url = (f"https://api.imperva.com/policies/v2/assets/WEBSITE/{site_id}/policies/{Wex_Internal_ACL_ID}")

        response = ssl_supressed_session().post(api_url, headers=headers, verify=False)

        print(f"Site ID {site_id} response status code {response.status_code}")

        if response.status_code == 200 :
            print("Policy Applied Successfully")

        else: 
            print(response.content)

if Action_Input == "Remove" and Policy_Input == "Temp":
    
    for site_id in site_ids:

        api_url = (f"https://api.imperva.com/policies/v2/assets/WEBSITE/{site_id}/policies/{MG4_Temp_Block_All_ACL_ID}")

        response = ssl_supressed_session().delete(api_url, headers=headers, verify=False)

        print(f"Site ID {site_id} response status code {response.status_code}")

        if response.status_code == 200 :
            print("Policy Removed Successfully")

        else: 
            print(response.content)


if Action_Input == "Remove" and Policy_Input == "Internal":
    
    for site_id in site_ids:

        api_url = (f"https://api.imperva.com/policies/v2/assets/WEBSITE/{site_id}/policies/{Wex_Internal_ACL_ID}")

        response = ssl_supressed_session().delete(api_url, headers=headers, verify=False)

        print(f"Site ID {site_id} response status code {response.status_code}")

        if response.status_code == 200 :
            print("Policy Removed Successfully")

        else: 
            print(response.content)

if Action_Input == "Add" and Policy_Input == "Prod":
    for site_id in site_ids:

        api_url = (f"https://api.imperva.com/policies/v2/assets/WEBSITE/{site_id}/policies/{Wex_Prod_ACL_ID}")

        response = ssl_supressed_session().post(api_url, headers=headers, verify=False)

        print(f"Site ID {site_id} response status code {response.status_code}")

        if response.status_code == 200 :
            print("Policy Applied Successfully")

        else: 
            print(response.content)

if Action_Input == "Remove" and Policy_Input == "Prod":
    
    for site_id in site_ids:

        api_url = (f"https://api.imperva.com/policies/v2/assets/WEBSITE/{site_id}/policies/{Wex_Prod_ACL_ID}")

        response = ssl_supressed_session().delete(api_url, headers=headers, verify=False)

        print(f"Site ID {site_id} response status code {response.status_code}")

        if response.status_code == 200 :
            print("Policy Removed Successfully")

        else: 
            print(response.content)