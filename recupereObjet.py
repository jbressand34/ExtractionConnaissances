# endoding : utf-8
import json
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.cm as cm
from operator import itemgetter
import operator

matrices = {}

file = open("../data_4_tp/data_matrix.json","r")
data = json.load(file)
file.close()

for key in data:
    matrice = np.array(data[key])
    #print(matrice.shape)
    matrices.update({ key : matrice})
file.close()

parcelles = {} #dictionnaire de matrices (5*10*nbPixel)
levees = {} #cle = parcelle, valeur = indice de levee 
#non_levees = {}
parcelle_pixel = {}

file = open("../data_4_tp/data_parcelle.json", "r")
data_parcels = json.load(file)

for key in data_parcels :
    parcelle = []
    for date in matrices:
        image = []
        for j in range(0,10):
            matrice_pixel = []
            for pixel in data_parcels[key]:
                nbLigne = pixel[0]
                nbColonne = pixel[1]
                matrice_pixel.append(matrices[date][j][nbLigne][nbColonne])
            image.append(matrice_pixel)
        parcelle.append(image)
    parcelles.update({key : np.array(parcelle)})
file.close()

for p in data_parcels:
    data_parcel = []
    for pixel in data_parcels[p]:
        data_parcel.append(pixel)
        data_parcel.append(pixel)
    parcelle_pixel.update({p : data_parcel})    
       
    


file1 = pd.read_csv("../data_4_tp/14072016_observations.csv")
file2 = pd.read_csv("../data_4_tp/28092016_observations.csv")
file3 = pd.read_csv("../data_4_tp/03112016_observations.csv")
file4 = pd.read_csv("../data_4_tp/21112016_observations.csv")
file5 = pd.read_csv("../data_4_tp/02122016_observations.csv")

for id, row in file1.iterrows():
    if("croissance" in row["Culture"] and row["ID2"] not in levees):
        levees[row["ID2"]]=1 
for id, row in file2.iterrows():    
    if("croissance" in row["Culture"] and row["ID2"] not in levees):
        levees[row["ID2"]]=2
for id, row in file3.iterrows():
    if("croissance" in row["Culture"] and row["ID2"] not in levees):
        levees[row["ID2"]]=3
for id, row in file4.iterrows():
    if("croissance" in row["Culture"] and row["ID2"] not in levees):
        levees[row["ID2"]]=4
for id, row in file5.iterrows():
    if("croissance" in row["Culture"] and row["ID2"] not in levees):
        levees[row["ID2"]]=5

"""
print("@--Levees--@")
for key in levees:
   print(key+" "+str(levees[key]))
"""
objets = {}

file_objet = open("../data_4_tp/data_segmentation_objet.json", "r")
data_objet = json.load(file_objet)
file_objet.close()

def appartenance_parcel(liste_pixeles):
    liste = []
    #print( len(liste_pixeles))
    for pixel in liste_pixeles:
        for parcelle in parcelle_pixel:
            if pixel in parcelle_pixel[parcelle] and \
                parcelle not in liste:
                liste.append(parcelle)
    return liste            


nbObj = 0
nbRepet=0
objs = []

for date in data_objet:
    for objet in data_objet[date]:
        nbObj += 1
        if objet in objs:
            nbRepet += 1
        else:
            objs.append(objet)
print("Nombre d'objet : "+str(nbObj))
print("Nombre de repetition : "+str(nbRepet))

avancement = -1
compteur = 0
for date in data_objet:
    for objet in data_objet[date]:
        if int(compteur*100/nbObj) > avancement:
            avancement = int(compteur*100/nbObj)
            print(str(avancement)+"%")
        compteur += 1
        liste_pixeles = data_objet[date][objet]
        _parcelles = appartenance_parcel(liste_pixeles)
        objets.update({date +" " + objet : _parcelles })

for o in objets:
    print(o + " " + objets[o])