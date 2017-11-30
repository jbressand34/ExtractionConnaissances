import json
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.cm as cm

levees = {}

file1 = pd.read_csv("../data_4_tp/14072016_observations.csv")
file2 = pd.read_csv("../data_4_tp/28092016_observations.csv")
file3 = pd.read_csv("../data_4_tp/03112016_observations.csv")
file4 = pd.read_csv("../data_4_tp/21112016_observations.csv")
file5 = pd.read_csv("../data_4_tp/02122016_observations.csv")

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

file = open("../data_4_tp/parcelles_levees.json","w")
json.dump(levees, file, indent=1)
file.close()