import requests
import sys
import re

reload(sys)
sys.setdefaultencoding('utf8')

url = 'URL'
payload = {'make': 'send','user': 'BENUTZERNAME','pass': 'PASSWORT'}

response = requests.post(url, data=payload)

#print(response.text)
#print(response.status_code)

for line in response:
	if re.search('charts', line):
		##print line
		if re.search('mittel', line):
			print line.split(",")[11].split("]")[0]
