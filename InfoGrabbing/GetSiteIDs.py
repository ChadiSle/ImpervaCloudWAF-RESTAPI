import requests
import re
import pandas
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

#You will need to add subaccount IDs if new subaccounts are added to a tenant, and adjust the rest of the script accordingly 

account_id = input("Which account or subaccount will you be searching? Account1/Account2/Subaccount1ofAccount1? :""\n")

#Add Parent and Subaccount IDs here to easily differentiate and pivot where you want to search for these site_ids, add some room for error when specifying as above with the header names
if account_id == "Account1" or account_id == "account1":
    account_id = ""
    headers = Imperva_Headers_Account1

elif account_id == "Account1_Subaccount1" or account_id == "account1_subaccount1":
    account_id = ""
    headers = Imperva_Headers_Account1

elif account_id == "Account2":
    account_id = ""
    headers = Imperva_Headers_Account2

target_domains = []
kill_input = ""
print("Please provide the domains you need Site IDs for :" "\n")

while True:
    line = input()
    if line == kill_input:
        break
    target_domains.extend(line.strip().split(","))

print(target_domains)
domain_to_site_id = []
matching_site_ids = []

for target_domain in target_domains:

    api_url = (f"https://api.imperva.com/sites-mgmt/v3/sites?names={target_domain}&siteTypes=&caid={accountID}")

    response = ssl_supressed_session().get(api_url, headers=headers)
    #response = requests.get(api_url, headers=headers, verify=False)

    if response.status_code == 200:

        response_content = response.content.decode("utf-8")
        site_id_pattern = r'"id":(\d+)'
        match_site_id = re.search(site_id_pattern, response_content)

        if match_site_id:
            
            site_id = match_site_id.group(1)
            domain_to_site_id.append({'Domain': target_domain, 'SiteID': site_id})
            print(f"Domain: {target_domain} Site ID: {site_id}")

    else:
        print(response.status_code)
        print(response.content)

    
data_frame = pandas.DataFrame(domain_to_site_id)
excel_file_path = 'Domain_to_Site_id.xlsx'
data_frame.to_excel(excel_file_path, index=False)

print(f"Excel file '{excel_file_path} created successfully.")
