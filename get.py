import requests
import sys

reload(sys)
sys.setdefaultencoding('utf8')

url = 'IP ADRESSE oder URL des Servers'
payload = {'make': 'send','user': 'BENUTZERNAME','pass': 'PASSWORT'}

r = requests.post(url, data=payload)

print(r.text)
print(r.status_code)

