import requests
import sys
import re

reload(sys)
sys.setdefaultencoding('utf8')                                             #deutschen Zeichensatz einstellen

url = 'URL'                                                                #URL
payload = {'make': 'send','user': 'BENUTZERNAME','pass': 'PASSWORT'}       #Benutzername und Passwort

response = requests.post(url, data=payload)                                #übermittle den Payload mit dem Benutzer und
                                                                           #passwort und empfange die Server-Antwort
#print(response.text)                                                      #Drucke die Server Antwort
#print(response.status_code)

for line in response:                                                      #für jede zeile der Serverantwort mache:
	if re.search('charts', line):                                      #suche nach dem Wort charts
		##print line                                               #gib Zeile aus
		if re.search('mittel', line):                              #suche nach dem wort mittel
			print line.split(",")[11].split("]")[0]            #trenne die Zeile bei den kommas und nimm
			                                                   #die 11 spalte, trenne davon beim ] und nimm die
				                                           #erste spalte

# Beispiel einer Zeile:
#  charts[1]['mittel'] = [['Sa',22.4],['So',20.9],['Mo',21.5],['Di',21.7],['Mi',22.3],['Do',16.8],['Fr',13.9]];
# Programm liefert somit 16.8 als Ausgabe für die Verwendung in beliebiger anderer Software z.B. Nagios oder Zabbix Monitoring
