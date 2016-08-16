
import csv
import sklearn
import math
from sklearn import cluster
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import DBSCAN
from sklearn.cluster import MiniBatchKMeans
from difflib import SequenceMatcher
import idigbio
import json
import urllib2
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

"""
Scientific name consists of Genus and Specific Epithet
Galapagos Islands: -0.6519, -90.4056
Moorea: -17.5388, -149.8295
"""

def convertCSVtoPickle(csvFile, pickleFile):
	df = pd.read_csv(csvFile)
	df.to_pickle(pickleFile)

def convertPickletoCSV(pickleFile, csvFile):
	df = pd.read_pickle(pickleFile)
	df.to_csv(csvFile, index_col = 0)

"""
Returns a np array of counts of the query (scientific name of a species) from gbif at the specified latitude and longitude year by year from beginning to end.
"""

def getCounts(query, latitude, longitude, beginning, end):
	query = query.replace(" ", "_")
	query = query.lower()
	years = np.arange(beginning, end + 1, 1)
	counts = []
	for i in range(end - beginning + 1):
		url = 'http://api.gbif.org/v1/occurrence/search?scientificName='+ str(query)\
		+'&year=' + str(beginning + i)\
		+'&decimalLatitude=' + str(latitude - 0.75) + "," + str(latitude + 0.75)\
		+'&decimalLongitude=' + str(longitude - 0.75) + "," + str(longitude + 0.75)\
		+'&limit=5&offset=0'
		response = urllib2.urlopen(url)
		data = json.load(response)
		if not ("count" in data):
			return None
		counts.append(data["count"])
	counts = np.asarray(counts)
	return counts

"""
Gets counts year by year from 1900 to 2015 from a queryCSV.
queryCSV is the csv name. 
The csv should contain a genus column and a specific epithet column or scientific name column. 
Counts saved as json object where saveJSON is the file name.
"""
def getData(queryCSV, saveJSON, latitude, longitude, location):
	species = getSpecies(queryCSV, location)
	counts = {}
	for specie in species:
		count = getCounts(specie, latitude, longitude, 1900, 2015)
		if count is not None:
			counts[specie] = count

	countsCopy = counts.copy()
	for key,value in counts.items():
		countsCopy[key] = value.tolist()
	with open(saveJSON, 'w') as outfile:
	    json.dump(countsCopy, outfile)
	return countsCopy
	
"""
Get total count of a place from -1000 to 2015. 
queryCSV is the csv name.
Counts saved as json object where saveJSON is the file name.
"""
def getTotalCount(queryCSV, saveJSON, latitude, longitude, location):
	species = getSpecies(queryCSV, location)
	counts = {}
	years = np.arange(1900, 2015 + 1, 1)
	for animal in species:
		count = ed.findOneQuery(animal, latitude, longitude, -1000, 2015)
		if count is not None:
			counts[animal] = count
		else:
			counts[animal] = 0
	with open(saveJSON, 'w') as outfile:
		json.dump(counts, outfile)
	return counts


"""
Makes a dataframe after counts year by year and total counts are made. Dataframe is saved as a pickle object where outputFile is the file name
"""
def makeDataframe(queryCSV, countsInputFile, totalCountsInputFile, outputFile, location):
	species = getSpecies(queryCSV, location)
	d = dict()
	for specie in species:
		d[specie] = None

	df = pd.DataFrame(d.items(), columns = ["Scientific Name", "Native"])

	counts = json.loads(open(inputFile).read())
	countsCopy = counts.copy()
	for key,value in countsCopy.items():
		counts[key] = np.asarray(value)



	totalCounts = json.loads(open(totalCountsInputFile).read())

	df["Total Counts"] = df["Scientific Name"].map(totalCounts)	
	df = df[np.isfinite(df['Total Counts'])]


	df["Counts"] = df["Scientific Name"].map(counts)

	df = df[df["Counts"] == df["Counts"]]


	df = df.reset_index()
	df = df.drop(["index"], axis = 1)

	df.to_pickle(outputFile)

	return df	


"""
Get total counts from other locations for current location. Dataframe made from makeDataframe needs to exist before calling the function. 
Dataframe is saved as pickle object or csv where outputFile is the filename
"""

def findOtherLocationCounts(inputFile, outputFile, otherlocations):
	df = pd.read_pickle(inputFile)
	for currentLocation in range(len(otherlocations)):
		print currentLocation
		locationCount = []	
		for i in df.index:
			count = findOneQuery(df["Scientific Name"].iloc[i], otherlocations[currentLocation][0], otherlocations[currentLocation][1], -1000, 2015)
			locationCount.append(count)
		df[otherlocations[currentLocation][2]] = locationCount
		df.to_pickle("mooreaHexapod" + str(currentLocation) + ".pkl")
	df.to_pickle(outputFile)
	return df	

"""
inputFile should only contain counts of locations and scientific name 
Random exploring of data to see if there are any features worth noting. 
Average Count is total / (number of locations + 1)
Weighted Average Count is just total / (number of locations where count isn't zero + 1)
Averages Difference is Weighted Average - Average
Location Presence is number of locations where count isn't zero
Median is median
Should be called after findOtherLocationCounts()
Dataframe is saved as pickle object where the file name is outputFile
"""

def getOtherAverages(inputFile, outputFile):

	df2 = pd.read_pickle(inputFile)
	df = df2.drop('Scientific Name', 1)

	# df = df.drop('Native', 1)
	# df = df.drop("Counts", 1)
	# df = df.drop("Length (cm)", 1)
	# df = df.drop("Wingspan (cm)", 1)
	# df = df.drop("Total Counts", 1)
	averages = []
	weightedAverage = []
	nonZeros = []
	averagesDifference = []
	medians = []
	totals = []
	weights = []
	for i in df.index:
		m = []
		total = 0
		nonZero = 0
		weight = 0
		for j in range(len(df.columns)):
			count =  int(df[df.columns[j]].iloc[i])
			if count != 0:
				nonZero += 1
			m.append(count)
			total += count
		averages.append(total / (len(df.columns) + 1))
		weightedAverage.append(total / (nonZero + 1))
		averagesDifference.append((total / (nonZero + 1))  - total/ (len(df.columns) + 1))
		totals.append(total)
		median = np.median(np.array(m))
		medians.append(median)
		nonZeros.append(nonZero)
	df2["Total"] = np.asarray(totals)
	df2["Average Count"] = np.asarray(averages)
	df2["Weighted Average Count"] = np.asarray(weightedAverage)
	df2["Location Presence"] = np.asarray(nonZeros)
	df2["Averages Difference"] = np.asarray(averagesDifference)
	df2["Median"] = np.asarray(medians)
	df2.to_pickle(outputFile)
	return df2

"""
Get max, min, average value, and max slope of counts for each species in the dataframe.
Thought maybe that a big change in slope may correspond to something, but doesn't seem that way.
Dataframe is saved as pickle object where the file name is outputFile
Should be used after getOtherAverages()
"""


def getValues(inputFile, outputFile):
	df = pd.read_pickle(inputFile)
	maxes = []
	mins = []
	maxSlopes = []
	averageValues = []
	for i in df.index:
		counts = df["Counts"].iloc[i]
		currentMin = float("inf")
		maxSlope = 0
		nonZeros = 0
		for j in range(len(counts)):
			if counts[j] != 0:
				nonZeros += 1
				if currentMin > counts[j]:
					currentMin = counts[j]
			if j != len(counts) - 1:
				slope = counts[j + 1] - counts[j]
				if slope > maxSlope:
					maxSlope = slope
		if nonZeros != 0:
			averageValues.append(df["Total Counts"].iloc[i] / nonZeros)
		else:
			averageValues.append(0)
		maxes.append(np.amax(counts))
		if math.isinf(currentMin):
			mins.append(0)
		else:
			mins.append(currentMin)
		maxSlopes.append(maxSlope)
	df["Min"] = np.asarray(mins)
	df["Max"] = np.asarray(maxes)
	df["Average Value"] = np.asarray(averageValues)
	df["Max Slope"] = np.asarray(maxSlopes)
	df2.to_pickle(outputFile)

	return df2

"""
Get total count in iDigBio api. Should be used after getValues().
Dataframe is saved as pickle object where the file name is outputFile

"""
def getidigbioCount(inputFile, outputFile):
	df = pd.read_pickle(inputFile)
	api = idigbio.json()
	counts = []
	for i in df.index:
		record_list = api.search_records(rq={"scientificname": df["Scientific Name"].iloc[i].replace("_", " ")})
		counts.append(record_list["itemCount"])
	df["iDigBio Count"] = np.asarray(counts)
	df.to_pickle(outputFile)
	return df


"""
Use clustering. Tried out a couple of them and found that normal k_means was the best. 
Features should be a list of feature names. 
"""

def findClusters(inputFile, features):
	df = pd.read_pickle(inputFile)
	df = df[features]
	x = np.array(df)	
	X = StandardScaler().fit_transform(x)
	k_means = cluster.KMeans(n_clusters = 8)
	k_means.fit(X)
	k_meansBatch = MiniBatchKMeans(n_clusters = 8, max_iter = 500)
	k_meansBatch.fit(X)
	db = DBSCAN(eps=0.3, min_samples=10).fit(X)
	core_samples_mask = np.zeros_like(db.labels_, dtype=bool)
	core_samples_mask[db.core_sample_indices_] = True

	return k_meansBatch.labels_


"""
Shows a time series (year by year) of a species given latitude (in decimal), longtiude (in decimal), beginning year, and end year
"""
def showTimeSeries(query, latitude, longitude, beginning, end):
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

def showTimeSeriesCountry(query, country, beginning, end): 
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
def showTimeSeriesBasic(query, beginning, end): 
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
Returns the total count of query from beginning year to end year given latitude and longitude.
"""

def findOneQuery(query, latitude, longitude, beginning, end):	
	query = query.replace(" ", "_")
	query = query.lower()
	url = 'http://api.gbif.org/v1/occurrence/search?scientificName='+ str(query)\
			+'&year=' + str(beginning) + "," + str(end)\
			+'&decimalLatitude=' + str(latitude - 0.75) + "," + str(latitude + 0.75)\
			+'&decimalLongitude=' + str(longitude - 0.75) + "," + str(longitude + 0.75)\
			+'&limit=5&offset=0'
	response = urllib2.urlopen(url)
	data = json.load(response)
	if not ("count" in data):
		return 0
	else:
		return data["count"]

"""
Returns the total count of a query from beginning year to end year given latitude and longitude.
"""

def findBasicQuery(query):	
	query = query.replace(" ", "_")
	query = query.lower()
	url = 'http://api.gbif.org/v1/occurrence/search?scientificName='+ str(query)\
			+'&limit=5&offset=0'
	response = urllib2.urlopen(url)
	data = json.load(response)
	if not ("count" in data):
		return 0
	else:
		return data["count"]




"""
Returns a list of the invasive species in the given location, read from a csv made by combineCSV. 
"""
def getInvasiveSpecies(inputFile, location):
	df = pd.read_csv(inputFile)
	d = df["Species"]
	d = d.tolist()
	s = set()
	for item in d:
		s.add(item.lower())
	return s

"""
Returns a set of the species in the queryCSV, which is the name of the csv. 
The csv should contain a genus column and a specific epithtet column. 
"""
def getSpecies(queryCSV, location):
	df = pd.read_csv(queryCSV)
	if "Scientific Name" in df.columns:
		d = df["Scientific Name"]
	else:
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
# showTimeSeriesCountry("Rhinella marina", "AU", 1900, 2010)

# """
# Common carps in Australia
# """
# showTimeSeriesCountry("Cyprinus carpio", "AU", 1900, 2014)

# """
# Goats in Galapagos 
# """
# showTimeSeries("Capra aegagrus", -0.6519, -90.4056, 2000, 2010)

# """
# Atlantic Bluefin Tuna in World

# """
# showTimeSeriesBasic("Thunnus thynnus", 1900, 2010)

# """
# Electric ants in Galapagos and Hawaii
# """
# # getCounts("Wasmannia auropunctata", -0.6519, -90.4056, 2000, 2010)
# getCounts("Wasmannia auropunctata", 19.8968, -155.5828, 2000, 2010)


# """
# Small Asian Mongoose in Hawaii
# """
# getCounts("Herpestes javanicus", 19.8968, -155.5828, 1800, 2010)

