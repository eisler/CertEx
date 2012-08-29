#!/usr/bin/env python

LOGFILE = "LOGFILE"
TMPCERTFILE = "tmp.pem"

import os
from optparse import OptionParser 
import subprocess


def getFileEndings(p="."):
    fel = []   
    tmp = "" 
    for e in os.walk(p, True):
        for ending in e[2]:
            tmp = ending.rpartition(".")[2]
            if not(tmp in fel):
                fel.append(tmp)  
    return fel

def createLogfile():
    file = open(LOGFILE, 'w+')
    return file

def createCertFile(dir = "."):
    if not(os.path.isdir(dir)):
        os.mkdir(dir)
    file = open(dir + "/" + TMPCERTFILE, 'w+')
    return file

def createOutPutFIle(p):
    datei = open("./" + p + ".txt", "w")
    return datei

def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False

def parseDigResultToKey(digResult):
    foundSome = False;
    digResult = digResult.rpartition("CERT")[2]
    digResult = digResult.partition(url)[0]
    digResult = digResult.partition(";")[0]
    digResult = digResult.split()

    key = ""
    key2 = ""

    for str in digResult:
        if(len(str)>10):
            foundSome = True
            key +=str
        else:
            if(foundSome):
                if(len(str) > 7):
                    key +=str  
                    break

    counter = 0
    for c in key:
        key2 += c
        if(counter == 63):
            key2 += "\n"
            counter = 0
        else:
            counter += 1

    key3 = "-----BEGIN CERTIFICATE----- \n"        
    key3 += key2
    key3 += "\n-----END CERTIFICATE-----"    
    return key3


#!/usr/bin/env python

parser = OptionParser()
parser.add_option("-p", "--Path", dest="path", help="path u want tu save the digResult")
parser.add_option("-u", "--URL", dest="url", help="URL u want to scan")
(optionen, args) = parser.parse_args()
PATH = optionen.path
url = optionen.url

if (url is None or len(url) == 0): # check if url is given
    parser.error('Url is required')
    


logfile = createLogfile()
digResult = subprocess.check_output(["dig", "any" , url])
logfile.write(digResult)
logfile.close()

key = parseDigResultToKey(digResult)

f = createCertFile()
f.write(key)
f.close()

tmpcert = ""

try:
    tmpcert = subprocess.check_output(["openssl", "x509", "-text", "-in", TMPCERTFILE])
except subprocess.CalledProcessError, e:
    print"Keiner Zertifikat gefunden... Falls Sie sich sicher sind, dass ein valides Zertifikat existiert."
    print("Senden Sie bitte das Logfile an: constantin.tschuertz@1un1.de")
    #os.system("rm" + tmpcert)

os.remove(TMPCERTFILE)

if(len(tmpcert) != 0):
    if(PATH is None):
        print(tmpcert)
    else:
        f = createOutPutFIle(PATH)
        f.write(tmpcert)
        f.close()
        
    

