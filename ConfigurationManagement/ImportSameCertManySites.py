import requests
import json
import base64

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

# Set the certificate details (copy paste here, the script will do the encoding)
certificate= ""
certificate = base64.b64encode(certificate.encode('utf-8'))
print(certificate)

# Set the private key details (copy paste here, the script will do the encoding)
private_key = ""
private_key = base64.b64encode(private_key.encode('utf-8'))
print(private_key)

#pass_phrase = input("Please provide the passphrase for the certificate (if there isnt one, leave blank and press enter) :""\n")  "Enable this line if using pfx"

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
  "auth_type": "RSA" #Change to "ECC" depending on cert type, also if using pfx another line with "pass_phrase": f'{pass_phrase}
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
