#!/usr/bin/python
#-*-coding=utf-8
# 

import sys
import json 
import urllib2
import urllib
import cookielib
from collections import OrderedDict


def getLicense(applyCode):

    cj = cookielib.LWPCookieJar()
    cookie_support = urllib2.HTTPCookieProcessor(cj)
    opener = urllib2.build_opener(cookie_support, urllib2.HTTPHandler)
    urllib2.install_opener(opener)
    
    loginUrl = "http://url"
    
    loginPostData = urllib.urlencode({"username":"","password":""})
    loginRequest = urllib2.Request(loginUrl, loginPostData)
    loginRequest.add_header("User-Agent", "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:26.0) Gecko/20100101 Firefox/26.0")
    try:
        loginResponse = urllib2.urlopen(loginRequest)
        # print loginResponse.info()
        # print loginResponse.read()
    except urllib2.HTTPError, e:
        print e.getcode()
        print e.geturl()
        # print "-------------------------"
        # print e.info()
        # print e.read()
    
    licenseUrl = "http://url"
    licensePostData = OrderedDict((("contract","dfg"),("customer","sd"),("note","sdf"),("type","dbackup4"),("state",1),
        ("useday",60),("code",applyCode)))
    licensePostData["properties"] = [OrderedDict((("name","clientnum"),("value",10))),
        OrderedDict((("name","limit"),("value","3"))),
        OrderedDict((("name","authosdb"),("value",8),("pre_value","1O"))),
        OrderedDict((("name","authosdb"),("value",5),("pre_value","2O"))),
        OrderedDict((("name","authosdb"),("value",5),("pre_value","3O"))),
        OrderedDict((("name","authosdb"),("value",5),("pre_value","4O"))),
        OrderedDict((("name","authosdb"),("value",5),("pre_value","5O"))),
        OrderedDict((("name","authosdb"),("value",5),("pre_value","1S"))),
        OrderedDict((("name","authosdb"),("value",5),("pre_value","1M"))),
        OrderedDict((("name","authosdb"),("value",5),("pre_value","2M"))),
        OrderedDict((("name","authosdb"),("value",5),("pre_value","1A"))),
        OrderedDict((("name","authosdb"),("value",5),("pre_value","2A"))),
        OrderedDict((("name","authosdb"),("value",5),("pre_value","3A"))),
        OrderedDict((("name","authosdb"),("value",5),("pre_value","4A"))),
        OrderedDict((("name","authosdb"),("value",5),("pre_value","5A"))),
        OrderedDict((("name","standbyosdb"),("value",5),("pre_value","1O"),("multiple",2))),
        OrderedDict((("name","standbyosdb"),("value",5),("pre_value","2O"),("multiple",2))),
        OrderedDict((("name","standbyosdb"),("value",5),("pre_value","3O"),("multiple",2))),
        OrderedDict((("name","standbyosdb"),("value",5),("pre_value","4O"),("multiple",2))),
        OrderedDict((("name","standbyosdb"),("value",5),("pre_value","5O"),("multiple",2))),
        OrderedDict((("name","standbyosdb"),("value",5),("pre_value","1S"),("multiple",2))),
        OrderedDict((("name","standbyosdb"),("value",5),("pre_value","1M"),("multiple",2))),
        OrderedDict((("name","standbyosdb"),("value",5),("pre_value","2M"),("multiple",2)))]
    
    licensePostData2 = json.dumps(licensePostData, separators=(',',':'))
    licenseRequest = urllib2.Request(licenseUrl, licensePostData2, {'Content-Type': 'application/json'})
    licenseRequest.add_header("User-Agent", "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:26.0) Gecko/20100101 Firefox/26.0")
    try:
        licenseResponse = urllib2.urlopen(licenseRequest)
        # print licenseResponse.info()
        getLicense = json.loads(licenseResponse.read())
        return getLicense['license']
    except urllib2.HTTPError, e:
        print e.getcode()
        print e.geturl()
        # print "-------------------------"
        # print e.info()
        # print e.read()
    loginResponse.close()
    licenseResponse.close()
    
if __name__ == '__main__':
    
    license = getLicense(sys.argv[1]) 
    print "Get the License is : \n %s" % license
