#!/bin/bash
cat output3.txt |grep charts.2...line|cut -d\' -f11 |cut -d, -f2 |cut -d] -f1
