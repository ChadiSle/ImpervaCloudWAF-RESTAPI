import requests
import re
import pandas
import asyncio

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

#You will need to add subaccount IDs if new subaccounts are added to a tenant, and adjust the rest of the script accordingly 
Wex_Health_ID = 1745073
Partner_Vanities_ID = 2014828
Wex_Inc_ID = 884886

AccountID = input("Is this for the Wex Health or Partner Vanities account ?: ""\n")
if AccountID == "Wex Health" or AccountID == "wex health" or AccountID == "Wex health" or AccountID == "wex Health":
    AccountID = Wex_Health_ID
elif AccountID == "Partner Vanities" or AccountID == "partner vanities" or AccountID == "Partner vanities" or AccountID == "partner Vanities":
    AccountID = Partner_Vanities_ID
else:
    AccountID = Wex_Inc_ID

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
domain_site_data = []



for target_domain in target_domains:

    api_url = (f"https://api.imperva.com/sites-mgmt/v3/sites?names={target_domain}&siteTypes=&caid={AccountID}")

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
excel_file_path = 'domain_to_site_id.xlsx'
data_frame.to_excel(excel_file_path, index=False)

print(f"Excel file '{excel_file_path} created successfully.")
