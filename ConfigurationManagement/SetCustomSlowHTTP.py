import requests
import json
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

#Slow_HTTP_Interval = input("What is the Interval you wish to set (in seconds)? :""\n")
#Slow_HTTP_Bytes = input("What is the Bytes you wish to set (in bytes)? :""\n")

site_ids = []


kill_input = ""
print("Please provide the site ids you wish to add this delivery setting too :" "\n")

while True:
    line = input()
    if line == kill_input:
        break
    site_ids.extend(line.strip().split(","))

print(site_ids)

for site_id in site_ids:

    value = {
                    "methods": ["HTTP_POST", "HTTP_GET"],
                    "interval": 120,
                    "byteCount": 5000
                }
            
    params = {
                'site_id': site_id,
                'param': 'request_body_timeouts',
                'value': json.dumps(value)
            }
    
   
    api_url = (f"https://my.imperva.com/api/prov/v1/sites/configure")

    response = ssl_supressed_session().post(api_url, headers=headers, params=params)

    print(response.json())
    print(response.status_code)
    
    
    if response.status_code == 200:
    
        print('Slow HTTP setting has been applied to site id: ' + site_id + '')
        print(response.status_code)