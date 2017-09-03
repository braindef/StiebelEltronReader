#coding=utf-8
#Benötigte Programmbibliotheken
import argparse
import time
import os.path
import requests
import sys
import re

reload(sys)
sys.setdefaultencoding('utf8')

#Angabe der Webseiten
url1 = 'URL'
url2 = url1+'?s=1,0'
url3 = url1+'?s=1,1'

#Benutzername und passwort
payload = {'make': 'send','user': 'USERNAME','pass': 'PASSWORD'}

#Aktuelle Stunde als Zeitstempel, da sich die Heizung träge verhält macht es keinen Sinn mehr als 1x die Stunde abzufragen
currentHour = time.strftime("%Y%m%d%H")
filename = './'+currentHour+'.dump'
#print filename


#Eingabeparameter verarbeiten
# Instantiate the parser
def parseArgs():
	parser = argparse.ArgumentParser(description='Liest Werte aus Stiebel Elron Webinterface aus')
	parser.add_argument('--csv', action="store_true", default=False, help='gibt alle Daten als CSV aus')
	parser.add_argument('--middle', action="store", dest="middle", help='gibt die Mittelwerte von der Startseite aus')
	parser.add_argument('--live', action="store", dest="specific", help='gibt die Live Werte aus')
	args = parser.parse_args()
	print ("csv: %s", args.csv)

	if not (args.middle is None):
		print ("middle: %s", args.middle)
		evaluateMiddle(args.middle)
	if not (args.specific is None):
		print ("Spezifisch: %s", args.specific)
		evaluateLive(args.specific)
	

#Hole das File von der STIEBEL ELTRON Webseite v2.5.6
def getFile():
	response1 = requests.post(url1, data=payload, headers={'Connection':'close'})
	response2 = requests.post(url2, data=payload, headers={'Connection':'close'})
	response3 = requests.post(url3, data=payload, headers={'Connection':'close'})

	file = open(filename, 'w')
	file.write(response1.content)  # python will convert \n to os.linesep
	file.write(response2.content)  # python will convert \n to os.linesep
	file.write(response3.content)  # python will convert \n to os.linesep
	file.close()  			# you can omit in most cases as the destructor will call it

#gibt die abgefragten Webseiten der Steuerung aus (nur für Testzwecke)
def printResponse():
	print(response1.text)
	print(response1.status_code)

	print(response2.text)
	print(response2.status_code)

	print(response3.text)
	print(response3.status_code)


#Werte die gespeicherte Datei aus
def evaluateMiddle(value):
	with open(filename, 'r') as fin:
		for line in fin:
			if re.search('charts', line):#
				##print line
				if re.search('mittel', line):
					print line.split(",")[11].split("]")[0]

def evaluateLive(value):
	print "test"

#Hole Wert mit dem namen der in der Variabel value gespeichert ist
def getValue(value):
	return "test"


parseArgs()

#Hauptprogramm
if not os.path.exists(filename):
	getFile()

