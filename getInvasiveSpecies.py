import matplotlib.pyplot as plt
import numpy as np
import pandas as pd



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

