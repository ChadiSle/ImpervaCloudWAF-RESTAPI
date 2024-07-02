#DDoS Proactive Threshold Warning Compliance Report
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

headers = input("Which Imperva Tenant are you searching? Wex Health/Wex Inc? :""\n")

if headers == "Wex Health" or headers == "wex health" or headers == "Wex health" or headers == "wex Health" or headers == "Wex Helth":
    headers = Wex_Health_headers

elif headers == "Wex Inc" or headers == "wex inc" or headers == "Wex inc" or headers == "Wex Corp":
    headers = Wex_Inc_headers


site_ids = []
kill_input = ""
print("Please provide the Site IDs you want to Audit for DDoS Alerting:" "\n")
while True:
    line = input()
    if line == kill_input:
        break
    site_ids.extend(line.strip().split(","))

incap_rule_id_info = []

for site_id in site_ids:
    
    api_url = (f"https://my.imperva.com/api/prov/v1/sites/status?site_id={site_id}&tests=domain_validation")

    response = requests.post(api_url, headers=headers, verify=False)

    print(response.status_code)
    response_content = response.content

    contentInSTR = response_content.decode('utf-8')

    print(contentInSTR)

    
    if response.status_code == 200:


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
excel_file_name = 'DDoS_Proactive_Threshold_Alert_Audit.xlsx'
data_frame.to_excel(excel_file_name, index=False)

print("Please check the DDoS_Proactive_Threshold_Alert_Audit.xlsx file for the Site ID and Compliance Status")