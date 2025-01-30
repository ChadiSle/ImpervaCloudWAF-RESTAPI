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


site_info = []
domains = []
kill_input = ""
print("Please provide the domains you wish to Onboard :" "\n")

# This while loop allows for the copy pasting of inputs from sheets such as an excel file where each input is on a new line, to continue you must press enter twice after pasting or typing an input, the blank line kills the input so the script can continue
while True:
    line = input()
    if line == kill_input:
        break
    domains.extend(line.strip().split(","))

print(domains)

account_id = input("Which account will you be onboarding to? Account1/Account2/Subaccount1ofAccount1? :""\n")

#Add Parent and Subaccount IDs here to easily differentiate and pivot where you want to onboard your sites, add some room for error when specifying as above with the header names
if account_id == "Account1" or account_id == "account1":
    account_id = ""
    headers = Imperva_Headers_Account1

elif account_id == "Account1_Subaccount1" or account_id == "account1_subaccount1":
    account_id = ""
    headers = Imperva_Headers_Account1

elif account_id == "Account2":
    account_id = ""
    headers = Imperva_Headers_Account2

#if using Advanced Config ie specifying the DNS
advanced_config = input("Will you be defining the origin IP/CNAME Yes/No :""\n")

if advanced_config == "Yes" or advanced_config == "yes":

    cname_or_IP = input("Please provide the IP/CNAME :""\n")

#When setting up sites prior to them having valid DNS, specify the IP/CNAME by appending "&site_ip=" to the api_url. For example: "/sites/add?domain=example.imperva.com&account_id=10&send_site_setup_emails=True&site_ip=1.2.3.4&log_level=full"
#If you are specifying IP/CNAME you will also have to force SSL by adding "&force_ssl=True" to the api_url, its also efficient to add "&log_level=full"
    for domain in domains:

        api_url = (f"https://my.imperva.com/api/prov/v1/sites/add?domain={domain}&account_id={account_id}&send_site_setup_emails=True&site_ip={cname_or_IP}&force_ssl=True&log_level=full")

        #Currently the Custom HTTP Adapter is being usede to make this call, to use the requests library instead simply change ssl_suppressed_session().post > requests.post
        response = ssl_supressed_session().post(api_url, headers=headers, verify=False)

        response_content = response.content

        # Regex pattern to match the Imperva CNAME
        cname_pattern = r'"set_data_to":\["([^"]+)"\]'
        site_id_pattern = r'"site_id":(\d+)'

        # Search for the cname in the response content
        match_cname = re.search(cname_pattern, response_content.decode())
        match_site_id = re.search(site_id_pattern, response_content.decode())

        if match_cname and match_site_id:
            cname = match_cname.group(1)
            site_id = match_site_id.group(1)

            site_info.append({'Domain': domain, 'SiteID': site_id, 'CNAME': cname})

            print(f"Domain: {domain} has been onboarded successfully, response status code {response.status_code}")
            print("Imperva CNAME: ", cname)
            print("Site ID: ", site_id)

        else:
            print(response_content)

    data_frame = pandas.DataFrame(site_info)
    excel_file_name = 'Onboarded_Site_Info.xlsx'
    data_frame.to_excel(excel_file_name, index=False)

    print("Please check the Onboarded_Site_Info.xlsx file for the Imperva CNAME and Site ID")


elif advanced_config == "No" or advanced_config == "no":

    for domain in domains:
        api_url = (f"https://my.imperva.com/api/prov/v1/sites/add?domain={domain}&account_id={account_id}&send_site_setup_emails=True&force_ssl=True&log_level=full")

        response = ssl_supressed_session().post(api_url, headers=headers, verify=False)

        response_content = response.content

        # Regex pattern to match the Imperva CNAME and site ID
        cname_pattern = r'"set_data_to":\["([^"]+)"\]'
        site_id_pattern = r'"site_id":(\d+)'

        # Search for the cname in the response content
        match_cname = re.search(cname_pattern, response_content.decode())
        match_site_id = re.search(site_id_pattern, response_content.decode())

        if match_cname and match_site_id:
            cname = match_cname.group(1)
            site_id = match_site_id.group(1)
            
            site_info.append({'Domain': domain, 'SiteID': site_id, 'CNAME': cname})

            print(f"Domain: {domain} has been onboarded successfully, response status code {response.status_code}")
            print("Imperva CNAME: ", cname)
            print("Site ID: ", site_id)

        else:
            print(response_content)

    data_frame = pandas.DataFrame(site_info)
    excel_file_name = 'Onboarded_Site_Info.xlsx'
    data_frame.to_excel(excel_file_name, index=False)

    print("Please check the Onboarded_Site_Info.xlsx file for the Imperva CNAME and Site ID")
