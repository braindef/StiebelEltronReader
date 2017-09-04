# Stiebel Eltron Webinterface Reader (German)
### Reads the values from Stiebler Elteron Webinterface and parses it to a format that can be read by zabbix monitoring with external scripts (Tested so far on v2.5.6)
if you want to use it in English or other Languages you must change the Keywords like "SOLLTEMPERATUR" to your language in the Zabbix Template (See **Zabbix Configuration**)

There seems to be a thing that must be added:
there are twice the Value SOLLTEMPERATUR HK 1, SOLLTEMPERATUR HK 2
guess one menas german "Heizkessel" and the other means german "Heizkörper"
->I will change that later to "SOLLTEMPERATUR Heizkörper 1" and "SOLLTEMPERATUR Heizkessel 1"

To install:
1. Install Zabbix on eg. a Debian Server
2. run **git clone https://github.com/braindef/StiebelEltronReader** in the folder /etc/zabbix/externalscripts
3. lazy variant: run **chown -R zabbix.zabbix /etc/zabbix/externalscripts**
4. Copy get.sh and get.py to **/etc/zabbix/externalscripts**
5. Set URL, Username and Password in get.py
6. import the *Template zbx_export_Heizung.xml* with your zabbix interface
7. Customize a screen for your Solution

![alt text](https://raw.githubusercontent.com/braindef/StiebelEltronReader/master/AuwertungMitZabbix.png "Output")

-For **installing Zabbix** see: http://marclandolt.ch/ml_buzzernet/2017/06/03/zabbix-on-debian-stretch/

-For **installing Debian** use Google: "installing Debian Stretch" or see my Video: https://www.youtube.com/watch?v=GvW4kpUvRiU

-If you want to **monitor your SNMP-Devices** / Switches With Zabbix see https://www.youtube.com/watch?v=kkipRMrNW2o

## Zabbix Configuration

![alt text](https://raw.githubusercontent.com/braindef/StiebelEltronReader/master/AuwertungMitZabbix.png "Output")

## Security Considerations

It is a bad idea to use this script and also the Webinterface over the internet since it is completely not encrypted except you use a https proxy and access over HTTPS or if you just use it at home over a wired connection or an encrypted WiFi

![alt text](https://raw.githubusercontent.com/braindef/StiebelEltronReader/master/password.png "password")
As you can easy see with **wireshark** and the function **follow tcp stream**

At the moment you can get these values with my python script:

![alt text](https://raw.githubusercontent.com/braindef/StiebelEltronReader/master/webinterface1.png "Webinterface 1")

![alt text](https://raw.githubusercontent.com/braindef/StiebelEltronReader/master/webinterface2.png "Webinterface 2")

And of course you can do this also over RS232, MODbus or CANbus, but the chance that you brick your controller unit is IMHO much bigger then and it is also more complicated to get the correct values and units. Since Stiebel Eltron did this already i decided to use this way.

Have Fun!
