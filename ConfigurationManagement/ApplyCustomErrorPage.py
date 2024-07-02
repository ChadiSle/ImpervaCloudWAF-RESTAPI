import requests
import json


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
print("Please provide the site ids you wish to add/remove this Custom Error Page to :" "\n")

while True:
    line = input()
    if line == kill_input:
        break
    site_ids.extend(line.strip().split(","))

print(site_ids)

Custom_Error_HTML = '''
<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta http-equiv="X-UA-Compatible" content="ie=edge">
    <title>Wex Health - Maintenance Page</title>
    <style type="text/css">
      body {
        color: #000000;
      }
	  
	  .hidden {
		height: 0;
		padding: 0;
		margin: 0;
        visibility: hidden;
	  }
	  
	  .maintenance {
		font-weight: bold;
	  }
  
      .container {
        width: -webkit-fit-content;
        width: -moz-fit-content;
        width: fit-content;
        max-width: 100%;
        margin: 0 auto;
        padding: 15px;
      }
  
      .container-inner {
        background: #FFFFFF;
        box-shadow: 0 10px 10px rgba(0, 0, 0, 0.1);
        border-radius: 8px;
      }
  
      .header {
        width: 100%;
        background: #F3F3F3;
        border-radius: 8px 8px 0 0;
        display: flex;
        align-items: center;
      }
  
      .error-description {
        padding: 35px 42px;
        font-size: 14px;
        font-weight: 500;
        color: #232323;
      }
  
      .error-description .error-title {
        line-height: 17px;
        margin-bottom: 4px;
      }
  
      .error-description .error-code {
        font-weight: bold;
        font-size: 32px;
        line-height: 39px;
        margin-bottom: 4px;
      }
  
      .error-description .hostname {
        line-height: 20px;
        margin-bottom: 2px;
      }
  
      .error-description .date {
        line-height: 17px;
        color: #727272;
      }
  
      .main {
        padding: 42px;
      }
  
      .troubleshooting {
        display: flex;
        flex-direction: row;
      }
  
      .troubleshooting .title {
        font-weight: bold;
        font-size: 18px;
        line-height: 22px;
        margin-bottom: 17px;
      }
  
      .troubleshooting .content {
        flex-basis: 100%;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
        min-width: 0;
      }
  
      .troubleshooting .content .description {
        line-height: 18px;
        margin-bottom: 35px;
      }
  
      .troubleshooting .parentheses-text {
        color: #727272;
      }
  
      .info-container .info {
        line-height: 15px;
      }
  
      .info-container .info:not(:last-child) {
        margin-bottom: 8px;
      }
  
      .info-container .info .value {
        color: #285AE6;
      }
  
      .powered-by {
        margin-top: 18px;
        display: flex;
        align-items: center;
        justify-content: center;
      }
  
      .powered-by .copyrights {
        color: #000000;
        text-decoration: none;
        font-size: 0;
      }
  
      .powered-by .copyrights::before {
        display: inline-block;
        content: url("data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iNTgiIGhlaWdodD0iMTYiIHZpZXdCb3g9IjAgMCA1OCAxNiIgZmlsbD0ibm9uZSIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj4KPHBhdGggZmlsbC1ydWxlPSJldmVub2RkIiBjbGlwLXJ1bGU9ImV2ZW5vZGQiIGQ9Ik0wLjYzNDkwMyAyLjMxMTQ5SDIuOTQ2MzlWMEgwLjYzNDkwM1YyLjMxMTQ5Wk01NS45NjY1IDEyLjg0MzVINTQuODEwOVYxNS4xNTQ2SDU3LjEyMjRWMTIuODQzNUg1NS45NjY1WiIgZmlsbD0iIzI4NUFFNiIvPgo8bWFzayBpZD0ibWFzazAiIG1hc2stdHlwZT0iYWxwaGEiIG1hc2tVbml0cz0idXNlclNwYWNlT25Vc2UiIHg9IjAiIHk9IjMiIHdpZHRoPSI1OCIgaGVpZ2h0PSIxMyI+CjxwYXRoIGZpbGwtcnVsZT0iZXZlbm9kZCIgY2xpcC1ydWxlPSJldmVub2RkIiBkPSJNMC42MzQ5MDMgMy4yMjQ2NEg1Ny4xMjI1VjE1LjE1ODdIMC42MzQ5MDNWMy4yMjQ2NFoiIGZpbGw9IndoaXRlIi8+CjwvbWFzaz4KPGcgbWFzaz0idXJsKCNtYXNrMCkiPgo8cGF0aCBmaWxsLXJ1bGU9ImV2ZW5vZGQiIGNsaXAtcnVsZT0iZXZlbm9kZCIgZD0iTTU0LjgxMSA4Ljg3MjI0QzU0LjYwNTkgOC40MjQ4NSA1My45OTExIDguMTQ1MjcgNTMuMzM4MiA4LjE0NTI3QzUyLjYxMTYgOC4xNDUyNyA1MS44NjU4IDguNDYyMDkgNTEuODY1OCA5LjE3MDY1QzUxLjg2NTggOS44OTc2MiA1Mi42MTE2IDEwLjE5NTYgNTMuMzM4MiAxMC4xOTU2QzUzLjk5MTEgMTAuMTk1NiA1NC42MDU5IDkuOTE2MDQgNTQuODExIDkuNDY5MDVWOC44NzIyNFpNNTQuODEwOCA2LjU0MzAzQzU0LjgxMDggNS43NDE1NiA1NC4xMjExIDUuMjM4NDkgNTIuOTQ3MiA1LjIzODQ5QzUyLjEwOCA1LjIzODQ5IDUxLjMyNSA1LjQ4MDgxIDUwLjY3MjkgNS45MDkzOFYzLjkxNDcyQzUxLjI2OTMgMy41NDIyMiA1Mi4zNTA0IDMuMjI1NCA1My40NTAyIDMuMjI1NEM1NS43NDI5IDMuMjI1NCA1Ny4xMjIzIDQuMzk5NzcgNTcuMTIyMyA2LjQzMTI4VjExLjc0NEg1NC44MTA4VjExLjI5NjZDNTQuNTMxMyAxMS41NzYyIDUzLjcxMSAxMS44OTMgNTIuNzk3OCAxMS44OTNDNTEuMTIwMyAxMS44OTMgNDkuNzIyIDEwLjkyMzcgNDkuNzIyIDkuMTkwMTdDNDkuNzIyIDcuNjA1NjUgNTEuMTIwMyA2LjUyNDYxIDUyLjk0NzIgNi41MjQ2MUM1My42NzM3IDYuNTI0NjEgNTQuNDc1MiA2Ljc2NjkzIDU0LjgxMDggNy4wMDkyNVY2LjU0MzAzWk00NC40MTk0IDExLjc0NDdMNDEuMjY5MiAzLjQxMjM5SDQzLjY5MjVMNDUuNjEyNiA4Ljk0ODU4TDQ3LjQ5NTEgMy40MTIzOUg0OS44MjVMNDYuNjU2NCAxMS43NDQ3SDQ0LjQxOTRaTTQwLjgyNzQgNS42ODU4OUM0MC41MTA2IDUuNDk5MjMgNDAuMTAwNCA1LjQwNjMyIDM5LjY3MTkgNS40MDYzMkMzOC44ODg4IDUuNDA2MzIgMzguMjU1MiA1LjgxNjA2IDM4LjA4NzMgNi41ODA2OVYxMS43NDRIMzUuNzc1OFYzLjQxMTY1SDM4LjA4NzNWNC4yMzE5NUMzOC40NDE0IDMuNjM1NTUgMzkuMTMxMSAzLjIyNTQgMzkuOTUxNCAzLjIyNTRDNDAuMzQyOCAzLjIyNTQgNDAuNjk2OCAzLjI5OTkgNDAuODI3NCAzLjM3NDRWNS42ODU4OVpNMjkuMjM5MyA2LjU5OTFIMzIuMzg5NUMzMi4zMzM0IDUuNzA0MyAzMS44MzAzIDUuMDcwNjYgMzAuOTE3MSA1LjA3MDY2QzMwLjE1MjUgNS4wNzA2NiAyOS41IDUuNTU1MyAyOS4yMzkzIDYuNTk5MVpNMjkuMTY1MiA4LjEwOTEzQzI5LjM1MTQgOS40NzAxNSAzMC4zMzk2IDEwLjAyODkgMzEuNTY5NiAxMC4wMjg5QzMyLjQ4MzIgMTAuMDI4OSAzMy4xMzUzIDkuODI0MjIgMzMuOTU1NiA5LjMwMjMyVjExLjIwMzNDMzMuMjY1OSAxMS43MDY3IDMyLjMzMzggMTEuOTMwMiAzMS4yMTU1IDExLjkzMDJDMjguNjgwNiAxMS45MzAyIDI2Ljk0NjYgMTAuMjkgMjYuOTQ2NiA3LjY0MzMxQzI2Ljk0NjYgNS4wMzM0MiAyOC41ODcyIDMuMjI1NCAzMC44NjExIDMuMjI1NEMzMy4yODQ3IDMuMjI1NCAzNC41MzM2IDQuOTAyODQgMzQuNTMzNiA3LjM2MzMzVjguMTA5MTNIMjkuMTY1MlpNMjAuMTcwOSA4Ljk0ODZDMjAuNDUwOSA5LjUyNjU3IDIxLjA2NTcgOS45MTc4OSAyMS43MzcgOS45MTc4OUMyMi45ODU4IDkuOTE3ODkgMjMuNzMxMiA4LjkxMTM1IDIzLjczMTIgNy41ODc5OEMyMy43MzEyIDYuMjQ1NzkgMjIuOTg1OCA1LjIzOTI0IDIxLjczNyA1LjIzOTI0QzIxLjA0NzMgNS4yMzkyNCAyMC40NTA5IDUuNjQ5MzkgMjAuMTcwOSA2LjIwODU0VjguOTQ4NlpNMjAuMTcxMSAxNS4xNTk0SDE3Ljg2VjMuNDExNjVIMjAuMTcxMVY0LjEwMTM3QzIwLjU0NCAzLjY1Mzk3IDIxLjM2NDMgMy4yMjU0IDIyLjI1OTEgMy4yMjU0QzI0LjY4MjMgMy4yMjU0IDI2LjA2MTggNS4yMzg0OSAyNi4wNjE4IDcuNTg3MjNDMjYuMDYxOCA5LjkzNTk3IDI0LjY4MjMgMTEuOTMwMiAyMi4yNTkxIDExLjkzMDJDMjEuMzY0MyAxMS45MzAyIDIwLjU0NCAxMS41MDE3IDIwLjE3MTEgMTEuMDU0M1YxNS4xNTk0Wk0xMy42MzQ4IDMuMjI1NEMxNS4zNDk5IDMuMjI1NCAxNi4zNzQ4IDQuNDE4MTkgMTYuMzc0OCA2LjMwMTExVjExLjc0NEgxNC4wNjM4VjYuNzg1NzZDMTQuMDYzOCA1Ljg5MDk2IDEzLjY3MiA1LjI5NDU3IDEyLjg3MDYgNS4yOTQ1N0MxMi4yNzQyIDUuMjk0NTcgMTEuNzMzNCA1LjY2NzA2IDExLjU4NDQgNi4zNzU2MVYxMS43NDRIOS4yNTQxMlY2Ljc4NTc2QzkuMjU0MTIgNS44OTA5NiA4Ljg4MTYzIDUuMjk0NTcgOC4wODAxNiA1LjI5NDU3QzcuNDgzMzYgNS4yOTQ1NyA2LjkyNDIxIDUuNjY3MDYgNi43NzUyMiA2LjM3NTYxVjExLjc0NEg0LjQ2MzczVjMuNDExNjVINi43NzUyMlY0LjEwMTM3QzcuMTg1MzcgMy41Nzk0NyA3Ljk0OTU5IDMuMjI1NCA4Ljg4MTYzIDMuMjI1NEM5Ljg2OTM1IDMuMjI1NCAxMC42NTI0IDMuNjcyOCAxMS4xMTgyIDQuMjg4MDNDMTEuNjU4OSAzLjY5MTIyIDEyLjQ2MDQgMy4yMjU0IDEzLjYzNDggMy4yMjU0Wk0yLjk0NjA3IDExLjc0NDdIMC42MzQ5ODdWMy40MTIzOUgxLjc5MDUzSDIuOTQ2MDdWMTEuNzQ0N1oiIGZpbGw9IiMyODVBRTYiLz4KPC9nPgo8L3N2Zz4K")
      }
  
      .powered-by .text {
        font-weight: 300;
        font-size: 11px;
        font-style: italic;
        line-height: 15px;
        margin-right: 10px;
      }
  
      @media (min-width: 768px) {
        .container {
          width: 817px;
          max-width: 100%;
        }
      }
  
      @media (max-width: 767px) {
        .container {
          width: 507px;
        }
      }
  
      @media (max-width: 400px) {
        .container {
          padding: 0;
        }
  
        .error-description .error-code {
          font-size: 26px;
        }
      }
    </style>
  </head>
  <body>
    <div class="container">
	  <div class="maintenance">
		Please excuse us while the system is undergoing enhancements and is temporarily unavailable.
		<br />
		We will be back up and running again before long, so please try again later.
		<br />
		Thank you for your patience.
	  </div>
      <div class="container-inner hidden">
        <div class="header">
          <div class="error-description">
            $TITLE$
          </div>
        </div>
        <div class="main">
          <div class="troubleshooting">
            <div class="content">
              $BODY$
            </div>
          </div>
        </div>
      </div>
      <div class="powered-by hidden">
        <span class="text">Powered by</span>
        <a href="https://www.imperva.com/why-am-i-seeing-this-page/?src=23&amp;utm_source=blockingpages" target="_blank" class="copyrights">Imperva</a>
      </div>
    </div>
  </body>
</html>
'''

data_add = {
    "custom_error_page": {
    "error_page_template": "",
    "custom_error_page_templates": {
      "error.type.access_denied": Custom_Error_HTML
    }
    }
}
data_delete = {
    "custom_error_page": {
    "error_page_template": "",
    "custom_error_page_templates": {
      "error.type.access_denied": ""
    }
    }
}
Add_Remove = input("Add or Remove Custom Error Page? (A/R): ")

if Add_Remove == "A":
    data = data_add
elif Add_Remove == "R":
    data = data_delete

for site_id in site_ids:

    api_url = (f"https://my.imperva.com/api/prov/v2/sites/{site_id}/settings/delivery")

    # YOU NEED TO REMEMBER WHEN YOUR DATA SHOULD BE JSON, USE JSON.DUMPS() TO CONVERT IT TO JSON
    response = requests.put(api_url, headers=headers, data=json.dumps(data), verify=False)

    print(f"Site ID {site_id} response status code {response.status_code}")

    if response.status_code == 200 and Add_Remove == "A" :
        print("Custom Error Page Added Successfully")

    elif response.status_code == 200 and Add_Remove == "R" :
        print("Custom Error Page Removed Successfully")

    else: 
        print(response.content)