#!/usr/bin/env python

'''
This script will hit the /host REST API endpoint and query for an IP address in an attempt to gain
more insight into what the public IP address is used for.

Notes: 
  Ipblock - contains general info: address, description (sometimes), owner (sometimes)
  RR - DNS A records section (not always there): name, zone
'''

import getpass
import sys
import urllib
import urllib2
import xml.etree.ElementTree as ET

URL = "http://netdot.example.com"

def main():
    hostData = lookupHost()
    hostDict = parseXml(hostData)
    printData(hostDict)

def getCreds():
    username = raw_input("Username: ")
    password = getpass.getpass("Password: ")
    return username, password

def lookupHost():
    loginUrl = URL + "/netdot/NetdotLogin"
    username, password = getCreds()
    hostIp = sys.argv[1]
    queryUrl = URL + "/netdot/rest/host?address="+hostIp
    values = {
            'destination' : '/netdot/',
            'credential_0' : username,
            'credential_1' : password
            }

    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor())
    urllib2.install_opener(opener)
    data = urllib.urlencode(values)
    f = opener.open(loginUrl, data)
    data = f.read()
    f.close()
    f = opener.open(queryUrl)
    data = f.read()
    f.close()
    return data

def parseXml(xml):
    dictionary = {}
    root = ET.fromstring(xml)

    for ipblock in root.iter('Ipblock'):
        dictionary['Address'] = ipblock.attrib['address']
        if ipblock.attrib['description']:
            dictionary['Description'] = ipblock.attrib['description']
        if ipblock.attrib['owner']:
            dictionary['Owner'] = ipblock.attrib['owner']
    for rr in root.iter('RR'):
        if rr.attrib['name']:
            name = rr.attrib['name']
            zone = rr.attrib['zone']
            dictionary['Hostname'] = name + zone
    
    return dictionary

def printData(dictionary):
    for k, v in dictionary.items():
        print k + ": " + v

if __name__ == "__main__":
    main()
