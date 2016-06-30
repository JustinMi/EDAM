
import exploreData as ed
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import csv
import sklearn
import json
import math
from sklearn import cluster
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import DBSCAN
from sklearn.cluster import MiniBatchKMeans
from difflib import SequenceMatcher
import idigbio



"""
I need to edit the code so that I don't need to keep commenting out depending on the species for all the code in this file. Will do so later.
"""

"""
Gets flower counts year by year from 1900 to 2015.

"""

def getFlowerData():
	flowers = ed.getFlowers("Galapagos Islands")
	invasive = ed.getInvasiveSpecies("Galapagos Islands")
	invasiveflowers = set()
	noninvasiveflowers = set()
	for flower in flowers:
		if flower in invasive:
			invasiveflowers.add(flower)
		else:
			noninvasiveflowers.add(flower)
	counts = {}
	years = np.arange(1900, 2015 + 1, 1)
	invasiveflowersCopy = invasiveflowers.copy()
	for flower in invasiveflowers:
		count = ed.getCounts(flower, -0.6519, -90.4056, 1900, 2015)
		if count is not None:
			counts[flower] = count
			# plt.plot(years, count, label = mammal)
		else:
			invasiveflowersCopy.remove(flower)
	invasiveflowers = invasiveflowersCopy

	# years = np.arange(2000, 2002, 1)
	# plt.show()
	noninvasiveflowersCopy = noninvasiveflowers.copy()
	for flower in noninvasiveflowers:
		count = ed.getCounts(flower, -0.6519, -90.4056, 1900, 2015)
		if count is not None:
			counts[flower] = count
				# plt.plot(years, count, label = mammal)
		else: 
			noninvasiveflowersCopy.remove(flower)
	noninvasiveflowers = noninvasiveflowersCopy
	countsCopy = counts.copy()
	for key,value in counts.items():
		countsCopy[key] = value.tolist()
	with open('magnoliophytadata.txt', 'w') as outfile:
	    json.dump(countsCopy, outfile)
	return countsCopy
	

"Gets reptile counts year by year from 1900 to 2015."


def getReptilesData():
	reptiles = ed.getReptiles("Galapagos Islands")
	invasive = ed.getInvasiveSpecies("Galapagos Islands")
	invasiveReptiles = set()
	noninvasiveReptiles = set()
	for reptile in reptiles:
		if reptile in invasive:
			invasiveReptiles.add(reptile)
		else:
			noninvasiveReptiles.add(reptile)
	counts = {}
	years = np.arange(1900, 2015 + 1, 1)
	invasiveReptilesCopy = invasiveReptiles.copy()
	for reptile in invasiveReptiles:
		count = ed.getCounts(reptile, -0.6519, -90.4056, 1900, 2015)
		if count is not None:
			counts[reptile] = count
			# plt.plot(years, count, label = mammal)
		else:
			invasiveReptilesCopy.remove(reptile)
	invasiveReptiles = invasiveReptilesCopy

	# years = np.arange(2000, 2002, 1)
	# plt.show()
	noninvasiveReptilesCopy = noninvasiveReptiles.copy()
	for reptile in noninvasiveReptiles:
		count = ed.getCounts(reptile, -0.6519, -90.4056, 1900, 2015)
		if count is not None:
			counts[reptile] = count
				# plt.plot(years, count, label = mammal)
		else: 
			noninvasiveReptilesCopy.remove(reptile)
	noninvasiveReptiles = noninvasiveReptilesCopy
	countsCopy = counts.copy()
	for key,value in counts.items():
		countsCopy[key] = value.tolist()
	with open('reptiledata.txt', 'w') as outfile:
	    json.dump(countsCopy, outfile)
	return countsCopy

"""
Gets mammals counts year by year from 1900 to 2015.
"""

def getMammalsData():
	mammals = ed.getMammals("Galapagos Islands")
	invasive = ed.getInvasiveSpecies("Galapagos Islands")
	invasiveMammals = set()
	noninvasiveMammals = set()
	for mammal in mammals:
		if mammal in invasive:
			invasiveMammals.add(mammal)
		else:
			noninvasiveMammals.add(mammal)
	counts = {}
	years = np.arange(1900, 2015 + 1, 1)
	invasiveMammalsCopy = invasiveMammals.copy()
	for mammal in invasiveMammals:
		count = ed.getCounts(mammal, -0.6519, -90.4056, 1900, 2015)
		if count is not None:
			counts[mammal] = count
			# plt.plot(years, count, label = mammal)
		else:
			invasiveMammalsCopy.remove(mammal)
	invasiveMammals = invasiveMammalsCopy

	# years = np.arange(2000, 2002, 1)
	# plt.show()
	noninvasiveMammalsCopy = noninvasiveMammals.copy()
	for mammal in noninvasiveMammals:
		count = ed.getCounts(mammal, -0.6519, -90.4056, 1900, 2015)
		if count is not None:
			counts[mammal] = count
				# plt.plot(years, count, label = mammal)
		else: 
			noninvasiveMammalsCopy.remove(mammal)
	noninvasiveMammals = noninvasiveMammalsCopy
	countsCopy = counts.copy()
	for key,value in counts.items():
		countsCopy[key] = value.tolist()
	with open('galapagosmammalscounts.txt', 'w') as outfile:
	    json.dump(countsCopy, outfile)
	return countsCopy

"""
Get total count from -1000 to 2015. 
"""
def getTotalCount():
	mammals = ed.getMammals("Galapagos Islands")
	# reptiles = ed.getReptiles("Galapagos Islands")
	invasive = ed.getInvasiveSpecies("Galapagos Islands")
	invasiveAnimals = set()
	noninvasiveAnimals = set()
	for mammal in mammals:
		if mammal in invasive:
			invasiveAnimals.add(mammal)
		else:
			noninvasiveAnimals.add(mammal)
	# for reptile in reptiles:
	# 	if reptile in invasive:
	# 		invasiveAnimals.add(reptile)
	# 	else:
	# 		noninvasiveAnimals.add(reptile)
	counts = {}
	invasiveAnimalsCopy = invasiveAnimals.copy()
	for animal in invasiveAnimals:
		count = ed.findOneQuery(animal, -0.6519, -90.4056, -1000, 2015)
		if count is not None:
			counts[animal] = count
		else:
			invasiveAnimalsCopy.remove(animal)
	invasiveAnimals = invasiveAnimalsCopy

	# # years = np.arange(2000, 2002, 1)
	noninvasiveAnimalsCopy = noninvasiveAnimals.copy()
	for animal in noninvasiveAnimals:
		count = ed.findOneQuery(animal, -0.6519, -90.4056, -1000, 2015)
		if count is not None:
			counts[animal] = count
				# plt.plot(years, count, label = mammal)
		else: 
			noninvasiveAnimalsCopy.remove(animal)
	noninvasiveAnimals = noninvasiveAnimalsCopy
	countsCopy = counts.copy()
	# with open('totalcounts.txt', 'w') as outfile:
	#     json.dump(countsCopy, outfile)


	# mammals = ed.getMammals("Galapagos Islands")
	# reptiles = ed.getReptiles("Galapagos Islands")
	# flowers = ed.getFlowers("Galapagos Islands")
	# invasive = ed.getInvasiveSpecies("Galapagos Islands")
	# invasiveFlowers = set()
	# noninvasiveFlowers = set()
	# for flower in flowers:
	# 	if flower in invasive:
	# 		invasiveFlowers.add(flower)
	# 	else:
	# 		noninvasiveFlowers.add(flower)
	# counts = {}
	# invasiveFlowersCopy = invasiveFlowers.copy()
	# for flower in invasiveFlowers:
	# 	count = ed.findOneQuery(flower, -0.6519, -90.4056, -1000, 2015)
	# 	if count is not None:
	# 		counts[flower] = count
	# 	else:
	# 		invasiveFlowersCopy.remove(flower)
	# invasiveFlowers = invasiveFlowersCopy

	# years = np.arange(2000, 2002, 1)
	# noninvasiveFlowersCopy = noninvasiveFlowers.copy()
	# for flower in noninvasiveFlowers:
	# 	count = ed.findOneQuery(flower, -0.6519, -90.4056, -1000, 2015)
	# 	if count is not None:
	# 		counts[flower] = count
	# 			# plt.plot(years, count, label = mammal)
	# 	else: 
	# 		noninvasiveFlowersCopy.remove(flower)
	# noninvasiveFlowers = noninvasiveFlowersCopy
	# countsCopy = counts.copy()
	# with open('magnoliophytatotalcounts.txt', 'w') as outfile:
	#     json.dump(countsCopy, outfile)

	with open("mammalstotalcounts.txt", 'w') as outfile:
		json.dump(countsCopy, outfile)





"""
Makes a dataframe after counts year by year from 1900 to 2015 and total counts in all history are made.
"""
def makeDataframe():
	# flowers = ed.getFlowers("Galapagos Islands")
	mammals = ed.getMammals("Galapagos Islands")
	# reptiles = ed.getReptiles("Galapagos Islands")
	invasive = ed.getInvasiveSpecies("Galapagos Islands")
	d = dict()
	for mammal in mammals:
		if mammal in invasive:
			d[mammal] = 1
		else:
			d[mammal] = 0
	# for reptile in reptiles:
	# 	if reptile in invasive:
	# 		d[reptile] = 1
	# 	else:
	# 		d[reptile] = 0
	# for flower in flowers:
	# 	if flower in invasive:
	# 		d[flower] = 1
	# 	else:
	# 		d[flower] = 0
	df = pd.DataFrame(d.items(), columns = ["Scientific Name", "Invasive"])

	counts = json.loads(open("galapagosmammalscounts.txt").read())
	# counts2 = json.loads(open("reptileData.txt").read())
	countsCopy = counts.copy()
	for key,value in countsCopy.items():
		counts[key] = np.asarray(value)
	# for key,value in counts2.items():
	# 	counts[key] = np.asarray(value)


	totalCounts = json.loads(open("mammalstotalcounts.txt").read())
	# totalCounts = json.loads(open("magnoliophytatotalcounts.txt").read())

	df["Total Counts"] = df["Scientific Name"].map(totalCounts)	
	df = df[np.isfinite(df['Total Counts'])]


	df["Counts"] = df["Scientific Name"].map(counts)

	# totalCounts = json.loads(open("totalcounts.txt").read())

	df = df[df["Counts"] == df["Counts"]]


	df = df.reset_index()
	df = df.drop(["index"], axis = 1)

	# df.to_pickle("galapagosSpecies.pkl")
	# df.to_pickle("galapagosFlowers.pkl")
	df.to_pickle("galapagosMammals.pkl")

	return df	

"""
Get total counts from other locations
"""
def findOtherLocationCounts():
	df = pd.read_pickle("galapagosMammals.pkl")
	# df = pd.read_pickle("galapagosFlowers11")

	for currentLocation in range(len(location)):
		# print location[currentLocation][2]
		locationCount = []	
		for i in df.index:
			# print i 
			count = ed.findOneQuery(df["Scientific Name"].iloc[i], location[currentLocation][0], location[currentLocation][1], -1000, 2015)
			locationCount.append(count)
		df[location[currentLocation][2]] = locationCount
		# df.to_pickle("galapagosFlowers" + str(currentLocation + 12) + ".pkl")


	# df.to_pickle("galapagosSpecies.pkl")
	df.to_pickle("galapagosMammalsClean.pkl")
	return df	


"""
Random exploring of data to see if there are any features worth noting. 
Weighted Average Count is just total / number of locations where count isn't zero.

"""

def getOtherAverages():
	# df2 = pd.read_pickle("galapagosFlowersClean.pkl")

	# df2 = pd.read_pickle("galapagosSpecies.pkl")
	df2 = pd.read_pickle("galapagosMammalsClean.pkl")
	df = df2.drop('Scientific Name', 1)

	nameLen = []
	nameSimilarity = []
	for i in df2.index:
		similarities = []
		similarity = SequenceMatcher(None, "galapagos", df2["Scientific Name"].iloc[i].replace(" ", "")).ratio()
		# for j in df2.index:
			# if i != j:
				# similarity = SequenceMatcher(None, df2["Scientific Name"].iloc[j].replace(" ", ""), df2["Scientific Name"].iloc[i].replace(" ", "")).ratio()
				# similarities.append(similarity)
		nameLen.append(len(df2["Scientific Name"].iloc[i]) - 1)
		# nameSimilarity.append(np.mean(similarities))
		nameSimilarity.append(similarity)
	df2["Name Length"] = np.asarray(nameLen)
	df2["Average Similarity"] = np.asarray(nameSimilarity)

	df = df.drop('Invasive', 1)
	df = df.drop("Counts", 1)
	df = df.drop("Total Counts", 1)
	# df = df.drop("Max", 1)
	# df = df.drop("Min", 1)
	# df = df.drop("Average Value", 1)
	# df = df.drop("Max Slope", 1)
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
		averages.append(total / len(df.columns))
		weightedAverage.append(total / (nonZero + 1))
		averagesDifference.append((total / (nonZero + 1))  - total/ len(df.columns))
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
	# df2.to_pickle("galapagosFlowersClean2.pkl")
	df2.to_pickle("galapagosMammalsClean2.pkl")
	return df2
	
"""
Get max, min, average value, and max slope of counts for each species in the dataframe.
Thought maybe that a big change in slope may correspond to something, but doesn't seem that way.
"""


def getValues():
	df = pd.read_pickle("galapagosMammalsClean2.pkl")
	# df = pd.read_pickle("galapagosFlowers.pkl")
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
	return df

def removeZeroEntries():
	df = getValues()
	nonZeros = []
	for i in df.index:
		if np.any(df[["Counts"]].iloc[i, 0] != 0):
			nonZeros.append(i)
	df = df.iloc[nonZeros]
	df = df.reset_index()
	df = df.drop(["index"], axis = 1)
	return df


"""
Use clustering. Tried out a couple of them and found that normal k_means was the best.
"""

def findClusters():
	df = getValues()

	df = df[["Averages Difference","Location Presence", "Median", "Average Count", "Total Counts", "Average Value", "iDigBio Count"]]
	# df = df.drop('Scientific Name', 1)
	# df = df.drop('Invasive', 1)
	# df = df.drop("Counts", 1)
	# df = df.drop("Max", 1)
	# df = df.drop("Min", 1)
	# df = df.drop("Average Value", 1)
	# df = df.drop("Max Slope", 1)
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
Get total count in iDigBio api.
"""
def getidigbioCount():
	df = pd.read_pickle("galapagosMammalsClean2.pkl")
	api = idigbio.json()
	counts = []
	for i in df.index:
		record_list = api.search_records(rq={"scientificname": df["Scientific Name"].iloc[i].replace("_", " ")})
		counts.append(record_list["itemCount"])
	df["iDigBio Count"] = np.asarray(counts)
	df.to_pickle("galapagosMammalsClean2.pkl")
	return df


"""
Different locations to get total counts from.
"""

location = [(-25.2744, 133.7751, "Northern Territory, Australia"),\
			(34.9592, -116.4194, "California, United States"),\
			(35.6895, 139.6917, "Tokyo, Japan"),\
			(-30.5595, 22.9375, "Northern Cape, South Africa"),\
			(42.3601, -71.0589, "Massachusetts, United States"),\
			(25.7617, -80.1918, "Florida, United States"),\
			(-0.1807, -78.4678, "Pichincha, Ecuador"),\
			(-3.4653, -62.2159, "Amazonas, Brazil"),\
			(3.1390, 101.6869, "Kuala Lumpur, Malaysia"),\
			(23.4162, 25.6628, "New Valley Governate, Egypt"),\
			(9.9281, -84.0907, "San Jose Province, Costa Rica"),\
			(51.5074, -0.1278, "London, England"),\
			(48.8566, 2.3522, "Ile-de-France, France"),\
			(59.3293, 18.0686, "Sodermanland, Sweden"),\
			(21.3069, -157.8583, "Hawaii, United States"),\
			(28.6139, 77.2090, "Delhi, India"),\
			(43.6532, -79.3832, "Ontario, Canada"),\
			(52.5200, 13.4050, "Berlin, Germany"),\
			(41.8780, -93.0977, "Iowa, United States"),\
			(-4.3871, 15.9700, "Kinshasa, DR Congo"),\
			(-6.1745, 106.8227, "Jakarta, Indonesia"),\
			(-4.0435, 39.6682, "Mombasa County, Kenya")]

"""
Run clustering.
"""

df = getValues()
prediction = findClusters()
invasive = np.where(df["Invasive"] == 1)[0]
for i in range(len(invasive)):
	print prediction[invasive[i]]


# print "Flowers"
# df2 = pd.read_pickle("galapagosFlowersClean2.pkl")
# invasive2 = np.where(df2["Invasive"] == 1)[0]
# df2 = df2[["Averages Difference","Location Presence", "Median", "Average Count", "Total Counts", "Weighted Average Count"]]
# x = np.array(df2)
# X = StandardScaler().fit_transform(x)
# k_means = MiniBatchKMeans()
# k_means.fit(X)
# prediction2 = k_means.labels_
# for i in range(len(invasive2)):
	# print prediction2[invasive2[i]]
