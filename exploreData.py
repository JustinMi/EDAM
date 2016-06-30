import json
import urllib2
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

"""
Scientific name consists of Genus and Specific Epithtet
"""

"""
Returns a np array of counts of the query at the specified latitude and longitude year by year from beginning to end.
"""

def getCounts(query, latitude, longitude, beginning, end):
	query = query.replace(" ", "_")
	query = query.lower()
	years = np.arange(beginning, end + 1, 1)
	counts = []
	for i in range(end - beginning + 1):
		url = 'http://api.gbif.org/v1/occurrence/search?scientificName='+ str(query)\
		+'&year=' + str(beginning + i)\
		+'&decimalLatitude=' + str(latitude - 1.5) + "," + str(latitude + 1.5)\
		+'&decimalLongitude=' + str(longitude - 1.5) + "," + str(longitude + 1.5)\
		+'&limit=5&offset=0'
		response = urllib2.urlopen(url)
		data = json.load(response)
		if not ("count" in data):
			return None
		counts.append(data["count"])
	counts = np.asarray(counts)
	return counts


"""
Shows a time series (year by year) of a species given latitude (in decimal), longtiude (in decimal), beginning year, and end year
"""
def findQuery(query, latitude, longitude, beginning, end):
	years = np.arange(beginning, end + 1, 1) 
	counts = getCounts(query, latitude, longitude, beginning, end)
	if counts == None:
		return None
	plt.plot(years, counts)
	plt.axis([beginning, end, 0, np.amax(counts) + 5])
	print years
	print counts
	plt.show()

"""
Shows a time series (year by year) of a species given country (2 letter code), beginning year, and end year 
"""

def findQueryCountry(query, country, beginning, end): 
	query = query.replace(" ", "_")
	query = query.lower()
	years = np.arange(beginning, end + 1, 1)
	counts = []
	for i in range(end - beginning + 1):
		url = 'http://api.gbif.org/v1/occurrence/search?scientificName='+ str(query)\
		+'&year=' + str(beginning + i)\
		+'&country=' + str(country)\
		+'&limit=5&offset=0'
		response = urllib2.urlopen(url)
		data = json.load(response)
		if not ("count" in data):
			return None
		counts.append(data["count"])
	counts = np.asarray(counts)
	plt.plot(years, counts)
	plt.axis([beginning, end, 0, np.amax(counts) + 5])
	print years
	print counts
	plt.show()

"""
Shows a time series of a species given beginning year and end year
"""
def findQueryBasic(query, beginning, end): 
	query = query.replace(" ", "_")
	query = query.lower()
	years = np.arange(beginning, end + 1, 1)
	counts = []
	for i in range(end - beginning + 1):
		url = 'http://api.gbif.org/v1/occurrence/search?scientificName='+ str(query)\
		+'&year=' + str(beginning + i)\
		+'&limit=5&offset=0'	
		response = urllib2.urlopen(url)
		data = json.load(response)
		if not ("count" in data):
			return None
		counts.append(data["count"])
	counts = np.asarray(counts)
	plt.plot(years, counts)
	plt.axis([beginning, end, 0, np.amax(counts) + 5])
	print years
	print counts
	plt.show()

"""
Returns total count of query from beginning year to end year given latitude and longitude.
"""

def findOneQuery(query, latitude, longitude, beginning, end):	
	query = query.replace(" ", "_")
	query = query.lower()
	url = 'http://api.gbif.org/v1/occurrence/search?scientificName='+ str(query)\
			+'&year=' + str(beginning) + "," + str(end)\
			+'&decimalLatitude=' + str(latitude - 3) + "," + str(latitude + 3)\
			+'&decimalLongitude=' + str(longitude - 3) + "," + str(longitude + 3)\
			+'&limit=5&offset=0'
	response = urllib2.urlopen(url)
	data = json.load(response)
	if not ("count" in data):
		return None
	else:
		return data["count"]


"""
Returns a list of the invasive species in the given location, read from a csv made by getInvasiveSpecies.combineCSV. The csv should be titled:
"invasivespecies" + location + ".csv" 
"""
def getInvasiveSpecies(location):
	df = pd.read_csv("invasivespecies" + location.replace(" ", "") + ".csv", delimiter = ',')
	d = df["Species"]
	d = d.tolist()
	s = set()
	for item in d:
		s.add(item.lower())
	return s

"""
Returns a list of the mammals in the given location, read from a csv made manually. The csv should be titled:
"mammals" + location + ".csv" 
"""
def getMammals(location):
	df = pd.read_csv("mammals" + location.replace(" ", "") + ".csv", delimiter = ",")
	d = df["Genus"] + " " + df["Specific Epithtet"]
	d = d.tolist()
	s = set()
	for item in d:
		s.add(item.lower())
	sCopy = s.copy()
	for item in s:
		if not all(c.isalpha() or c.isspace() for c in item):
			sCopy.remove(item)
	return sCopy

"""
Returns a list of the mammals in the given location, read from a csv made manually. The csv should be titled:
"reptiles" + location + ".csv" 
"""
def getReptiles(location):
	df = pd.read_csv("reptiles" + location.replace(" ", "") + ".csv", delimiter = ",")
	d = df["Genus"] + " " + df["Specific Epithtet"]
	d = d.tolist()
	s = set()
	for item in d:
		s.add(item.lower())
	sCopy = s.copy()
	for item in s:
		if not all(c.isalpha() or c.isspace() for c in item):
			sCopy.remove(item)
	return sCopy

"""
Returns a list of the mammals in the given location, read from a csv made manually. The csv should be titled:
"magnoliophyta" + location + ".csv" 
"""
def getFlowers(location):
	df = pd.read_csv("magnoliophyta" + location.replace(" ", "") + ".csv", delimiter = ",")
	d = df["Genus"] + " " + df["Specific Epithtet"]
	d = d.tolist()
	s = set()
	for item in d:
		s.add(item.lower())
	sCopy = s.copy()
	for item in s:
		if not all(c.isalpha() or c.isspace() for c in item):
			sCopy.remove(item)
	return sCopy



"""
EXPERIMENTING WITH CODE
"""


# """
# Cane toads in Australia
# """
# findQueryCountry("Rhinella marina", "AU", 1900, 2010)

"""
Common carps in Australia
"""
# findQueryCountry("Cyprinus carpio", "AU", 1900, 2014)

# """
# Goats in Galapagos 
# """
# findQuery("Capra aegagrus", -0.6519, -90.4056, 2000, 2010)

# """
# Atlantic Bluefin Tuna in World

# """
# findQueryBasic("Thunnus thynnus", 1900, 2010)

# """
# Electric ants in Galapagos and Hawaii
# """
# # findQuery("Wasmannia auropunctata", -0.6519, -90.4056, 2000, 2010)
# findQuery("Wasmannia auropunctata", 19.8968, -155.5828, 2000, 2010)


# """
# Small Asian Mongoose in Hawaii
# """
# findQuery("Herpestes javanicus", 19.8968, -155.5828, 1800, 2010)

	# url = 'http://api.gbif.org/v1/occurrence/search?scientificName='\
	# 	+ str(query) + '&year=' + str(beginning) + ','\
	# 	+ str(end) + '&limit=5&offset=0'
	# response = urllib2.urlopen(url)
	# data = json.load(response)
	# print data["count"]