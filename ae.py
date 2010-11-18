#!/usr/bin/python

import sys, os, subprocess, re, shutil
import cookielib
import urllib2
import string
import random
import time

from libs import libmms

if len(sys.argv) == 1:
    urlsstrings = open("urls.txt", "r").read()
    urls = open("urls.txt", "w")
    urls.write("\n".join(urlsstrings.split('\n')[1:]))
    urls.close()
    urlsstring = urlsstrings.split('\n')[0]
else:
    urlsstring = sys.argv[1]

piece = 2 # minutes
threads = 10

folder = "./downloads"
folder_id = re.search(r".+\/\d+\/(.+)-porn-videos\.html", urlsstring, re.M).group(1)

if os.path.exists("%s/%s.wmv" % (folder, folder_id)):
    print "%s/%s.wmv exists" % (folder, folder_id)
    sys.exit()

try:
    os.mkdir("%s/%s" % (folder, folder_id))
except:
    pass

time = int(time.time())
mail = "%s@%s.com" % ("".join([random.choice(string.letters) for x in range(8)]), "".join([random.choice(string.letters) for x in range(8)]))
password = "".join([random.choice(string.letters) for x in range(8)])

# print mail
# print password

cj = cookielib.LWPCookieJar()

c_urlopen = urllib2.build_opener(
    urllib2.HTTPHandler(debuglevel=0),
    urllib2.HTTPCookieProcessor(cj),
)
urllib2.install_opener(c_urlopen)

# Registration >>>
request = urllib2.Request("https://www.adultempire.com/Account/CreateAccount?callback=jsonp%s&_=%s&email=%s&passWord=%s&userName=%s&keepLogged=false&salt=%s" % (time, time, mail, password, mail, time))
request.add_header('Accept', '*/*')
response = c_urlopen.open(request)
# print response.read()

request = urllib2.Request("https://www.adultempire.com/Account/Login?callback=jsonp%s&_=%s&userName=%s&passWord=%s&keepLogged=false&salt=%s" % (time, time, mail, password, time))
request.add_header('Accept', '*/*')
response = c_urlopen.open(request)
# print response.read()

request = urllib2.Request("https://www.adultempire.com/Account/ForcePromotion?callback=jsonp%s&_=%s" % (time, time))
request.add_header('Accept', '*/*')
response = c_urlopen.open(request)
# print response.read()
# Registration <<<

request = urllib2.Request("%s?viewPart=VideoPlayer" % (urlsstring))
request.add_header('Accept', '*/*')
response = c_urlopen.open(request)
d = response.read()

mms_link = re.search(r"http:\/\/stream\d+\.dvdempire\.com\/.+stream_type=1", d, re.M).group(0)
# print mms_link

request = urllib2.Request(mms_link)
request.add_header('Accept', '*/*')
response = c_urlopen.open(request)
d = response.read()

mms = re.search(r"mms:\/\/video\d+\.dvdempire\.com\/.+stream_type=1", d, re.M).group(0)
# print mms

stream = libmms.Stream(mms, 1e6)
duration = stream.duration()
length = stream.length()

pieces     = int(duration/(piece*60))
piece_size = int(length/pieces/1024) # kBytes

if len(sys.argv) == 1:
    f = open("run/%s.sh" % (folder_id), "w")
    for c in range(0, pieces+1):
        if c > 0 and c % threads == 0:
            f.write("python wait.py \"%s/%s\"\n" % (folder, folder_id))
        f.write("python ae.py \"%s\" %s &\n" % (urlsstring, c))
    f.write("python wait.py \"%s/%s\" && python join.py \"%s/%s\"\n" % (folder, folder_id, folder, folder_id))
    f.close()
    
    s = open("run/%s.sh" % (folder_id), "r").read()
    p = subprocess.Popen(s, stdout=subprocess.PIPE, shell=True)
    os.waitpid(p.pid, 0)
    
    shutil.rmtree("%s/%s" % (folder, folder_id))
else:
    file_piece = int(sys.argv[2])
    stream.seek(file_piece*piece_size*1024)
    
    flock = open("%s/%s/lock.%s" % (folder, folder_id, file_piece), "w")
    flock.close()
    
    f = open("%s/%s/part.%s" % (folder, folder_id, str(file_piece).rjust(4, str(0))), "w")
    i = 0
    for data in stream:
        f.write(data)
        i = i+1
        if i == piece_size:
            break
    f.close()
    
    os.unlink("%s/%s/lock.%s" % (folder, folder_id, file_piece))
