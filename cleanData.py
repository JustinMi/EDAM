import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

"""
Cleans species record data given by Moorea Biocode Project. Should be converted to csv and csv should be titled "Biocode" + phylum/subphylum + "Records".
Cleaned csv is titled "Biocode" + phylum/subphylum + "RecordsClean.csv"

"""
def cleanMooreaRecords(phylum):
	df = pd.read_csv("Biocode" + phylum + "Records.csv", delimiter = ",", index_col = None, header = 0)
	speciesSet = set()
	df = df[["seq_num[ce]", "MinElevationMeters[ce]", "MaxElevationMeters[ce]", "ScientificName", "Genus", "SpecificEpithet", "DecimalLatitude[ce]", "DecimalLongitude[ce]"]]
	df["Scientific Name"] = df["ScientificName"].astype(str)
	clean = []
	for i in df.index:
		if df["Scientific Name"].iloc[i] != "NaN" and " " in df["Scientific Name"].iloc[i] and "sp." not in df["Scientific Name"].iloc[i]:
			clean.append(i)
	df = df.iloc[clean]
	df["Scientific Name"] = df["ScientificName"].str.lower()
	df = df.reset_index()
	df = df.drop(["index", "ScientificName"], axis = 1)
	df.to_csv("Biocode" + phylum + "RecordsClean.csv")
	return df

"""
Cleans species data given by Moorea Biocode Project. Should be converted to csv and csv should be titled "Biocode" + phylum/subphylum.
Cleaned csv is titled "Moorea" + phylum + ".csv"
"""
def cleanMooreaSpecies(phylum):
	df = pd.read_csv("Biocode" + phylum + ".csv", delimiter = ",", index_col = None, header = 0)
	speciesSet = set()
	for i in df.index:
		genus = str(df["genus"].iloc[i])
		species = str(df["species"].iloc[i])
		if genus != "" and genus != "Undetermined" and species != "nan" and species != "sp.":
			scientificName = genus + " " + species
			scientificName = scientificName.lower()
			speciesSet.add(scientificName)

	df = pd.DataFrame(list(speciesSet))
	df.columns = ["Scientific Name"]
	df.to_csv("Moorea" + phylum[0].upper() + phylum[1:].lower() + ".csv")
	return df

"""
Not all the species are actually in the species data given by the Moorea Biocode Project. The function utilizes the records data and combines it with the 
classification data to get all species.
"""
def getAllSpecies(phylum):
	records = pd.read_csv("Biocode" + phylum + "RecordsClean.csv", delimiter = ",", index_col = None, header = 0)
	classificationdf = pd.read_csv("Moorea" + phylum + "Classification.csv")	
	s = set()
	for i in records.index:
		s.add(records["Scientific Name"].iloc[i])
	s2 = set()
	for i in classificationdf.index:
		s2.add(classificationdf["Scientific Name"].iloc[i])
	for species in s:
		if species not in s2:
			classificationdf = classificationdf.append(pd.DataFrame([species], columns = ["Scientific Name"]))
	classificationdf = classificationdf.reset_index()
	classificationdf = classificationdf.drop(["index", "Unnamed: 0"], axis = 1)
	classificationdf = classificationdf[["Scientific Name", "Native", "Distribution", "Notes"]]
	classificationdf.to_csv("classification.csv")
	return classificationdf

"""
Combines csvs of invasive species in a given location. The csvs should be downloaded from iucngisd.org and should be titled:
"invasivespecies" + "location" + number starting from 1 + ".csv"
"""
def combineCSV(location, numFiles):
	dfList = []
	for i in range(1, numFiles + 1):
		df = pd.read_csv("invasivespecies" + location.replace(" ", "") + str(i) + ".csv", delimiter = ";", index_col = None, header = 0)
		dfList.append(df)
	frame = pd.concat(dfList)
	frame.to_csv("invasivespecies" + location.replace(" ", "") + ".csv")

"""
Returns a set of the invasive species in the given location, read from a csv made by combineCSV. The csv should be titled:
"invasivespecies" + "location" + ".csv" 
"""
def getInvasiveSpecies(location):
	df = pd.read_csv("invasivespecies" + location.replace(" ", "") + ".csv", delimiter = ',')
	return set(df["Species"].tolist())

