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


site_info = []
domains = []
kill_input = ""
print("Please provide the domains you wish to Onboard :" "\n")

while True:
    line = input()
    if line == kill_input:
        break
    domains.extend(line.strip().split(","))

print(domains)

account_id = input("Which account will you be onboarding to? Wex Health/Partner Vanities/Wex Inc? :""\n")

#8/30/23 changed to Wex Inc account ID
#Wex Health: 1745073
if account_id == "Wex Health" or account_id == "wex health" or account_id == "Wex health" or account_id == "wex Health" or account_id == "Wex Helth":
    account_id = 1745073
    headers = Wex_Health_headers

elif account_id == "Partner Vanities" or account_id == "partner vanities" or account_id == "Partner vanities" or account_id == "partner Vanities" or account_id == "Partner Vanity" or account_id == "partner vanity" or account_id == "Partner vanity" or account_id == "partner Vanity" or account_id == "Partner Vanties":
    account_id = 2014828
    headers = Wex_Health_headers

elif account_id == "Wex Inc":
    account_id = 884886
    headers = Wex_Inc_headers

#if using Advanced Config ie specifying the DNS
advanced_config = input("Will you be defining the origin IP/CNAME Yes/No :""\n")

if advanced_config == "Yes" or advanced_config == "yes":

    cname_or_IP = input("Please provide the IP/CNAME :""\n")

#When setting up sites prior to them having valid DNS, specify the IP/CNAME by appending "&site_ip=" to the api_url. For example: "/sites/add?domain=example.imperva.com&account_id=10&send_site_setup_emails=True&site_ip=1.2.3.4&log_level=full"
#If you are specifying IP/CNAME you will also have to force SSL by adding "&force_ssl=True" to the api_url, its also efficient to add "&log_level=full"
    for domain in domains:

        api_url = (f"https://my.imperva.com/api/prov/v1/sites/add?domain={domain}&account_id={account_id}&send_site_setup_emails=True&site_ip={cname_or_IP}&force_ssl=True&log_level=full")

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