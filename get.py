import requests
import sys
import re

reload(sys)
sys.setdefaultencoding('utf8')                                             #deutschen Zeichensatz einstellen

url1 = 'URL'                                                               #URL1
url2 = 'URL?s=1,1'                                                         #URL2
url3 = 'URL?s=1,0'                                                         #URL3

payload = {'make': 'send','user': 'BENUTZERNAME','pass': 'PASSWORT'}       #Benutzername und Passwort

                                                                           #übermittle den Payload mit dem Benutzer und
                                                                           #passwort und empfange die Server-Antworten
response1 = requests.post(url1, data=payload, headers={'Connection':'close'})
response2 = requests.post(url2, data=payload, headers={'Connection':'close'})
response3 = requests.post(url3, data=payload, headers={'Connection':'close'})

print(response1.text)                                                      #Drucke die Server Antworten
#print(response1.status_code)

print(response2.text)
#print(response2.status_code)

print(response3.text)
#print(response3.status_code)



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
