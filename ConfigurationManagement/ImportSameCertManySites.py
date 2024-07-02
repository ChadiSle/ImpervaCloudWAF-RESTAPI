import requests
import json
import base64
# for python versions 3.11 or lower, no need for custom http adapter, you may use the standard requests library and adjust the post/get/put/delete methods accordingly
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

# Currently Testing Sub Account Specific Credentials
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

# Set the certificate details
certificate= ""
certificate = base64.b64encode(certificate.encode('utf-8'))
print(certificate)

# Set the private key details
private_key = ""
private_key = base64.b64encode(private_key.encode('utf-8'))
print(private_key)

#pass_phrase = input("Please provide the passphrase for the certificate (if there isnt one, leave blank and press enter) :""\n")    

# Set the site ids
site_ids = []
kill_input = ""
print("Please provide the site ids you wish to add this certificate too :" "\n")

while True:
    line = input()
    if line == kill_input:
        break
    site_ids.extend(line.strip().split(","))


# Set the API data
data = {
  "certificate": certificate.decode('utf-8'),
  "private_key": private_key.decode('utf-8'),
  "auth_type": "RSA"
}

for site_id in site_ids:

    api_url = (f"https://my.imperva.com/api/prov/v2/sites/{site_id}/customCertificate")

    # Make the API request
    response = ssl_supressed_session().put(api_url, data=json.dumps(data), headers=headers)

# Check the response status code
    if response.status_code == 200:
        print(response.status_code, response.content)
    else:
        print("Error uploading certificate:", response.status_code, response.content)