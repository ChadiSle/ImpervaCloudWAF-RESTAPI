import requests
import re
import pandas
import datetime
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
print("Please provide the Site IDs you want to check HSM connectivity for:" "\n")

while True:
    line = input()
    if line == kill_input:
        break
    site_ids.extend(line.strip().split(","))

CompliantNonCompliantSites = []

for site_id in site_ids:
    
    api_url = (f"https://my.imperva.com/api/prov/v2/sites/{site_id}/hsmCertificate/connectivityTest")

    # If using an ssl suppresed session, comment out the requests.post() and uncomment the ssl_supressed_session().post() 
    #response = ssl_supressed_session().get(api_url, headers=headers, verify=False)
    
    response = requests.get(api_url, headers=headers, verify=False)

    print(response.status_code)
   

    response_content = response.content

    contentInSTR = response_content.decode('utf-8')

   
    if response.status_code != 200:

        print(contentInSTR)

        site_status_url = (f"https://my.imperva.com/api/prov/v1/sites/status?site_id={site_id}&tests=domain_validation")

        # If using an ssl suppresed session, comment out the requests.post() and uncomment the ssl_supressed_session().post() 
        #site_status = ssl_supressed_session().post(site_status_url, headers=headers, verify=False)
    
        site_status = requests.post(site_status_url, headers=headers, verify=False)

        print(site_status.content)

        if site_status.status_code == 200:

            site_statusSTR = site_status.content

            site_status_responseSTR = site_statusSTR.decode('utf-8')

            pattern = r'"domain":"([^"]+)"'
    
            match = re.search(pattern, site_status_responseSTR)

            if match:
                domain = match.group(1)
                CompliantNonCompliantSites.append({'Site ID':site_id, 'Domain':domain, 'HSM Connectivity': 'No'})
                print(f"Site ID: {site_id} Domain: {domain}")

    elif response.status_code == 200:

        site_status_url = (f"https://my.imperva.com/api/prov/v1/sites/status?site_id={site_id}&tests=domain_validation")

        # If using an ssl suppresed session, comment out the requests.post() and uncomment the ssl_supressed_session().post() 
        #site_status = ssl_supressed_session().post(site_status_url, headers=headers, verify=False)
    
        site_status = requests.post(site_status_url, headers=headers, verify=False))

        if site_status.status_code == 200:

            site_statusSTR = site_status.content

            site_status_responseSTR = site_statusSTR.decode('utf-8')

            pattern = r'"domain":"([^"]+)"'
    
            match = re.search(pattern, site_status_responseSTR)

            if match:
                domain = match.group(1)
                CompliantNonCompliantSites.append({'Site ID':site_id, 'Domain':domain, 'HSM Connectivity': 'Yes'})
                print(f"Site ID: {site_id} Domain: {domain}")
            
data_frame = pandas.DataFrame(CompliantNonCompliantSites)
excel_file_name = 'HSM_Compliance_Report.xlsx'
data_frame.to_excel(excel_file_name, index=False)

print("Please check the HSM_Compliance_Report.xlsx file")
