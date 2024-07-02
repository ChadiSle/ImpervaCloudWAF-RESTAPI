import requests
import re
import pandas

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

headers = input("Which Imperva Tenant are you working on? Wex Health/Wex Inc? :""\n")

if headers == "Wex Health" or headers == "wex health" or headers == "Wex health" or headers == "wex Health" or headers == "Wex Helth":
    headers = Wex_Health_headers

elif headers == "Wex Inc" or headers == "wex inc" or headers == "Wex inc" or headers == "Wex Corp":
    headers = Wex_Inc_headers


DDoS_Report = []

site_ids = []
kill_input = ""
print("Please provide the site ids you wish to know the DDoS threshold for:" "\n")

while True:
    line = input()
    if line == kill_input:
        break
    site_ids.extend(line.strip().split(","))



for site_id in site_ids:

    api_url = (f"https://my.imperva.com/api/prov/v1/sites/status?site_id={site_id}")

    response = requests.post(api_url, headers=headers, verify=False)

    response_content = response.content

    # Regex pattern to match rule_id
    DDoS_Threshold_Pattern= (r'"ddos_traffic_threshold":(\d+)')
    SiteID_Pattern = (r'"site_id":(\d+)')
    Activation_Mode_Pattern = (r'"activation_mode_text"\s*:\s*"([^"]*)"')
    Domain_Pattern = (r'"domain":"([^"]+)"')


    # Match all relevant information
    match_DDoS_Threshold = re.search(DDoS_Threshold_Pattern, response_content.decode())
    DDoS_Threshold = match_DDoS_Threshold.group(1)

    match_SiteID = re.search(SiteID_Pattern, response_content.decode())
    SiteID = match_SiteID.group(1)

    match_Activation_Mode = re.search(Activation_Mode_Pattern, response_content.decode())
    Activation_Mode = match_Activation_Mode.group(1)

    match_Domain = re.search(Domain_Pattern, response_content.decode())
    Domain = match_Domain.group(1)

    DDoS_Report.append({'SiteID': site_id, 'Domain': Domain, 'DDoS_Threshold': DDoS_Threshold, 'DDoS_Activation_Mode': Activation_Mode})

    print(response.status_code)

data_frame = pandas.DataFrame(DDoS_Report)
excel_file_name = 'DDoS_Report.xlsx'
data_frame.to_excel(excel_file_name, index=False)

print("Please check the DDoS_Report.xlsx file for requested information")





