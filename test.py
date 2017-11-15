# endoding : utf-8
import json
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.cm as cm 

file = open("data_4_tp/data_matrix.json","r")
data = json.load(file)

dates = []
matrices = []

for key in data:
	dates.append(key)
	matrice = np.array(data[key])
	#print(matrice.shape)
	matrices.append(matrice)
file.close()

parcelles = {} #dictionnaire de matrices (5* nbPixel * 10)
levees = {} #cle = parcelle, valeur = indice de levee 


file = open("data_4_tp/data_parcelle.json", "r")
data = json.load(file)

for key in data :
	parcelle = []
	for i in range(0,5):
		image = []
		for pixel in data[key]:
			nbLigne = pixel[0]
			nbColonne = pixel[1]
			matrice_pixel = []
			for j in range(0,10):
				matrice_pixel.append(matrices[i][j][nbLigne][nbColonne])
			image.append(matrice_pixel)
		parcelle.append(image)
	parcelles.update({key : np.array(parcelle)})
file.close()

#print(parcelles.keys())

file1 = pd.read_csv("data_4_tp/14072016_observations.csv")
file2 = pd.read_csv("data_4_tp/28092016_observations.csv")
file3 = pd.read_csv("data_4_tp/03112016_observations.csv")
file4 = pd.read_csv("data_4_tp/21112016_observations.csv")
file5 = pd.read_csv("data_4_tp/02122016_observations.csv")


for id, row in file1.iterrows():
	#print(row["ID2"] + " " + row["Culture"])
	if("croissance" in row["Culture"] and row["ID2"] not in levees):
		levees[row["ID2"]]=1
for id, row in file2.iterrows():
	#print(row["ID2"] + " " + row["Culture"])
	if("croissance" in row["Culture"] and row["ID2"] not in levees):
		levees[row["ID2"]]=2
for id, row in file3.iterrows():
	#print(row["ID2"] + " " + row["Culture"])
	if("croissance" in row["Culture"] and row["ID2"] not in levees):
		levees[row["ID2"]]=3
for id, row in file4.iterrows():
	#print(row["ID2"] + " " + row["Culture"])
	if("croissance" in row["Culture"] and row["ID2"] not in levees):
		levees[row["ID2"]]=4
for id, row in file5.iterrows():
	#print(row["ID2"] + " " + row["Culture"])
	if("croissance" in row["Culture"] and row["ID2"] not in levees):
		levees[row["ID2"]]=5
"""
for key in levees:
	print(key+" "+str(levees[key]))
"""

differences = {}

max = 0

for key in levees:
	matrice = parcelles[key][levees[key]-1] - parcelles[key][levees[key]-2]
	differences.update({key : matrice})
	if np.max(matrice) > max:
		max = np.max(matrice)
	if -np.min(matrice) > max:
		max = -np.min(matrice)
	#plt.matshow(matrice, cmap='Greys')
	#plt.show()

colors = cm.gray(np.linspace(-max, max, 10))
print(max)
for matrice in differences:
	plt.imshow(matrice, cmap='gray', vmin=-max, vmax=max)
	plt.show()




"""
for parcelle in parcelles:
	print(parcelle.shape)
"""

