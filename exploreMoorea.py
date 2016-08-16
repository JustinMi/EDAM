import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import cleanData as cd
import exploreData as ed
import gmplot


"""
Goes through the cleaned csv of the records on Biocode and maps the species to the elevations they have been recorded in.

"""

def getElevations(inputFile):
	df = pd.read_pickle(inputFile)
	minElevations = {}
	maxElevations = {}
	for i in df.index:
		species = df["Scientific Name"].iloc[i]
		if species not in minElevations.keys():
			minElevations[species] = []
			maxElevations[species] = []
		minElevation = df["Min Elevation"].iloc[i]
		maxElevation = df["Max Elevation"].iloc[i]
		if minElevation == minElevation:
			minElevations[species].append(minElevation)
		if maxElevation == maxElevation:
			maxElevations[species].append(maxElevation)
	df = pd.DataFrame(minElevations.items(), columns = ["Scientific Name", "Min Elevations"])
	df["Max Elevations"] = df["Scientific Name"].map(maxElevations)
	df["Max Elevation"] = df.apply(lambda row: max(row["Max Elevations"] or ['Empty']), axis = 1)
	df["Min Elevation"] = df.apply(lambda row: min(row["Min Elevations"] or ['Empty']), axis = 1)

	return df

"""
Goes through the cleaned csv of the records on Biocode and records the total number of times each specie appears.

"""

def getRecordCounts(inputFile):
	df = pd.read_pickle(inputFile)
	counts = {}
	for i in df.index:
		species = df["Scientific Name"].iloc[i]
		if species not in counts:
			counts[species] = 0
		counts[species] += 1
	df = pd.DataFrame(counts.items(), columns = ["Scientific Name", "Total Count"])
	return df

"""
Combines the dataframes made from the records csv and the dataframe of classifications. 
"""
def combineDataFrames(recordsFile, classificationFile):
	df1 = getElevations(recordsFile)
	df2 = getRecordCounts(recordsFile)
	df3 = df1.merge(df2, on = "Scientific Name")
	df4 = pd.read_csv(classificationFile)
	df4 = df4[["Scientific Name", "Native"]]
	df5 = df3.merge(df4, on = "Scientific Name")
	return df5

"""
Keep only the species that we know are native or not.
"""
def getClassifiedSpecies(recordsFile, classificationFile):
	df1 = combineDataFrames(recordsFile, classificationFile)
	classified = []
	for i in df1.index:
		if df1["Native"].iloc[i] == "1" or df1["Native"].iloc[i] == "0":
			classified.append(i)
	df2 = df1.iloc[classified]
	df2 = df2.reset_index()
	df2["Native"] = pd.to_numeric(df2["Native"])
	df2 = df2.drop(["index"], axis = 1)
	return df2

"""
Get the counts of the classified species from different locations.
"""

def getOtherLocationCounts(recordsFile, classificationFile, classifiedFile, totalCountsFile):
 	df = getClassifiedSpecies(recordsFile, classificationFile)
	df.to_pickle(classifiedFile)
	df2 = ed.findOtherLocationCounts(classifiedFile, totalCountsFile, location)
	df2.to_pickle(totalCountsFile)
	df2.to_csv(totalCountsFile, index_col = 0)
	return df2




"""
Maps the records csv on Google Maps according to classification.
If classified as native, color is green.
If classified as non-native, color is red.
If unknown classification, color is yellow.
Map is saved as html with name outputMap
"""

def showGoogleMap(recordFile, classificationFile, outputMap):
	# googlemaps.Client(serverkey)
	classificationdf = pd.read_csv(classificationFile)
	native = set()
	nonnative = set()
	for i in classificationdf.index:
		species = classificationdf["Scientific Name"].iloc[i]
		if classificationdf["Native"].iloc[i] == '0':
			nonnative.add(species)
		elif classificationdf["Native"].iloc[i] == '1':
			native.add(species)
	df = pd.read_csv(recordFile)
	gmap = gmplot.GoogleMapPlotter(-17.5388, -149.8295, 12)
	latitudes = []
	longitudes = []
	for i in df.index:
		latitude = df["Latitude"].iloc[i] 
		longitude = df["Longitude"].iloc[i]
		if latitude == latitude and longitude == longitude:
			species = df["Scientific Name"].iloc[i].lower()
			if species in native:
				gmap.circle(latitude, longitude, 20, color = "green")
			elif species in nonnative:
				gmap.circle(latitude, longitude, 20, color = "red")
			else:
				gmap.circle(latitude, longitude, 20, color = "yellow")

	gmap.draw(outputMap)

location = [\
			(-25.2744, 133.7751, "Northern Territory, Australia"),\
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


# ed.convertCSVtoPickle("mooreaHexapodTrainingTest.csv", "mooreaHexapodTrainingTest.pkl")
# df = pd.read_pickle("mooreaHexapodTrainingTest.pkl")
# prediction = ed.findClusters("mooreaHexapodTrainingTest.pkl", ["Percent", "Length (cm)", "Min Elevation", "Max Elevation", "World Total", "Total Count", "Elevation Difference", "Location Presence"])
# df["Prediction"] = np.asarray(prediction)
# native = np.where(df["Native"] == 1)[0]
# for i in range(len(native)):
# 	print prediction[native[i]]