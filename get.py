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
url1 = 'http://*****URL*****'		#Adresse der Steuerung bzw. des Webinterfaces
url2 = url1 + '?s=1,0'
url3 = url1 + '?s=1,1'

#Benutzername und Passwort
payload = {'make': 'send','user': '*****USERNAME*****','pass': '*****PASSWORD*****'}
#---------------------------------------------------------------------------


#Alle Verfügbaren Werte (Keys) um die Werte (Values) abzufragen, falls die Steuerungssoftware geändert wird muss das angepasst werden
allKeys = ["SOLLTEMPERATUR HK 1","SOLLTEMPERATUR HK 2","ISTTEMPERATUR","SOLLTEMPERATUR","BIVALENZTEMPERATUR HZG",
"BIVALENZTEMPERATUR WW","VERFLÜSSIGERTEMP.","DRUCK HEIZKREIS","VOLUMENSTROM","LEISTUNG WP",
"LSTG PU PUMPE","AUSSENTEMPERATUR","ISTTEMPERATUR HK 1","SOLLTEMPERATUR HK 1","ISTTEMPERATUR HK 2",
"SOLLTEMPERATUR HK 2","VORLAUFISTTEMPERATUR WP","VORLAUFISTTEMPERATUR NHZ","RÜCKLAUFISTTEMPERATUR",
"FESTWERTSOLLTEMPERATUR","PUFFERSOLLTEMPERATUR","PUFFERISTTEMPERATUR","RESTSTILLSTANDZEIT","VD HEIZEN",
"VD WARMWASSER","NHZ 1","NHZ 2","VD HEIZEN TAG","VD HEIZEN SUMME",
"VD WARMWASSER TAG","VD WARMWASSER SUMME","NHZ HEIZEN SUMME"]

#Aktueller Monat als Dateiname für die CSV Datei, Pro Monat eine Datei
currentMonth = time.strftime("%Y%m")
filenameCSV = './Heizung_'+currentMonth+'.csv'

#Aktueller Zeitstempel, da sich die Heizung träge verhält macht es keinen Sinn mehr als 1x alle 10 Min abzufragen
currentHour = time.strftime("%Y%m%d%H")+str(int(time.strftime("%M"))/10)
filename = './'+currentMonth+'/'+currentHour+'.dump'
#print filename

#print filename


#Eingabeparameter verarbeiten
# Instantiate the parser
def parseArgs():
	parser = argparse.ArgumentParser(description='Liest Werte aus Stiebel Elron Webinterface aus aufruf z.B: $ python get.py --live "PUFFERISTTEMPERATUR"')
	#parser.add_argument('--csv', action="store_true", default=False, help='gibt alle Daten als CSV aus')
	parser.add_argument('--history', action="store", dest="history", help='gibt den gestrigen Mittelwerte von der Startseite aus, Parameter: MIN,MIDDLE,MAX,HEIZEN,WARMWASSER')
	parser.add_argument('--live', action="store", dest="live", help='gibt die Live Werte aus')
	args = parser.parse_args()
	if not (args.history is None):
		if (args.history=="MIN"):
			print getMin()
		if (args.history=="MIDDLE"):
			print getMiddle()
		if (args.history=="MAX"):
			print getMax()
		if (args.history=="HEIZEN"):
			print getHeizen()
		if (args.history=="WARMWASSER"):
			print getWarmwasser()
			
	if not (args.live is None):
	#	print ("Spezifisch: %s", args.specific)
		print getLive(args.live)


#Hole die drei Werteseiten von der STIEBEL ELTRON Steuerunngs Webseite v2.5.6
def getFile():
	response1 = requests.post(url1, data=payload, headers={'Connection':'close'})
	response2 = requests.post(url2, data=payload, headers={'Connection':'close'})
	response3 = requests.post(url3, data=payload, headers={'Connection':'close'})

	file = open(filename, 'w')
	file.write(response1.content)  #hänge die drei dateien aneinander
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


#Hole die Temparatur Minimalwerte aus dem gespeicherten File
def getMin():
	with open(filename, 'r') as fin:
		for line in fin:
			if re.search('charts', line):
				##print line
				if re.search('min', line):
					return line.split(",")[11].split("]")[0]

#Hole die Temparatur Mittelwerte aus dem gespeicherten File
def getMiddle():
	with open(filename, 'r') as fin:
		for line in fin:
			if re.search('charts', line):
				##print line
				if re.search('mittel', line):
					return line.split(",")[11].split("]")[0]

#Hole die Temparatur Maximalwerte aus dem gespeicherten File
def getMax():
	with open(filename, 'r') as fin:
		for line in fin:
			if re.search('charts', line):
				##print line
				if re.search('max', line):
					return line.split(",")[11].split("]")[0]

#Hole die Temparatur Mittelwerte aus dem gespeicherten File
def getHeizen():
	with open(filename, 'r') as fin:
		for line in fin:
			if re.search('charts\[2\]', line):
				##print line
				if re.search('line', line):
					return line.split(",")[11].split("]")[0]

#Hole die Temparatur Mittelwerte aus dem gespeicherten File
def getWarmwasser():
	with open(filename, 'r') as fin:
		for line in fin:
			if re.search('charts\[3\]', line):
				if re.search('line', line):
					return line.split(",")[11].split("]")[0]


#Hole die Live Daten aus dem gespeicherten File
def getLive(value):
	#print value
	with open(filename, 'r') as fin:
		for line in fin:
			if re.search(">"+value+"<", line): #suche nach ">NAMEDERVARIABEL<"
				return fin.next().split(">")[1].split(" ")[0].replace(",",".");


#fügt alle aktuelle Werte zum CSV dazu
def addToCSV():
	if not os.path.exists(filenameCSV):		#Header in die CSV Datei schreiben falls sie neu erstellt wurde
		with open(filenameCSV, 'a') as fout:
			fout.write("Date")
			for i in allKeys:
				fout.write(","+i)
			fout.write(",MIN,MIDDLE,MAX,HEIZEN,WARMWASSER")
			fout.write("\n")
			fout.close()

	with open(filenameCSV, 'a') as fout:		#Akutelle Werte in die CSV schreiben
		fout.write(time.strftime("%Y-%m-%d %H:%M:%S"))
		for i in allKeys:
			fout.write(","+getLive(i))
		fout.write(","+getMin()) #history Daten
		fout.write(","+getMiddle())
		fout.write(","+getMax())
		fout.write(","+getHeizen())
		fout.write(","+getWarmwasser())
		fout.write("\n")


#-----------------------------------------
# MAIN: Hauptprogramm, hier startet alles
#-----------------------------------------
if not os.path.exists("./"+currentMonth):
	os.makedirs("./"+currentMonth)
if not os.path.exists(filename):#Holt das Datenfile vom Server wenn es diese Stunde nicht schon einmal geholt wurde und die Datei schon existiert
	getFile()		
	addToCSV()		#Fügt die Daten dem CSV hinzu
parseArgs()			#je nach Aufrufparameter (Args) wird dann die Funktion für den Entsprechenden wert aufgerufen


