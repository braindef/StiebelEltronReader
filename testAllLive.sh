#!/bin/bash
IFS=$'\n' && for i in $(cat AlleFelder.txt); do python get.py --live "$i"; done
