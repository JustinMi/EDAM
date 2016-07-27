import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

"""
Cleans species record data given by Moorea Biocode Project. The record data should be converted to csv.
"""
def cleanMooreaRecords(inputFile, outputFile):
	df = pd.read_csv(inputFile)
	speciesSet = set()
	df = df[["seq_num[ce]", "MinElevationMeters[ce]", "MaxElevationMeters[ce]", "ScientificName", "Genus", "SpecificEpithet", "DecimalLatitude[ce]", "DecimalLongitude[ce]"]]
	df["Scientific Name"] = df["ScientificName"].astype(str)
	df["Min Elevation"] = df["MinElevationMeters[ce]"]
	df["Max Elevation"] = df["MaxElevationMeters[ce]"]
	df["Latitude"] = df["DecimalLatitude[ce]"]
	df["Longitude"] = df["DecimalLongitude[ce]"]
	df["Specific Epithet"] = df["SpecificEpithet"]
	clean = []
	for i in df.index:
		if df["Scientific Name"].iloc[i] != "NaN" and " " in df["Scientific Name"].iloc[i] and "sp." not in df["Scientific Name"].iloc[i]:
			clean.append(i)
	df = df.iloc[clean]
	df["Scientific Name"] = df["Scientific Name"].str.lower()
	df = df.reset_index()
	df = df.drop(["index", "ScientificName", "MinElevationMeters[ce]", "MaxElevationMeters[ce]", "DecimalLatitude[ce]", "DecimalLongitude[ce]", "SpecificEpithet"], axis = 1)
	df.to_csv(outputFile)
	return df

"""
Cleans species data given by Moorea Biocode Project. The species data should be converted to csv.
"""
def cleanMooreaSpecies(inputFile, outputFile):
	df = pd.read_csv(inputFile)
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
	df.to_csv(outputFile)
	return df

"""
Not all the species are actually in the species data given by the Moorea Biocode Project. The function utilizes the records data and combines it with the 
classification data to get all species.
"""
def getAllSpecies(recordsFile, classificationFile, outputFile, phylum):
	records = pd.read_csv(recordsFile)
	classificationdf = pd.read_csv(classificationFile)	
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
	classificationdf.to_csv(outputFile)
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


