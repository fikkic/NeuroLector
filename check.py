import requests
import urllib3


urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

url = "https://ngw.devices.sberbank.ru:9443/api/v2/oauth"

payload={
  'scope': 'GIGACHAT_API_PERS'
}
headers = {
  'Content-Type': 'application/x-www-form-urlencoded',
  'Accept': 'application/json',
  'RqUID': '019c41e7-e8c3-75e4-835f-c1920ea1c1f0',
  'Authorization': 'Basic MDE5YzQxZTctZThjMy03NWU0LTgzNWYtYzE5MjBlYTFjMWYwOjc4NDg2NzBhLWI3YWQtNDM0ZS1hOTllLTNmOGU3ZTI1ZTljMg=='
}

response = requests.request("POST", url, headers=headers, data=payload, verify=False)

print(response.text)
