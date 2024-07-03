import requests
import json
#The below libaries allow for the creation of a custom HTTP Adapter which I have found necessary working from certain environment and versions of python. I believe the "Unsafe Legacy Renegotiation Disabled" error is due to a CVE imperva may not be privy too regarding their latest SSL certificates on their API servers. Python has recently removed those unsecure certs from their ssl library. I suggest trying to run this script normally with the requests library before proceeding to disable ssl with this custom adapter if you get an ssl error.
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

hsmCertificate = "hsmCertificate"
api_url = "https://my.imperva.com/api/prov/v2/sites"

site_ids = []
kill_input = ""
print("Please provide the site ids you wish to add this certificate too :" "\n")

while True:
    line = input()
    if line == kill_input:
        break
    site_ids.extend(line.strip().split(","))

print(site_ids)

for site_id in site_ids:

    data = {
  "data": {
    "certificate": "", # Add public full chained cert in base64 here
    "hsmDetails": [
      {
        "keyId": "", # UUID of Security Object in Fortanix for the private key of the cert
        "apiKey": "", # Fortanix API Key
        "hostName": "api.amer.smartkey.io"
      }
    ]
  }
}

    api_endpoint = f"{api_url}/{site_id}/{hsmCertificate}"
    
    response = requests.put(api_endpoint, headers=headers, data=json.dumps(data), verify=False)

    print(f"Site ID {site_id} response status code: {response.status_code}")
