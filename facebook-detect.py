#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import os
import sys
sys.path.append( '/home/ec2-user/lib')

import cv, cv2
import numpy as np 
import urllib2
import tempfile 
import os, shutil
import json
import cgitb
cgitb.enable()

class ReturnValue: 
    facebook_image = False
    omeagel_image = False
    myeecards_image = False
	

print "Content-Type: text/plain;charset=utf-8"
print


def match_template(img, template_path): 
    # load the template image
    template = cv2.imread(template_path)

    # look for the template image inside of the loaded image
    result = cv2.matchTemplate(image,template,cv2.TM_CCOEFF_NORMED)

    # filter for only matches above the specified confidence level
    confidence = 0.75
    match_indices = np.arange(result.size)[(result>confidence).flatten()]
    return len(match_indices)

# grab the first argument, this is the url of the image to test
srcimg = sys.argv[1]

# create a temp file to hold the downloaded file
fd, path = tempfile.mkstemp() 

# download the file, write it to the temp path
print "Downloading file at:", srcimg
print ""
filedata = urllib2.urlopen(srcimg)
os.write(fd, filedata.read())
os.close(fd)

# load the image
image = cv2.imread(path)

# grab the symbols and iterate through them
symboldir = "fbsymbols/"
listing = os.listdir(symboldir)

is_facebook_img = False

for infile in listing:
    if infile[0]==".":
        print "skipping ", infile
        continue
    print "matching against:", infile
    count = match_template(image, symboldir+infile)
    print "Matches found: ", count
    if count > 0: 
        is_facebook_img = True
    
print json.dumps(is_facebook_img)
print ""
if is_facebook_img:
    print "I have determined that this IS a Facebook screen capture."
else:
    print "I have determined that this IS NOT a Facebook screen capture."
