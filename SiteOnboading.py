import requests
import re
import pandas
import openpyxl


# Set your API credentials and other Headers
#api_id = input("Please Enter your API ID :""\n")
#api_key = input("Please Enter your API Key :""\n")

headers = {
    "Content-Type": "application/json",
    "Accept-Encoding": "gzip, deflate, br",
    "Connection": "keep-alive",
    "x-api-id": "",
    "x-api-key": ""
    
}
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

account_id = input("Which account will you be onboarding to? Sinevis/Shared Subaccount/Chadi Subaccount? :""\n")

if account_id == "Sinevis":
    account_id = 1747036

elif account_id == "Shared Subaccount":
    account_id = 1855439

elif account_id == "Chadi Subaccount":
    account_id = 2091311

#if using Advanced Config ie specifying the DNS
advanced_config = input("Will you be defining the origin IP/CNAME Yes/No :""\n")

if advanced_config == "Yes" or advanced_config == "yes":

    appgw_cname_or_IP = input("Please provide the IP/CNAME :""\n")

#When setting up sites prior to them having valid DNS, specify the IP/CNAME by appending "&site_ip=" to the api_url. For example: "/sites/add?domain=example.imperva.com&account_id=10&send_site_setup_emails=True&site_ip=1.2.3.4&log_level=full"
#If you are specifying IP/CNAME you will also have to force SSL by adding "&force_ssl=True" to the api_url, its also efficient to add "&log_level=full"
    for domain in domains:

        api_url = (f"https://my.imperva.com/api/prov/v1/sites/add?domain={domain}&account_id={account_id}&send_site_setup_emails=True&site_ip={appgw_cname_or_IP}&force_ssl=True&log_level=full")

        response = requests.post(api_url, headers=headers, verify=False)

        print(api_url)

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

        response = requests.post(api_url, headers=headers, verify=False)

        print(api_url)

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
