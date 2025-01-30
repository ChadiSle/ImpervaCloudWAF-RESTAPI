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


site_ids = []
kill_input = ""
print("Please provide the Site IDs of the sites you want to verify:" "\n")
while True:
    line = input()
    if line == kill_input:
        break
    site_ids.extend(line.strip().split(","))

SiteStatusInfo = []

for site_id in site_ids:
    
    api_url = (f"https://my.imperva.com/api/prov/v1/sites/status?site_id={site_id}&tests=services")

    response = ssl_supressed_session().post(api_url, headers=headers, verify=False)

    print(response.status_code)
    response_content = response.content

    contentInSTR = response_content.decode('utf-8')

    if response.status_code == 200:

        response_content = response.content

        contentInSTR = response_content.decode('utf-8')

        DomainPattern = r'"domain":"([^"]+)"'
        expPattern = r'"expirationDate":(\d+)'
    
        expirationDate_match = re.search(expPattern, contentInSTR)
        DomainMatch = re.search(DomainPattern, contentInSTR)

        if expirationDate_match:
            domain = DomainMatch.group(1)
            expirationDate = expirationDate_match.group(1)
            expirationDate = pandas.to_datetime(expirationDate, unit='ms')
            print(expirationDate)
            SiteStatusInfo.append({'Site ID':site_id, 'Website': domain, 'SSL Expiration Date': expirationDate, 'Site Status': 'VERIFIED'})
            print(f"Site ID: {site_id} Connection Validated")
            
        else:
            SiteStatusInfo.append({'Site ID': site_id, 'Website': 'Unable to Obtain', 'SSL Expiration Date': 'Unable to Obtain', 'Site Status': 'UNVERIFIED'})
            print(contentInSTR)

            
data_frame = pandas.DataFrame(SiteStatusInfo)
excel_file_name = 'SiteStatusVerification.xlsx'
data_frame.to_excel(excel_file_name, index=False)

print("Please check the SiteStatusVerification.xlsx file for the Site Status Info")
