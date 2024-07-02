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


site_ids = []
kill_input = ""
print("Please provide the site ids you wish to add these rules too :" "\n")

while True:
    line = input()
    if line == kill_input:
        break
    site_ids.extend(line.strip().split(","))


#Everything in the param "filter=" correlates to the actual syntax of the rule being created the "name=" param is the name of the rule 
# name="Block%20TOR%20and%20Anon" correlates to the rule name "Block TOR and Anon" : filter="MaliciousIPList%20%3D%3D%20AnonymousProxyIPs%20%7C%20MaliciousIPList%20%3D%3D%20TorIPs" correlates to "MaliciousIPList == AnonymousProxyIPs | MaliciousIPList == TorIPs"
# name="IP%20Reputation"IPReputationRiskLevel%20%3D%3D%20High%20%26%20ClientIP%20%21%3D%20209.134.130.138%3B209.134.157.10%3B65.122.49.226%3B65.214.41.35" correlates to "IPReputationRiskLevel == High & ClientIP != 209.134.130.138;209.134.157.10;65.122.49.226;65.214.41.35"

# Names of Common Rules we use and their params


Block_MG4_Card = "Block%20MG4%20Card"
Block_MG4_Card_Param = "ClientIP%20%3D%3D%200.0.0.0%2F0"

IP_Reputation = "IP%20Reputation"
IP_Reputation_Param = "IPReputationRiskLevel%20%3D%3D%20High%20%26%20ClientIP%20%21%3D%20209.134.130.138%3B209.134.157.10%3B65.122.49.226%3B65.214.41.35"

Block_Tor_and_Anon = "Block%20TOR%20and%20Anon"
Block_Tor_and_Anon_Param = "MaliciousIPList%20%3D%3D%20AnonymousProxyIPs%20%7C%20MaliciousIPList%20%3D%3D%20TorIPs"

DDoS_RPS_Alert = "DDoS%20Proactive%20Threshold%20Warning"
DDoS_RPS_Alert_Param = ""

#Rule Action
rule_action = input("Will the rule action be block/alert? :""\n")
rule_action_alert = "RULE_ACTION_ALERT"
rule_action_block = "RULE_ACTION_BLOCK"


if rule_action == "block":
    rule_action = rule_action_block

if rule_action == "alert":
    rule_action = rule_action_alert

incap_rule = input("Do you want to apply IP Rep/Block Tor/Block IP/RPS Alert? :""\n")

if incap_rule == "Block IP":
    Block_IP = input("Please provide the IP you wish to block :""\n")
    incap_rule = f"ClientIP%20%3D%3D%20{Block_IP}"
    rule_name = f"Block%20{Block_IP}%20Change%20Ticket%20178343"

if incap_rule == "IP Rep":
    incap_rule = IP_Reputation_Param
    rule_name = IP_Reputation

if incap_rule == "Block Tor":
    incap_rule = Block_Tor_and_Anon_Param
    rule_name = Block_Tor_and_Anon

if incap_rule == "RPS Alert":
    RPS = input("Please provide the RPS you wish to alert on :""\n")
    DDoS_RPS_Alert_Param = f"SiteRequestRate%20%3D%3D%20{RPS}"
    incap_rule = DDoS_RPS_Alert_Param
    rule_name = DDoS_RPS_Alert

site_to_rule_id = []

for site_id in site_ids:

    api_url = (f"https://my.imperva.com/api/prov/v1/sites/incapRules/add?action={rule_action}&site_id={site_id}&name={rule_name}&filter={incap_rule}")

    response = ssl_supressed_session().post(api_url, headers=headers, verify=False)

    response_content = response.content

    # Regex pattern to match rule_id
    rule_id_pattern= (r'"rule_id":"(\d+)"')

    # Search for rule_id in response content
    match_rule_id = re.search(rule_id_pattern, response_content.decode())

    rule_id = match_rule_id.group(1)

    site_to_rule_id.append({'SiteID': site_id, 'RuleID': rule_id})

    print(f"Site ID {site_id} response status code {response.status_code}")
    print(f"Rule: {rule_id} has been added to Site: {site_id}")

data_frame = pandas.DataFrame(site_to_rule_id)
excel_file_name = 'SiteToRuleID.xlsx'
data_frame.to_excel(excel_file_name, index=False)

print("Please check the SiteToRuleID.xlsx file for the Site to Rule ID mapping")


#https://management.service.imperva.com/my/sites/rules/manage?extSiteId=37519257&id=2191120&caid=782530