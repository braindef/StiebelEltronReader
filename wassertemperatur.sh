#!/bin/bash
cat output3.txt |grep jsobj |grep val24a -A1 |grep \'val\' |cut -d\' -f4

