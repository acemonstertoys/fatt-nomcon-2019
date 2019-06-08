#!/usr/bin/env python

__author__ =  "Blaze Sanders"
__email__ =   "blaze.d.a.sanders@gmail.com"
__company__ = "Ace Toy Company"
__status__ =  "Development"
__date__ =    "Late Updated: 2019-06-06"
__doc__ =     "Get and Post data from JSON web API and pass status to Driver.py"

# Pull and process JSON formatted data from a HTTP protocol URL database
# https://www.geeksforgeeks.org/get-post-requests-using-python/
# https://www.digitalocean.com/community/tutorials/how-to-use-web-apis-in-python-3
#import requests

# Read Comma Separated Value (CSV) files from external storage
# https://docs.python.org/3/library/csv.html
import csv

# Allow us to work with the JSON data format
import json

# urllib3 is a powerful, sanity-friendly HTTP client for Python
# https://urllib3.readthedocs.io/en/latest/
import urllib3

# Allow time travel and time measurement
import time
import datetime

TIME_ZONE = 'CT' # or "PT or "Zulu"

ACCESS_POINTS_URL = 'https://nomcon.foballthethings.org/api/accesspoints/'

API_ENDPOINT = 'https://nomcon.foballthethings.org/api/'

API_KEY = '2e77c0656e0549e4cefadfac979ccc622b98b07f'

class Database:


	headers = {'Content-Type': 'application/coreapi+json',
                   'Authorization': 'Bearer {0}'.format(API_KEY)}

	# Defining a params dictionary for parameters to be sent to the API
	JSON_PARAMS = {
		'id': 1,'created_date': "2019-04-20T16:44:35.560440Z",
                'modified_date': "2019-06-01T17:39:09.497574Z",
                'name': "Minty Box", 'location': "Exhibit Hall",
		'verb': "mints dispensed"}



	###
	# Check integer or hex whitelist
	#
	# Return TRUE if fobID is in list of valid IDs, FASLE otherwise
	###
	def isValid(fobID):
		validIDs = [1234, 9876, 5555, 0000]
		idFound = False
		for i in validIDs:
			if(fobID == validIDs[i]):
				idFound = True

		return  idFound

	def createLocalWhitelist():
		print("TODO CSV STUFF")

	def postJSONdata(time, userID, deviceName):
		print("TODO POST STUFF")

	def getJSONdata(time, userID, deviceName):
		r = requests.get('https://nomcon.foballthethings.org/api')
		r = requests.get('https://nomcon.foballthethings.org/api/accesspoints/')

		#TODO curl -X GET --header 'Accept: application/coreapi+json' --header 'Authorization: 2e77c0656e0549e4cefadfac979ccc622b98b07f' 'https://nomcon.foballthethings.org/api/'

		while True:
			try:
				r.json()
			except (ValueError, RuntimeError, TypeError, NameError):
				#Value Error thrown when no JSON object could be decoded
				print("BAD STUFF HAPPENED")

			fobID = r.ID

			if(isValid(fobID)):
				print("DO HDMI STUFF")
				#TODO HDMI  STUFF

if __name__ == "__main__":
	print("TESTING")

	timeStamp = time.time()
	iso8601DateTime = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
	print("Current Time is:" + time)
	http = urllib3.PoolManager()

	#project = http.request('GET', API_ENDPOINT)
	project = http.request('POST', ACCESS_POINTS_URL)
	print(project.data.decode('UTF-8'))






	time.sleep(10)
	# sending get request and saving the response as response object
	r = requests.get(url = URL, params = PARAMS)

	# extracting data in json format
	data = r.json()

	# extracting latitude, longitude and formatted address  
	# of the first matching location 
	latitude = data['results'][0]['geometry']['location']['lat'] 
	longitude = data['results'][0]['geometry']['location']['lng'] 
	formatted_address = data['results'][0]['formatted_address'] 

	# printing the output 
	print("Latitude:%s\nLongitude:%s\nFormatted Address:%s" %(latitude, longitude,formatted_address)) 


