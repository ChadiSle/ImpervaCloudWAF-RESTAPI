import requests
import re
import pandas

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
print("Please provide the Site IDs you want the datacenter info for:" "\n")
while True:
    line = input()
    if line == kill_input:
        break
    site_ids.extend(line.strip().split(","))

OriginInfo = []

for site_id in site_ids:
    
    api_url = (f"https://my.imperva.com/api/prov/v3/sites/{site_id}/data-centers-configuration")
    
    #return to normal requests.get method if using normal requests library with python 3.11 or earlier
    response = ssl_supressed_session().get(api_url, headers=headers)

    print(response.status_code)

    if response.status_code == 200:

        api_url_2 = (f"https://my.imperva.com/api/prov/v1/sites/status?site_id={site_id}&tests=domain_validation")
        
        #return to normal requests.post method if using normal requests library with python 3.11 or earlier
        response2 = ssl_supressed_session().post(api_url_2, headers=headers, verify=False)

        if response2.status_code == 200:

            response2_content = response2.content
            response_content = response.content

            contentInSTR = response_content.decode('utf-8')
            content2InSTR = response2_content.decode('utf-8')

            origin_pattern = r'"address":"([^"]+)"'
            domain_pattern = r'"domain":"([^"]+)"'
    
            match_origin = re.search(origin_pattern, contentInSTR)
            match_domain = re.search(domain_pattern, content2InSTR)

            if match_origin and match_domain:
                address = match_origin.group(1)
                domain = match_domain.group(1)
                OriginInfo.append({'Site ID':site_id, 'Domain':domain, 'Imperva Origin Setting':address})
            
            else: print(f"No Match Found, here is the response content {contentInSTR}")

            
data_frame = pandas.DataFrame(OriginInfo)
excel_file_name = 'ImpervaSiteToOriginInfo.xlsx'
data_frame.to_excel(excel_file_name, index=False)

print("Please check the ImpervaSiteToOriginInfo.xlsx file for the Imperva Origin and Site ID")




    