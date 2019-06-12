#!/usr/bin/env python

__author__ =  "Blaze Sanders"
__email__ =   "blaze.d.a.sanders@gmail.com"
__company__ = "Ace Toy Company"
__status__ =  "Development"
__date__ =    "Late Updated: 2019-06-09"
__doc__ =     "GET and POST data from a JSON web API"

# Allow us to work with the JSON data format
import json

# urllib3 is a powerful, sanity-friendly HTTP client for Python
# https://urllib3.readthedocs.io/en/latest/
import urllib3

# Allow time travel :) and timestamp generation for data logging
# https://docs.python.org/3/library/time.html
# https://docs.python.org/3/library/datetime.html
import time
import datetime

# Constant to toggle debug print statements ON and OFF
DEBUG_STATEMENTS_ON = True

# TODO UPDATE THIS CONSTANT FOR EACH PROJECT!!!
# See https://nomcon.foballthethings.org/api/accesspoints/
THIS_PROJECTS_DEVICE_ID = 1 # =Minty Box 1

# Constant to manually adjust timezone project is running in, if internet not working
TIME_ZONE = 'CT' # or "PT or "Zulu"
INTERNET_TIME = 0
MANUAL_TIME = 1

# List of Device Names and ID that you can perform http.GET on
ACCESS_POINTS_URL = 'https://nomcon.foballthethings.org/api/accesspoints/'
# Define dictionary for parameters being sent to the ACCESS_POINTS_URL
ACCESS_POINTS_PARAMS = {'id': 'value', 'created_date': 'value','modified_date': 'value','name': 'value', 'location': 'value', 'verb': 'value'}
# The number of devices hardcoded into the AccessPoint API
MAX_NUMBER_OF_DEVICES = 8

# List of valid RFID fob UID's in hex format that you can perform http.GET on
CREDENTIALS_URL = 'https://nomcon.foballthethings.org/api/credentials/'
# Define dictionary for parameters being sent to the CREDENTAILS_URL
CREDENTIALS_PARAMS = {'id': 'value', 'created_date': 'value','modified_date': 'value', 'encodedCredential': 'value'}
# The number of IDs hardcoded into the Credentials API
MAX_NUMBER_OF_CREDENTIALS = 503
# This CONSTANT value is returned if credential is NOT FOUND
CREDENTIALS_ID_NOT_FOUND = -1

# Location for datalog that user RFID scans that you can perform http.POST on
DATA_LOG_URL = 'https://nomcon.foballthethings.org/api/activitylistings/'

# Highest level API URL
API_ENDPOINT = 'https://nomcon.foballthethings.org/api/'

# Security Key to allow POSTing to API
API_KEY = 'Token 2e77c0656e0549e4cefadfac979ccc622b98b07f'

# Django is uses one indexed arrays and Python uses zero index arrays
DJANGO_PYTHON_ARRAY_OFFSET = 1

# Highest level JSON value definitions
SwaggerHeaders = {  'Content-Type': 'application/json',
            'Accept': 'application/json',
            'Allow': 'GET, POST, HEAD, OPTIONS',
            'Authorization': 'Token 2e77c0656e0549e4cefadfac979ccc622b98b07f'}

###
# Calls standard Python 3 print("X") statement if DEBUG global variable is TRUE
#
# return NOTHING
###
def debugPrint(printMe):
    if(DEBUG_STATEMENTS_ON):
        #print("Database.py DEBUG STATEMENT:")
        print(printMe)
    else:
        print("/n") # PRINT NEW LINE

###
# Get current time
#
# @timeSource - Select INERNET_TIME or MANUAL_TIME contnts as true time of device
#
# return String variable with time formatted in iso8601 format
###
def getTime(timeSource):
    if(timeSource == INTERNET_TIME):
        timeStamp = time.time()
        iso8601DateTime = datetime.datetime.fromtimestamp(timeStamp).strftime('%Y-%m-%d %H:%M:%S')
        #debugPrint("Current Time is: " + iso8601DateTime)
        return iso8601DateTime
    elif(timeSource == MANUAL_TIME):
        debugPrint("TODO MANUAL TIME ZONE UPDATING")
        #TODO timezoneOffsett = ?-7? Zulu -7 or PT +3
        #TODO return iso8601DateTime + timeZoneOffset
    else:
        print("INVALID timeSource parameters sent to getTime method, please use INTERNET_TIME or MANUAL_TIME")


###
# Convert Django ONE indexed array notation into Python ZERO indexed array notation
#
# return interger value of expected index
###
def djangoToPythonIndexConversion(djangoIndex):
    return djangoIndex - DJANGO_PYTHON_ARRAY_OFFSET

###
# Convert Python ZERO indexed array notation into Django ONE indexed array notation
#
# return interger value of expected index
###
def pythonToDjangoIndexConversion(pythonIndex):
    return pythonIndex + DJANGO_PYTHON_ARRAY_OFFSET

class Database:

    ###
    # Constructor to initialize an Database object
    #
    # @self - Newly created object
    # @url - Highest level URL of API level you are attempting to read (GET) or write (POST) to
    #
    # url - URL documentation, not actually used in code (as of June 9, 2019)
    # httpObject - urlllib3 object used to perfom .request('POST') & .request('GET') commands
    # credentialsDict - Python Dictionary to hold fob ID whitelist locally
    #
    # return NOTHING
    ###
    def __init__(self, url):
        self.url = url
        self.httpObject = urllib3.PoolManager()
        self.credentialsDict = {}

    ###
    # Search credentialsDict (a python Dictionary) for HEX whitelisted fobIDs
    #
    # @fobID - HEX Fob UID you are searching for (e.g. 002AC13)
    #
    # Return Interger variable with database ID if fobID is in the  whitelist, -1 OTHERWISE
    ###
    def getAutoGeneratedDatabaseID(self, fobID):
        try:
            # Not optimized! Searches entire dictionary in O(1) time
            for id in range(0, MAX_NUMBER_OF_CREDENTIALS):
                if(self.credentialsDict[id]['encodedCredential'] == fobID):
                    return self.credentialsDict[id]['id']
        except IndexError as error:
            print("ERROR THERE ARE ONLY 503 CREDENTIALS")
            return CREDENTIALS_ID_NOT_FOUND
        except Exception as exception:
            print("SOMETHING WEIRD HAPPENED MOVE TO MARS!")
            return CREDENTIALS_ID_NOT_FOUND
        #return self.credentialsDict.get(fobID, "CREDENTIALS_ID_NOT_FOUND").id


    ###
    # POST data to https://nomcon.foballthethings.org/api/activitylistings/
    #
    # @id - Autofenerated database id to log
    #
    # return HTTP Status Code of POSY attempt (201 is good)
    ###
    def postDataLog(self, id):
        data = {'credential': id,
            'access_point': THIS_PROJECTS_DEVICE_ID}
        encoded_data = json.dumps(data).encode('UTF-8')
        dataToPOST = self.httpObject.request(   'POST',
                            DATA_LOG_URL,
                            body = encoded_data,
                            headers = SwaggerHeaders)
        http_status = dataToPOST.status

        #201 means data POSTed https://httpstatuses.com/201
        print(http_status)


    ###
    # GET data from https://nomcon.foballthethings.org/api/credentials/
    # and store in the Python Dictionary "crenedtialsDict" in Database object
    #
    # return NOTHING
    ###
    def getCredentials(self):

        fobWhiteList = self.httpObject.request( 'GET',
                            CREDENTIALS_URL,
                            CREDENTIALS_PARAMS)

        self.credentialsDict = json.loads(fobWhiteList.data.decode('UTF-8'))
        #debugPrint("Print Dictionary 1 id and encodedCredentials:")
        #debugPrint(fobWhiteListDict[djangoToPythonIndexConversion(1)]['encodedCredential'])
        #debugPrint(fobWhiteListDict[djangoToPythonIndexConversion(1)]['id'])


if __name__ == "__main__":
    print("STARTING Database.py MAIN FUNCTION AT " + getTime(INTERNET_TIME))

    # Create database object to use functions above
    api = Database(API_ENDPOINT)
    api.getCredentials()

    # In Python 3, leading zeros are not allowed on integer (e.g. 0002755603)
    # UID = 2755603 #hex(0002755603) #002AC13 #2755603 #4 #str(0x002A0C13)
    hexFobID = "0028130D"
    databaseID = api.getAutoGeneratedDatabaseID(hexFobID)
    debugPrint(databaseID)

    if(databaseID != CREDENTIALS_ID_NOT_FOUND):
        api.postDataLog(databaseID)
    else:
        print("HEX code UID not found in Whitelist")

    print("ENDING Database.py MAIN FUNCTION")


# 1. GET /api/credentials, which is the whitelist of hex values and their associated ID in our system.
# 2. When a fob is swiped, find that value in the whitelist you pulled down and get the ID mapped to it.
# 3. POST to /api/activitylistings with the ID you just got and the hard-coded "access point ID" (ranging from 1-8 currently) so we know which fob and which device was swiped.

# POSTing to api/credentials would only add a fob to the whitelist.  There is no access point ID in that endpoint anywhere.

# When you hit /api/credentials, you'll get a list back like the following

# {"id":"200","encodedCredential":"1f00001111"},{"id":"201","encodedCredential":"002915D6"}

# Store that in an array somewhere.  Then when you swipe the fob, it will transmit a value which I believe is either in hex or 
# needs to be converted to hex, not sure.  So say it transmits "1f00001111", you'll find in your array that it is id 200.  
# And if you're coding the Kraken, you know the access point ID is 2, so you can post the "200" and the "2" to the 
# /api/activitylistings endpoint so we get the fob and the device.
