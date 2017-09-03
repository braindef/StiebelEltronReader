#coding=utf-8
import argparse
import time
import os.path
import requests
import sys
import re

#auf UTF-8 Zeichensatz einstellen
reload(sys)
sys.setdefaultencoding('utf8')


#Adresse der Webseite(n)
#---------------------------------------------------------------------------
url1 = '****ADRESSE****'		#Adresse der Steuerung bzw. des Webinterfaces
url2 = url1 + '?s=1,0'
url3 = url1 + '?s=1,1'

#Benutzername und Passwort
payload = {'make': 'send','user': '****BENUTZERNAME****','pass': '****PASSWORT****'}
#---------------------------------------------------------------------------


#Alle Verfügbaren Werte (Keys) um die Werte (Values) abzufragen, falls die Steuerungssoftware geändert wird muss das angepasst werden
allKeys = ["SOLLTEMPERATUR HK 1","SOLLTEMPERATUR HK 2","ISTTEMPERATUR","SOLLTEMPERATUR","BIVALENZTEMPERATUR HZG",
"BIVALENZTEMPERATUR WW","VERFLÜSSIGERTEMP.","DRUCK HEIZKREIS","VOLUMENSTROM","LEISTUNG WP",
"LSTG PU PUMPE","AUSSENTEMPERATUR","ISTTEMPERATUR HK 1","SOLLTEMPERATUR HK 1","ISTTEMPERATUR HK 2",
"SOLLTEMPERATUR HK 2","VORLAUFISTTEMPERATUR WP","VORLAUFISTTEMPERATUR NHZ","RÜCKLAUFISTTEMPERATUR",
"FESTWERTSOLLTEMPERATUR","PUFFERSOLLTEMPERATUR","PUFFERISTTEMPERATUR","RESTSTILLSTANDZEIT","VD HEIZEN",
"VD WARMWASSER","NHZ 1","NHZ 2","VD HEIZEN TAG","VD HEIZEN SUMME",
"VD WARMWASSER TAG","VD WARMWASSER SUMME","NHZ HEIZEN SUMME"]


#Aktuelle Stunde als Zeitstempel, da sich die Heizung träge verhält macht es keinen Sinn mehr als 1x die Stunde abzufragen
currentHour = time.strftime("%Y%m%d%H")
filename = './'+currentHour+'.dump'

#Aktueller Monat als Dateiname für die CSV Datei, Pro Monat eine Datei
currentMonth = time.strftime("%Y%m")
filenameCSV = './Heizung_'+currentMonth+'.csv'
#print filename


#Eingabeparameter verarbeiten
# Instantiate the parser
def parseArgs():
	parser = argparse.ArgumentParser(description='Liest Werte aus Stiebel Elron Webinterface aus aufruf z.B: $ python get.py --live "PUFFERISTTEMPERATUR"')
	#parser.add_argument('--csv', action="store_true", default=False, help='gibt alle Daten als CSV aus')
	parser.add_argument('--middle', action="store", dest="middle", help='gibt die Mittelwerte von der Startseite aus')
	parser.add_argument('--live', action="store", dest="specific", help='gibt die Live Werte aus')
	args = parser.parse_args()
	#print ("csv: %s", args.csv)
	#
	if not (args.middle is None):
	#	print ("middle: %s", args.middle)
		getMiddle(args.middle)
	if not (args.specific is None):
	#	print ("Spezifisch: %s", args.specific)
		print getLive(args.specific)


#Hole die drei Werteseiten von der STIEBEL ELTRON Webseite v2.5.6
def getFile():
	response1 = requests.post(url1, data=payload, headers={'Connection':'close'})
	response2 = requests.post(url2, data=payload, headers={'Connection':'close'})
	response3 = requests.post(url3, data=payload, headers={'Connection':'close'})

	file = open(filename, 'w')
	file.write(response1.content)
	file.write(response2.content)
	file.write(response3.content)
	file.close()

#gibt die abgefragten Webseiten der Steuerung aus (nur für Testzwecke)
def printResponse():
	print(response1.text)
	print(response1.status_code)

	print(response2.text)
	print(response2.status_code)

	print(response3.text)
	print(response3.status_code)


#Hole die Mittelwerte aus dem gespeicherten File
def getMiddle(value):
	with open(filename, 'r') as fin:
		for line in fin:
			if re.search('charts', line):
				##print line
				if re.search('mittel', line):
					print line.split(",")[11].split("]")[0]


#Hole die Live Daten aus dem gespeicherten File
def getLive(value):
	#print value
	with open(filename, 'r') as fin:
		for line in fin:
			if re.search(">"+value+"<", line):
				return fin.next().split(">")[1].split(" ")[0].replace(",",".");


#fügt alle aktuelle Werte zum CSV dazu
def addToCSV():
	if not os.path.exists(filenameCSV):		#Header in die CSV Datei schreiben falls sie neu erstellt wurde
		with open(filenameCSV, 'a') as fout:
			fout.write("Date")
			for i in allKeys:
				fout.write(","+i)
			fout.write("\n")
			fout.close()

	with open(filenameCSV, 'a') as fout:		#Akutelle Werte in die CSV schreiben
		fout.write(time.strftime("%Y %m %d %H:%M:%S"))
		for i in allKeys:
			fout.write(","+getLive(i))
		fout.write("\n")




#-----------------------------------------
# MAIN: Hauptprogramm, hier startet alles
#-----------------------------------------
if not os.path.exists(filename):#Holt das Datenfile vom Server wenn es diese Stunde nicht schon einmal geholt wurde und die Datei schon existiert
	getFile()		
	addToCSV()		#Fügt die Daten dem CSV hinzu
parseArgs()			#je nach Aufrufparameter (Args) wird dann die Funktion für den Entsprechenden wert aufgerufen


