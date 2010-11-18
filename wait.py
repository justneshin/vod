#!/usr/bin/python

import sys, os, re
import time

time.sleep(60)

do = True
while do:
    do = False
    
    search = re.compile("lock\.\d+$", re.IGNORECASE)
    files = os.listdir(sys.argv[1])
    check = [f for f in files if search.search(f)]
    
    if check:
        do = True
        time.sleep(10)
