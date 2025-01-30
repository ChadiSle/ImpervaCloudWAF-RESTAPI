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
print("Please provide the Site IDs you want the TXT Records for:" "\n")
while True:
    line = input()
    if line == kill_input:
        break
    site_ids.extend(line.strip().split(","))

TXT_Record_Info = []

for site_id in site_ids:
    
    api_url = (f"https://my.imperva.com/api/prov/v1/sites/status?site_id={site_id}&tests=domain_validation")

    response = ssl_supressed_session().post(api_url, headers=headers, verify=False)

    print(response.status_code)
    response_content = response.content

    contentInSTR = response_content.decode('utf-8')

    print(contentInSTR)

    
    if response.status_code == 200:

        pattern1 = r'"set_type_to":"TXT","set_data_to":\["([^"]+)"\]'
        pattern2 = r'"domain":"([^"]+)"'
        pattern3 = r'"dns_record_name":"([^"]+)"'
    
        matchTXT = re.search(pattern1, contentInSTR)
        matchDomain = re.search(pattern2, contentInSTR)
        matchDNSrecordName = re.search(pattern3, contentInSTR)

        if matchTXT:
            set_data_to = matchTXT.group(1)
            domain = matchDomain.group(1)
            dns_record_name = matchDNSrecordName.group(1)

            print("dns_record_name:", dns_record_name)
            print("set_data_to:", set_data_to)
            print("domain:", domain)
            TXT_Record_Info.append({'Site ID':site_id, 'Domain':domain, 'DNS Record Name': dns_record_name, 'TXT Record':set_data_to})
            
            
        else: print(f"No Match Found")

            
data_frame = pandas.DataFrame(TXT_Record_Info)
excel_file_name = 'TXT_to_Domain_Info.xlsx'
data_frame.to_excel(excel_file_name, index=False)

print("Please check the TXT_to_Domain_Info.xlsx file for the TXT Record Info")
