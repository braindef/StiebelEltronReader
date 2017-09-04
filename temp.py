#coding=utf-8
import argparse
import time
import os.path
import requests
import sys
import re

currentHour = time.strftime("%Y%m%d%H")+str(int(time.strftime("%M"))/10)
filename = './'+currentHour+'.dump'
print filename
