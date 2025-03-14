import requests
import json
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

import requests
import pandas
import re

# Set your API credentials
headers = {
    "Content-Type": "application/json",
    "Accept-Encoding": "gzip, deflate, br",
    "Connection": "keep-alive",
    "x-api-id": "",
    "x-api-key": ""
    
}

site_ids = []
kill_input = ""
print("Please provide the site ids you wish to check this delivery setting for :" "\n")

HTTP2_Report=[]

while True:
    line = input()
    if line == kill_input:
        break
    site_ids.extend(line.strip().split(","))

for site_id in site_ids:

    api_url = (f"https://my.imperva.com/api/prov/v1/sites/performance/advanced/get?site_id={site_id}&param=http_2")

    response = requests.post(api_url, headers=headers, verify=False)
    
    # If using an ssl suppresed session, comment out the requests.post() and uncomment the ssl_supressed_session().post() 
    #response = ssl_supressed_session().post(api_url, headers=headers, verify=False)
    
    response_content=response.content
    print(response_content)
    pattern = (rb'"value"\s*:\s*true')
    match_setting_value = re.search(pattern, response_content)

    if match_setting_value:
        print(f"Site ID {site_id} response status code {response.status_code}")
        print(response.content)
        HTTP2_Report.append({"Site ID":site_id,"HTTP/2 Setting Value":"True"})
        
    else:
        print(f"Site ID {site_id} response status code {response.status_code}")
        print(response.content)
        HTTP2_Report.append({"Site ID":site_id,"HTTP/2 Setting Value":"False"})

data_frame = pandas.DataFrame(HTTP2_Report)
excel_file_name = 'HTTP2_Report.xlsx'
data_frame.to_excel(excel_file_name, index=False)
print("Please check HTTP2_Report.xlsx for results")
