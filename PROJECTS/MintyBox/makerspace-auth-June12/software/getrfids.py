#!/usr/bin/env python
####
#
# FYI, this is god awful.  I wish it hadn't been implemented this way
# fortunately Elijah is re-writing the backend so we can burn this garbage
# down for the tire-fire it is.
#
###
import os
import sha
import sys
from datetime import datetime

import requests 

secret = os.getenv("FATT_SECRET")
URL = os.getenv("FATT_URL")

def reqhash(unixtime):
    """
    method: stuff
    returns: hash
    """

    if not URL:
        raise Exception("Environment Variable FATT_URL is not defined")

    if not secret:
        raise Exception("Environment Variable FATT_SECRET is not defined")

    # First, calculate a sha1 hash of the supplied unixtime
    ut_hash = sha.new(unixtime).hexdigest()
    # Next, calculate a sha1 hash of the supplied secret
    sec_hash = sha.new(secret).hexdigest()
    # Finally, catenate the two previous hashes together and rehash
    req_hash = sha.new(ut_hash + sec_hash).hexdigest()
    return req_hash

def getrfids():
    """
    """
    ut = datetime.now().strftime("%s")
    x = reqhash(ut)
    payload = {'ts': ut, 'hs': x}
    
    #response = requests.get(URL, params=payload, verify=False)
    try:
        response = requests.get(URL, params=payload)
    except requests.exceptions.Timeout:
    # Maybe set up for a retry, or continue in a retry loop
        print("Timeout connecting to URL")
        sys.exit(1) 
    except requests.exceptions.TooManyRedirects:
    # Tell the user their URL was bad and try a different one
        print "Invalid URL, exiting"
        sys.exit(1)
    except requests.exceptions.RequestException as e:
        print e
        sys.exit(1)
    rfids = response.json()[1]
    return rfids

def cacheRFIDs(rfids, filename="authorized.txt"):
    file = open(filename, "w+")
    for token in rfids:
        file.write(token + "\n")


def main():
    r = getrfids()

    #print("Total of {} RFID fobs".format(len(r)))
    cacheRFIDs(r)



if __name__ == '__main__':
    main()

# vim: ts=4 sw=4 et
