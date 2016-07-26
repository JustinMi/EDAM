import json
import urllib2
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

"""
Scientific name consists of Genus and Specific Epithtet
Galapagos Islands: -0.6519, -90.4056
Moorea: -17.5388, -149.8295
"""

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
Gets query (phylum, family, etc) counts year by year from 1900 to 2015. 
The csv should contain a genus column and a specific epithtet column. 

"""
def getData(query, latitude, longitude, location):
	species = getSpecies(query, location)
	counts = {}
	for specie in species:
		count = getCounts(specie, latitude, longitude, 1900, 2015)
		if count is not None:
			counts[specie] = count

	countsCopy = counts.copy()
	for key,value in counts.items():
		countsCopy[key] = value.tolist()
	with open(location.replace(" ", "") + query + 'data.txt', 'w') as outfile:
	    json.dump(countsCopy, outfile)
	return countsCopy
	
"""
Get total count from -1000 to 2015. 
"""
def getTotalCount(query, latitude, longitude, location):
	species = ed.getSpecies(query, location)
	counts = {}
	years = np.arange(1900, 2015 + 1, 1)
	for animal in species:
		count = ed.findOneQuery(animal, latitude, longitude, -1000, 2015)
		if count is not None:
			counts[animal] = count
		else:
			counts[animal] = 0
	with open(location + query + "TotalCounts.txt", 'w') as outfile:
		json.dump(counts, outfile)
	return counts


"""
Makes a dataframe after counts year by year and total counts are made. Dataframe is saved as a pickle object titled 
location + query + ".pkl"
"""
def makeDataframe(query, location):
	species = getSpecies(query, location)
	d = dict()
	for specie in species:
		d[specie] = None

	df = pd.DataFrame(d.items(), columns = ["Scientific Name", "Native"])

	counts = json.loads(open(location + query + "data.txt").read())
	# counts2 = json.loads(open("reptileData.txt").read())
	countsCopy = counts.copy()
	for key,value in countsCopy.items():
		counts[key] = np.asarray(value)
	# for key,value in counts2.items():
	# 	counts[key] = np.asarray(value)


	totalCounts = json.loads(open(location + query + "TotalCounts.txt").read())
	# totalCounts = json.loads(open("magnoliophytatotalcounts.txt").read())

	df["Total Counts"] = df["Scientific Name"].map(totalCounts)	
	df = df[np.isfinite(df['Total Counts'])]


	df["Counts"] = df["Scientific Name"].map(counts)

	df = df[df["Counts"] == df["Counts"]]


	df = df.reset_index()
	df = df.drop(["index"], axis = 1)

	df.to_pickle(location.replace(" ", "") + query + ".pkl")

	return df	


"""
Get total counts from other locations for current location. Dataframe made from makeDataframe needs to exist before calling the function. 
Dataframe is saved as pickle object titled location + query + "Clean.pkl"
"""

def findOtherLocationCounts(query, location, otherlocations):
	df = pd.read_pickle(location.replace(" ", "") + query + ".pkl")
	for currentLocation in range(len(otherlocations)):
		# print location[currentLocation][2]
		locationCount = []	
		for i in df.index:
			# print i 
			count = ed.findOneQuery(df["Scientific Name"].iloc[i], location[currentLocation][0], location[currentLocation][1], -1000, 2015)
			locationCount.append(count)
		df[location[currentLocation][2]] = locationCount
	df.to_pickle(location.replace(" ", "") + query + "Clean.pkl")
	return df	

"""
Random exploring of data to see if there are any features worth noting. 
Name Length is name length (No idea where I was going with this)
Name Similarity is seeing how similar the name of a species is to the location (Totally useless)
Average Count is total / (number of locations + 1)
Weighted Average Count is just total / (number of locations where count isn't zero + 1)
Averages Difference is Weighted Average - Average
Location Presence is number of locations where count isn't zero
Median is median
Should be called before getValues()
Dataframe is saved as pickle object titled location + query + "Clean2.pkl"

"""

def getOtherAverages(query, location):

	df2 = pd.read_pickle(location.replace(" ", "") + query + "Clean.pkl")
	df = df2.drop('Scientific Name', 1)

	nameLen = []
	nameSimilarity = []
	for i in df2.index:
		similarities = []
		similarity = SequenceMatcher(None, location, df2["Scientific Name"].iloc[i].replace(" ", "")).ratio()
		nameLen.append(len(df2["Scientific Name"].iloc[i]) - 1)
		nameSimilarity.append(similarity)
	df2["Name Length"] = np.asarray(nameLen)
	df2["Average Similarity"] = np.asarray(nameSimilarity)

	df = df.drop('Invasive', 1)
	df = df.drop("Counts", 1)
	df = df.drop("Total Counts", 1)
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
			count =  df[df.columns[j]].iloc[i]
			if count != 0:
				nonZero += 1
			m.append(count)
			total += count
		averages.append(total / (len(df.columns) + 1))
		weightedAverage.append(total / (nonZero + 1))
		averagesDifference.append((total / (nonZero + 1))  - total/ len(df.columns + 1))
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
	df2.to_pickle(location.replace(" ", "") + query + "Clean2.pkl")
	return df2

"""
Get max, min, average value, and max slope of counts for each species in the dataframe.
Thought maybe that a big change in slope may correspond to something, but doesn't seem that way.
Dataframe is saved as pickle object titled location + query + "Clean3.pkl"
Should be used after getOtherAverages()
"""


def getValues(query, location):
	df = pd.read_pickle(location.replace(" ", "") + query + "Clean2.pkl")
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
	df2.to_pickle(location.replace(" ", "") + query + "Clean3.pkl")

	return df2

"""
Get total count in iDigBio api. Should be used after getValues()
"""
def getidigbioCount(query, location):
	df = pd.read_pickle(location.replace(" ", "") + query + "Clean3.pkl")
	api = idigbio.json()
	counts = []
	for i in df.index:
		record_list = api.search_records(rq={"scientificname": df["Scientific Name"].iloc[i].replace("_", " ")})
		counts.append(record_list["itemCount"])
	df["iDigBio Count"] = np.asarray(counts)
	df.to_pickle(location.replace(" ", "") + query + "Clean4.pkl")
	return df


"""
Use clustering. Tried out a couple of them and found that normal k_means was the best. Should be used after calling getidigioCount()
"""

def findClusters(query, location):
	df = pd.read_pickle(location.replace(" ", "") + query + "Clean4.pkl")
	df = df[["Averages Difference","Location Presence", "Median", "Average Count", "Total Counts", "Average Value", "iDigBio Count"]]
	x = np.array(df)	
	X = StandardScaler().fit_transform(x)
	k_means = cluster.KMeans(n_clusters = 7)
	k_means.fit(X)
	k_meansBatch = MiniBatchKMeans(n_clusters = 8, max_iter = 500)
	k_meansBatch.fit(X)
	db = DBSCAN(eps=0.3, min_samples=10).fit(X)
	core_samples_mask = np.zeros_like(db.labels_, dtype=bool)
	core_samples_mask[db.core_sample_indices_] = True

	return k_means.labels_


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
Returns a list of the species with the given query (phylum, family, etc.) in the given location, read from a csv made manually. The csv should be titled:
query + location + ".csv". 
The csv should contain a genus column and a specific epithtet column. 
"""
def getSpecies(query, location):
	df = pd.read_csv(query + location.replace(" ", "") + ".csv", delimiter = ",")
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

