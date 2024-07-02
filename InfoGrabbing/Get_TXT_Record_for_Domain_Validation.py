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
print("Please provide the Site IDs you want the TXT Records for:" "\n")
while True:
    line = input()
    if line == kill_input:
        break
    site_ids.extend(line.strip().split(","))

TXT_Record_Info = []

for site_id in site_ids:
    
    api_url = (f"https://my.imperva.com/api/prov/v1/sites/status?site_id={site_id}&tests=domain_validation")

    response = requests.post(api_url, headers=headers, verify=False)

    print(response.status_code)
    response_content = response.content

    contentInSTR = response_content.decode('utf-8')

    print(contentInSTR)

    
    if response.status_code == 200:

        pattern1 = r'"set_type_to":"TXT","set_data_to":\["([^"]+)"\]'
        pattern2 = r'"domain":"([^"]+)"'
        pattern3 = r'"dns_record_name":"([^"]+)"'
    
        matchTXT = re.search(pattern1, contentInSTR)
        matchDomain = re.search(pattern2, contentInSTR)
        matchDNSrecordName = re.search(pattern3, contentInSTR)

        if matchTXT:
            set_data_to = matchTXT.group(1)
            domain = matchDomain.group(1)
            dns_record_name = matchDNSrecordName.group(1)

            print("dns_record_name:", dns_record_name)
            print("set_data_to:", set_data_to)
            print("domain:", domain)
            TXT_Record_Info.append({'Site ID':site_id, 'Domain':domain, 'DNS Record Name': dns_record_name, 'TXT Record':set_data_to})
            
            
        else: print(f"No Match Found")

            
data_frame = pandas.DataFrame(TXT_Record_Info)
excel_file_name = 'TXT_to_Domain_Info.xlsx'
data_frame.to_excel(excel_file_name, index=False)

print("Please check the TXT_to_Domain_Info.xlsx file for the TXT Record Info")
