#bin/bash
cd /etc/zabbix/externalscripts

/usr/bin/python get.py $1 "$2"
