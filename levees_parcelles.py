import json
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.cm as cm

#print("\nCréation d'un fichier json qui contient les parcelles levées en se basant sur les observations.")
file_config = open("config.json", "r")
config = json.load(file_config)
file_config.close()
path = config["pathToDataDirectory"]

levees = {}

file1 = pd.read_csv("path/14072016_observations.csv")
file2 = pd.read_csv("path/28092016_observations.csv")
file3 = pd.read_csv("path/03112016_observations.csv")
file4 = pd.read_csv("path/21112016_observations.csv")
file5 = pd.read_csv("path/02122016_observations.csv")

for id, row in file1.iterrows():
    if("croissance" in row["Culture"] and row["CODE_2016_"] not in levees):
        levees[row["CODE_2016_"]]= "20160806"
for id, row in file2.iterrows():    
    if("croissance" in row["Culture"] and row["CODE_2016_"] not in levees):
        levees[row["CODE_2016_"]]="20161003"
for id, row in file3.iterrows():
    if("croissance" in row["Culture"] and row["CODE_2016_"] not in levees):
        levees[row["CODE_2016_"]]="20161102"
for id, row in file4.iterrows():
    if("croissance" in row["Culture"] and row["CODE_2016_"] not in levees):
        levees[row["CODE_2016_"]]="20161122"
for id, row in file5.iterrows():
    if("croissance" in row["Culture"] and row["CODE_2016_"] not in levees):
        levees[row["CODE_2016_"]]="20161202"

file = open("path/parcelles_levees.json","w")
json.dump(levees, file, indent=1)
file.close()