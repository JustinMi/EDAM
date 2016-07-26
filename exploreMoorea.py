import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import cleanData as cd
import exploreData as eds
# import googlemaps
# import ConfigParser 
import gmplot

# """
# If planning to use Google Maps API, make an .ini file titled "GoogleAPI.ini" with a section named "Key" and in the section have the line "Server: " + serverkey

# """
# config = ConfigParser.ConfigParser()
# config.read("GoogleAPI.ini")
# serverkey = config.get("Key", "Server")

"""
Goes through the csv of the records on Biocode csv and maps the species to the elevations they have been recorded in.
CSV should be titled 'Biocode' + phylum + 'RecordsClean' (This is done by the cleanMooreaRecords function in cleanData.py)

"""

def getElevations(phylum):
	df = pd.read_csv("Biocode" + phylum + "RecordsClean.csv", delimiter = ",", index_col = None, header = 0)
	minElevations = {}
	maxElevations = {}
	for i in df.index:
		species = df["ScientificName"].iloc[i]
		if species not in minElevations.keys():
			minElevations[species] = []
			maxElevations[species] = []
		minElevation = df["MinElevationMeters[ce]"].iloc[i]
		maxElevation = df["MaxElevationMeters[ce]"].iloc[i]
		if minElevation == minElevation:
			minElevations[species].append(minElevation)
		if maxElevation == maxElevation:
			maxElevations[species].append(maxElevation)
	df = pd.DataFrame(minElevations.items(), columns = ["ScientificName", "Min Elevations"])
	df["Max Elevations"] = df["ScientificName"].map(maxElevations)
	return df

"""
Goes through the csv of the records on Biocode csv and records the total number of times each specie appears.
CSV should be titled 'Biocode' + phylum + 'RecordsClean' (This is done by the cleanMooreaRecords function in cleanData.py)

"""

def getRecordCounts(phylum):
	df = pd.read_csv("Biocode" + phylum + "RecordsClean.csv", delimiter = ",", index_col = None, header = 0)
	counts = {}
	for i in df.index:
		species = df["ScientificName"].iloc[i]
		if species not in counts:
			counts[species] = 0
		counts[species] += 1
	df = pd.DataFrame(counts.items(), columns = ["ScientificName", "Counts"])
	return df

"""
Combines all the dataframes. 
"""
def combineDataFrames(phylum):
	df1 = getElevations(phylum)
	df2 = getRecordCounts(phylum)
	df = pd.concat([df1, df2])
	return df


"""
Maps the records csv on Google Maps according to classification.
If classified as native, color is green.
If classified as non-native, color is red.
If unknown classification, color is yellow.
Classification csv should be titled "Moorea" + phylum (first letter capitalized) + "Classification" 
CSV should be titled 'Biocode' + phylum (first letter capitalized) + 'RecordsClean' (This is done by the cleanMooreaRecords function in cleanData.py)
Map is saved as phylum + "map.html" 
"""

def showGoogleMap(phylum):
	# googlemaps.Client(serverkey)
	classificationdf = pd.read_csv("Moorea" + phylum + "Classification.csv")
	native = set()
	nonnative = set()
	for i in classificationdf.index:
		species = classificationdf["Scientific Name"].iloc[i]
		if classificationdf["Native"].iloc[i] == '0':
			nonnative.add(species)
		elif classificationdf["Native"].iloc[i] == '1':
			native.add(species)
	df = pd.read_csv("Biocode" + phylum + "RecordsClean.csv", delimiter = ",", index_col = None, header = 0)
	gmap = gmplot.GoogleMapPlotter(-17.5388, -149.8295, 12)
	latitudes = []
	longitudes = []
	for i in df.index:
		latitude = df["DecimalLatitude[ce]"].iloc[i] 
		longitude = df["DecimalLongitude[ce]"].iloc[i]
		if latitude == latitude and longitude == longitude:
			species = df["ScientificName"].iloc[i].lower()
			if species in native:
				gmap.circle(latitude, longitude, 20, color = "green")
			elif species in nonnative:
				gmap.circle(latitude, longitude, 20, color = "red")
			else:
				gmap.circle(latitude, longitude, 20, color = "yellow")


	# gmap = gmplot.GoogleMapPlotter(-17.5388, -149.8295, 12)

	# gmap.scatter(latitudes, longitudes, color = "#00FFFF", size = 100)

	gmap.draw(phylum + "map.html")

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



# df = findOtherLocationCounts("Hexapod")
# df = pd.read_pickle("mooreaHexapodCounts")

