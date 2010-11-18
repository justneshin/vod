#!/usr/bin/python

import sys, os, subprocess

files = []
for filepart in os.listdir(sys.argv[1]):
    files.append('"%s/%s"' % (sys.argv[1], filepart))
files.sort()

s = "cat %s > %s.wmv" % (" ".join(files), sys.argv[1])
p = subprocess.Popen(s, stdout=subprocess.PIPE, shell=True)
os.waitpid(p.pid, 0)
