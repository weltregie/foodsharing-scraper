#!/usr/bin/python
# -*- coding: utf-8 -*-
import requests
import string
import time

from email.mime.text import MIMEText
from subprocess import Popen, PIPE

from BeautifulSoup import BeautifulSoup

foodcart_ids = []
loop = 1

myheaders = {}
myheaders['User-Agent'] = "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:19.0) Gecko/20100101 Firefox/19.0"

while True:
    r = requests.get('http://foodsharing.de/staedte/berlin', headers = myheaders)
    soup = BeautifulSoup(r.text)
    results = soup.findAll('tr', attrs = {'class': 'foodcart-entry'})
    
    for result in results:
        name = result.findAll('strong', attrs = {'class': 'font size-large'})
        link = result.findAll('a')
        #for n in name:
        #    print n.contents[0]
        for l in link:
            linkpath = l.get('href')
            foodcart_id = string.split(linkpath, '/')[-1:][0]
            #print "http://foodsharing.de" + linkpath
            if foodcart_id not in foodcart_ids:
                foodcart_ids.append(foodcart_id)
                # send mail
                msg = MIMEText('http://foodsharing.de' + linkpath)
                msg['To'] = 'lists@weltregie.org'
                msg['Subject'] = 'Neuer Essenskorb, id ' + str(foodcart_id)
                p = Popen(['/usr/sbin/sendmail', '-t'], stdin = PIPE)
                p.communicate(msg.as_string())
                print '--> Neuer Essenskorb:', 'http://foodsharing.de' + linkpath 
    print "Durchlauf", loop, ':', foodcart_ids
    loop += 1
    time.sleep(60)
