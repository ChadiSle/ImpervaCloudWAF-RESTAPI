import requests
import re
import pandas


# Set your API credentials
headers = {
    "Content-Type": "application/json",
    "Accept-Encoding": "gzip, deflate, br",
    "Connection": "keep-alive",
    "x-api-id": "",
    "x-api-key": ""
    
}


# Adjust the header variable names to reflect the name of the accounts you will most commonly be working on and the credentials you will need for them.


SiteConfiguration_Report = []

site_ids = []
kill_input = ""
print("Please provide the site ids you wish to extract the config data for:" "\n")

while True:
    line = input()
    if line == kill_input:
        break
    site_ids.extend(line.strip().split(","))


# Regex patterns to grab report info

DDoS_Threshold_Pattern= (r'"ddos_traffic_threshold":(\d+)')
SiteID_Pattern = (r'"site_id":(\d+)')
Activation_Mode_Pattern = (r'"activation_mode_text"\s*:\s*"([^"]*)"')
Domain_Pattern = (r'"domain":"([^"]+)"')
Custom_Cert_Pattern = (r'"custom_certificate"\s*:\s*\{\s*"active"\s*:\s*(true|false)')
Origin_Info_Pattern = (r'"ips"\s*:\s*\[(.*?)\]')
Imperva_CNAME_Pattern = (r'"set_data_to":\["([^"]+)"\]')
Support_All_TLS_Pattern = (r'"support_all_tls_versions"\s*:\s*(true|false)')
Use_Wildcard_SAN_Pattern = (r'"use_wildcard_san_instead_of_full_domain_san"\s*:\s*(true|false)')
SQL_Injection_Pattern =(r'\{\s*"action"\s*:\s*"[^"]*",\s*"action_text"\s*:\s*"([^"]+)"[^}]*?"name"\s*:\s*"SQL Injection"')
XSS_Pattern = (r'\{\s*"action"\s*:\s*"[^"]*",\s*"action_text"\s*:\s*"([^"]+)"[^}]*?"name"\s*:\s*"Cross Site Scripting"')
IRA_Pattern = (r'\{\s*"action"\s*:\s*"[^"]*",\s*"action_text"\s*:\s*"([^"]+)"[^}]*?"name"\s*:\s*"Illegal Resource Access"')
RFI_Pattern = (r'\{\s*"action"\s*:\s*"[^"]*",\s*"action_text"\s*:\s*"([^"]+)"[^}]*?"name"\s*:\s*"Remote File Inclusion"')
Backdoor_Protect_Pattern = (r'\{\s*"action"\s*:\s*"[^"]*",\s*"action_text"\s*:\s*"([^"]+)"[^}]*?"name"\s*:\s*"Backdoor Protect"')
API_Specification_Violation_Pattern = (r'\{\s*"action"\s*:\s*"[^"]*",\s*"action_text"\s*:\s*"([^"]+)"[^}]*?"name"\s*:\s*"API Specification Violation"')
BlockBadBots_Pattern = (r'"block_bad_bots"\s*:\s*(true|false)')
UnknownClientsChallenge_Pattern = (r'"unknown_clients_challenge"\s*:\s*"([^"]+)"')
BlockNonEssentialBots_Pattern = (r'"block_non_essential_bots"\s*:\s*(true|false)')
ChallengeSuspectedBots_Pattern = (r'"challenge_suspected_bots"\s*:\s*(true|false)')
AddNakedDomainSAN_Pattern = (r'"add_naked_domain_san"\s*:\s*(true|false)')
SiteStatus_Pattern = (r'"status"\s*:\s*"([^"]+)"')

for site_id in site_ids:

    api_url = (f"https://my.imperva.com/api/prov/v1/sites/status?site_id={site_id}")

    response = requests.post(api_url, headers=headers, verify=False)

    response_content = response.content

    print(response.status_code)
    print(response_content)    
    print(site_id)

    # Match all relevant information

    match_SiteStatus = re.search(SiteStatus_Pattern, response_content.decode())
    SiteStatus = match_SiteStatus.group(1)

    match_DDoS_Threshold = re.search(DDoS_Threshold_Pattern, response_content.decode())
    if match_DDoS_Threshold == None:

        DDoS_Threshold = "N/A"
    else: 
        DDoS_Threshold = match_DDoS_Threshold.group(1)

    match_UnknownClientsChallenge = re.search(UnknownClientsChallenge_Pattern, response_content.decode())
    if match_UnknownClientsChallenge == None:

        UnknownClientsChallenge = "N/A"
    else: 
        UnknownClientsChallenge = match_UnknownClientsChallenge.group(1)

    match_BlockNonEssentialBots = re.search(BlockNonEssentialBots_Pattern, response_content.decode())
    if match_BlockNonEssentialBots == None:

        BlockNonEssentialBots = "N/A"
    else: 
        BlockNonEssentialBots = match_BlockNonEssentialBots.group(1)

    match_ChallengeSuspectedBots = re.search(ChallengeSuspectedBots_Pattern, response_content.decode())
    if match_ChallengeSuspectedBots == None:

        ChallengeSuspectedBots = "N/A"
    else: 
        ChallengeSuspectedBots = match_ChallengeSuspectedBots.group(1)

    match_Support_All_TLS = re.search(Support_All_TLS_Pattern, response_content.decode())
    if match_Support_All_TLS == None:

        Support_All_TLS = "N/A"
    else:
        Support_All_TLS = match_Support_All_TLS.group(1)

    match_Use_Wildcard_SAN = re.search(Use_Wildcard_SAN_Pattern, response_content.decode())
    Use_Wildcard_SAN = match_Use_Wildcard_SAN.group(1)

    match_AddNakedDomainSAN = re.search(AddNakedDomainSAN_Pattern, response_content.decode())
    AddNakedDomainSAN = match_AddNakedDomainSAN.group(1)

    match_Imperva_CNAME = re.search(Imperva_CNAME_Pattern, response_content.decode())
    Imperva_CNAME = match_Imperva_CNAME.group(1)

    match_Origin_Info = re.search(Origin_Info_Pattern, response_content.decode())
    Origin_Info = match_Origin_Info.group(1)

    match_Custom_Cert = re.search(Custom_Cert_Pattern, response_content.decode())
    Custom_Cert = match_Custom_Cert.group(1)

    match_SiteID = re.search(SiteID_Pattern, response_content.decode())
    SiteID = match_SiteID.group(1)

    match_Activation_Mode = re.search(Activation_Mode_Pattern, response_content.decode())
    Activation_Mode = match_Activation_Mode.group(1)

    match_Domain = re.search(Domain_Pattern, response_content.decode())
    Domain = match_Domain.group(1)

    match_SQL_Injection = re.search(SQL_Injection_Pattern, response_content.decode())
    if match_SQL_Injection == None:

        SQL_Injection = "Exceptions Exists"
    else:
        SQL_Injection = match_SQL_Injection.group(1)

    match_XSS = re.search(XSS_Pattern, response_content.decode())
    if match_XSS == None:
        XSS = "Exceptions Exist"
    else:
        XSS = match_XSS.group(1)

    match_IRA = re.search(IRA_Pattern, response_content.decode())
    if match_IRA == None:
        IRA = "Exceptions Exist"
    else:
        IRA = match_IRA.group(1)

    match_RFI = re.search(RFI_Pattern, response_content.decode())
    if match_RFI == None:
        RFI = "Exceptions Exist"
    else:
        RFI = match_RFI.group(1)

    match_Backdoor_Protect = re.search(Backdoor_Protect_Pattern, response_content.decode())
    if match_Backdoor_Protect == None:
        Backdoor_Protect = "N/A"
    else:
        Backdoor_Protect = match_Backdoor_Protect.group(1)

    match_API = re.search(API_Specification_Violation_Pattern, response_content.decode())
    if match_API == None:
        API_Specification_Violation = "N/A"
    else:
        API_Specification_Violation = match_API.group(1)

    match_BlockBadBots = re.search(BlockBadBots_Pattern, response_content.decode())
    if match_BlockBadBots == None:
        BlockBadBots = "N/A"
    else:
        BlockBadBots = match_BlockBadBots.group(1)

    SiteConfiguration_Report.append({'Site ID': site_id, 'Domain': Domain, 'Configuration': SiteStatus, 'Imperva CNAME': Imperva_CNAME, 'Origin Info': Origin_Info, 'DDoS Threshold': DDoS_Threshold, 'DDoS Activation Mode': Activation_Mode, 'Uses Wildcard SAN': Use_Wildcard_SAN, 'Uses Naked Domain SAN': AddNakedDomainSAN, 'Custom Cert': Custom_Cert, 'Support All TLS Versions': Support_All_TLS, 'SQL Injection': SQL_Injection, 'Cross Site Scripting': XSS, 'Illegal Resource Access': IRA, 'Remote File Inclusion': RFI, 'Backdoor Protect': Backdoor_Protect, 'API Specification Violation': API_Specification_Violation, 'Block Bad Bots': BlockBadBots, 'Challenge Suspected Bots': ChallengeSuspectedBots, 'Unknown Clients Challenge': UnknownClientsChallenge, 'Block Non Essential Bots': BlockNonEssentialBots})


data_frame = pandas.DataFrame(SiteConfiguration_Report)
excel_file_name = 'SiteConfiguration_Report.xlsx'
data_frame.to_excel(excel_file_name, index=False)

print("Please check the SiteConfiguration_Report.xlsx file for requested information")