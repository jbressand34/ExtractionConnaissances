# endoding : utf-8
import json
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.cm as cm
from operator import itemgetter
import operator

dates = []
matrices = []

file = open("../data_4_tp/data_matrix.json","r")
data = json.load(file)
file.close()

for key in data:
    dates.append(key)
    matrice = np.array(data[key])
    #print(matrice.shape)
    matrices.append(matrice)
file.close()

parcelles = {} #dictionnaire de matrices (5*10*nbPixel)
levees = {} #cle = parcelle, valeur = indice de levee 
non_levees = {}

file = open("../data_4_tp/data_parcelle.json", "r")
data_parcels = json.load(file)

for key in data_parcels :
    parcelle = []
    for i in range(0,5):
        image = []
        for j in range(0,10):
            matrice_pixel = []
            for pixel in data_parcels[key]:
                nbLigne = pixel[0]
                nbColonne = pixel[1]
                matrice_pixel.append(matrices[i][j][nbLigne][nbColonne])
            image.append(matrice_pixel)
        parcelle.append(image)
    parcelles.update({key : np.array(parcelle)})
file.close()

#print(parcelles.keys())

file1 = pd.read_csv("../data_4_tp/14072016_observations.csv")
file2 = pd.read_csv("../data_4_tp/28092016_observations.csv")
file3 = pd.read_csv("../data_4_tp/03112016_observations.csv")
file4 = pd.read_csv("../data_4_tp/21112016_observations.csv")
file5 = pd.read_csv("../data_4_tp/02122016_observations.csv")


for id, row in file1.iterrows():
    #print(row["ID2"] + " " + row["Culture"])
    if("croissance" in row["Culture"] and row["ID2"] not in levees):
        levees[row["ID2"]]=1
        non_levees[row["ID2"]]=5
for id, row in file2.iterrows():
    #print(row["ID2"] + " " + row["Culture"])
    if("croissance" in row["Culture"] and row["ID2"] not in levees):
        levees[row["ID2"]]=2
        non_levees[row["ID2"]]=1
for id, row in file3.iterrows():
    #print(row["ID2"] + " " + row["Culture"])
    if("croissance" in row["Culture"] and row["ID2"] not in levees):
        levees[row["ID2"]]=3
        non_levees[row["ID2"]]=2
for id, row in file4.iterrows():
    #print(row["ID2"] + " " + row["Culture"])
    if("croissance" in row["Culture"] and row["ID2"] not in levees):
        levees[row["ID2"]]=4
        non_levees[row["ID2"]]=3
for id, row in file5.iterrows():
    #print(row["ID2"] + " " + row["Culture"])
    if("croissance" in row["Culture"] and row["ID2"] not in levees):
        levees[row["ID2"]]=5
        non_levees[row["ID2"]]=4


print("@--Levees--@")
for key in levees:
   print(key+" "+str(levees[key]))
print("@--Non-Levees--@")
for key in non_levees:
   print(key+" "+str(non_levees[key]))


differences = {}
differences2 = {}

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

for key in non_levees:
    matrice = parcelles[key][non_levees[key]-1] - parcelles[key][non_levees[key]-2]
    differences2.update({key : matrice})
"""
print("@--Differences levees--@")
for key in differences:
    print(key+" : "+str(differences[key]))
print("@--Differences non levees--@")
for key in differences2:
    print(key+" : "+str(differences2[key]))
"""

#print(differences["C57"])
#print(differences["C57"].shape)

def compute_ndvi(img):
    R=np.array(img[2])
    PIR=np.array(img[6])
    return(PIR-R)/(PIR+R)

plt.figure(figsize=(15,10))
keys = {}
keys2 = {}
max = 0
item = [3,4,5,6,7,8,9]
for key in levees:
    #print(differences[key].mean())
    moyennes = []
    moyennes2 = []
    for indice in item:
        try :
            moyennes.append(differences[key][indice])
            moyennes2.append(differences2[key][indice])
        except :
            print(len(differences[key]))
            print(differences[key].shape)
            raise
    moyenne = np.array(moyennes).mean()
    moyenne2 = np.array(moyennes2).mean()
    if moyenne > max :
        max = moyenne
    elif -moyenne > max:
        max = -moyenne
    keys.update({key:moyenne})
    keys2.update({key:moyenne2})
"""
print("@-- Moyennes levees --@")
for key in keys:
    print(key+" : "+str(keys[key]))
print("@-- Moyennes non levees --@")
for key in keys2:
    print(key+" : "+str(keys2[key]))
"""
colorsN = cm.winter(np.linspace(0, 1, 10))
colorsP = cm.spring(np.linspace(0, 1, 10))

tri = sorted(keys.items(), key=operator.itemgetter(1))
tri2 = sorted(keys2.items(), key=operator.itemgetter(1))

#print(tri)
plt.subplot(1,2,1)
plt.imshow(compute_ndvi(data["20160806"]),cmap="gray")
plt.title("levee")
i=0
for val in tri:
    try:
        p=np.array(data_parcels[val[0]])
        #print(differences[key].mean())
        if val[1] < 0 :
            couleur = colorsN[i]
        else:
            couleur = colorsP[i]    
        #print(couleur)
        plt.scatter(p[:,0],p[:,1],c=couleur)
    except:
        pass
    i+=1

plt.subplot(1,2,2)
plt.imshow(compute_ndvi(data["20160806"]),cmap="gray")
plt.title("non_levee")
i=0
for val in tri2:
    try:
        p=np.array(data_parcels[val[0]])
        #print(val[1])
        if val[1] < 0 :
            couleur = colorsN[i]

        else:
            couleur = colorsP[i]    
        #print(couleur)
        plt.scatter(p[:,0],p[:,1],c=couleur)
    except:
        pass
    i+=1

plt.show()





"""
for parcelle in parcelles:
    print(parcelle.shape)
"""

