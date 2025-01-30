#DDoS Proactive Threshold Warning Compliance Report (This script can be adjusted to verify the presence of any Security Rule on a sites configuration so long as the naming convention is absolute with no typos or errors
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
print("Please provide the Site IDs you want to Audit for DDoS Alerting:" "\n") #Adjust rule name accordingly if desired
while True:
    line = input()
    if line == kill_input:
        break
    site_ids.extend(line.strip().split(","))

incap_rule_id_info = []

for site_id in site_ids:
    
    api_url = (f"https://my.imperva.com/api/prov/v1/sites/status?site_id={site_id}&tests=domain_validation")

    response = ssl_supressed_session().post(api_url, headers=headers, verify=False)

    print(response.status_code)
    response_content = response.content

    contentInSTR = response_content.decode('utf-8')

    print(contentInSTR)

    
    if response.status_code == 200:

        # Adjust the value for "name" to reflect the rule you want to verify the presence of
        
        pattern = r'"id":(\d+),"name":"DDoS Proactive Threshold Warning"'
    
        match = re.search(pattern, contentInSTR)

        if match:
            incap_rule_id = match.group(1)
            incap_rule_id_info.append({'Site ID':site_id, 'Rule ID':incap_rule_id})
            print(f"Site ID: {site_id} Rule ID: {incap_rule_id}")
            
        else: 
            print(f"No Match Found, here is the response content {contentInSTR}")
            incap_rule_id_info.append({'Site ID':site_id, 'Rule ID': 'No Matching RuleID'})

            
data_frame = pandas.DataFrame(incap_rule_id_info)
excel_file_name = 'Security_Rule_Compliance_Report.xlsx'
data_frame.to_excel(excel_file_name, index=False)

print("Please check the DDoS_Proactive_Threshold_Alert_Audit.xlsx file for the Site ID and Compliance Status")
