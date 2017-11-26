# encoding : utf-8
import json
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.cm as cm
from operator import itemgetter
import operator
import time

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
		levees[row["ID2"]]=20160806
for id, row in file2.iterrows():    
	if("croissance" in row["Culture"] and row["ID2"] not in levees):
		levees[row["ID2"]]=20161003
for id, row in file3.iterrows():
	if("croissance" in row["Culture"] and row["ID2"] not in levees):
		levees[row["ID2"]]=20161102
for id, row in file4.iterrows():
	if("croissance" in row["Culture"] and row["ID2"] not in levees):
		levees[row["ID2"]]=20161122
for id, row in file5.iterrows():
	if("croissance" in row["Culture"] and row["ID2"] not in levees):
		levees[row["ID2"]]=20161202

"""
print("@--Levees--@")
for key in levees:
   print(key+" "+str(levees[key]))
"""
objets = {}
pixels_objet = {}
nb_pixel_objet = {}

file_objet = open("../data_4_tp/data_segmentation_objet.json", "r")
data_objet = json.load(file_objet)
file_objet.close()

for date, val1 in data_objet.items():
	for objet, val2 in val1.items():
		nb_pixel_objet[date+" "+objet]=0
		pixels_objet[date+" "+objet] = []
		for pixel in val2:
			nb_pixel_objet[date+" "+objet] += 1
			pixels_objet[date+" "+objet].append(pixel)

def appartenance_parcel(liste_pixeles):
	dico = {}
	#print( len(liste_pixeles))
	for parcelle, val1 in parcelle_pixel.items():
		for pixel in liste_pixeles:
			if pixel in val1:
				if parcelle not in dico:
					dico[parcelle] = 1
				else :
					dico[parcelle] += 1
	return dico            


#nbObj = 0
"""
nbRepet=0
objs = {}
"""
"""
for date, val1 in data_objet.items():
	for objet, val2 in val1.items():
		nbObj += 1
"""
"""
		if objet not in objs:
			objs[objet] = []
			objs[objet].append(val2.sort())
		elif objs[objet][0] != val2.sort():
			print(objs[objet][0])
			print(val2.sort())
			raise Exception("Les pixels sont différents")
		else :
			objs[objet].append(val2.sort())

		if len(objs[objet])==5:
			nbRepet += 1
"""
#print("Nombre d'objet : "+str(len(objs)))
#print("Nombre d'objet appartenant aux 5 dates : "+str(nbRepet))
"""
avancement = -1
compteur = 0
debut = time.time()
encours = time.time()
for date in data_objet:
	for objet in data_objet[date]:
		if int(compteur*100/nbObj) > avancement:
			avancement = int(compteur*100/nbObj)
			print(str(avancement)+"% "+str(int(time.time()-encours))+"s")
			encours = time.time()
		compteur += 1
		liste_pixeles = data_objet[date][objet]
		_parcelles = appartenance_parcel(liste_pixeles)
		objets.update({date +" " + objet : _parcelles })
print("Durée : "+str(int(time.time()-debut))+"s")

file = open("../data_4_tp/objets.json", "w")
json.dump(objets,file)
file.close()
"""
file = open("../data_4_tp/objets.json")
objets = json.load(file)
file.close()



objets_levees = []
objets_non_levees = []

for key, val in objets.items():
	tab = key.split(" ")
	date = tab[0]
	objet = tab[1]
	nbPixelTotal = nb_pixel_objet[key]
	nbPixelsLevees = 0
	nbPixelsNonLevees = 0
	for parcelle, nbPixel in val.items():
		if parcelle in levees and levees[parcelle] <= int(date):
			nbPixelsLevees += nbPixel
		elif parcelle in levees :
			nbPixelsNonLevees += nbPixel
	if nbPixelsLevees/nbPixelTotal > 1/4 and nbPixelsLevees>nbPixelsNonLevees:
		objets_levees.append(key)
	elif nbPixelsNonLevees > 1/4 and nbPixelsNonLevees>nbPixelsLevees:
		objets_non_levees.append(key)

print("Nombre d'objets levees : "+str(len(objets_levees)))
print("Nombre d'objets non levees : "+str(len(objets_non_levees)))

nbPixelLevees = 0
nbPixelNonLevees = 0

for obj in objets_levees:
	nbPixelLevees+=nb_pixel_objet[obj]
for obj in objets_non_levees:
	nbPixelNonLevees+=nb_pixel_objet[obj]

print("Nombre de pixels levees : "+str(nbPixelLevees))
print("Nombre de pixels non levees : "+str(nbPixelNonLevees))

objets_levees_dump = {}
objets_non_levees_dump = {}

dates = ["20160806", "20161003", "20161102", "20161122","20161202"]

def getDatePrev(date):
	datePrev = None
	if date == dates[0]:
		datePrev = None
	elif date == dates[1]:
		datePrev = dates[0]
	elif date == dates[2]:
		datePrev = dates[1]
	elif date == dates[3]:
		datePrev = dates[2]
	elif date == dates[4]:
		datePrev = dates[3]
	else:
		print(date)
		print(date==date[0])
		raise Exception()
	return datePrev

for obj in objets_levees:
	tab = key.split(" ")
	date = tab[0]
	datePrev = getDatePrev(date)
	matrice = []
	matrice_prev = []
	for pixel in pixels_objet[obj]:
		signaux = []
		signaux_prev = []
		for numsignal in range(0,10):
			signal = matrices[date][numsignal][pixel[0]][pixel[1]]
			signaux.append(signal)
			if datePrev != None :
				signal_prev = matrices[datePrev][numsignal][pixel[0]][pixel[1]]
				signaux_prev.append(signal_prev)
			else:
				print(datePrev)
				raise Exception()
		matrice.append(signaux)
		matrice_prev.append(signaux_prev)
	m = []
	m.append(matrice)
	m.append(matrice_prev)	
	objets_levees_dump[obj] = pd.Series(m).to_json(orient='values')


for obj in objets_non_levees:
	tab = key.split(" ")
	date = tab[0]
	datePrev = getDatePrev(date)
	matrice = []
	matrice_prev = []
	for pixel in pixels_objet[obj]:
		signaux = []
		signaux_prev = []
		for numsignal in range(0,10):
			signal = matrices[date][numsignal][pixel[0]][pixel[1]]
			signaux.append(signal)
			if datePrev != None :
				signal_prev = matrices[datePrev][numsignal][pixel[0]][pixel[1]]
				signaux_prev.append(signal_prev)
		matrice.append(signaux)
		matrice_prev.append(signaux_prev)
	m = []
	m.append(matrice)
	m.append(matrice_prev)	
	objets_non_levees_dump[obj] = pd.Series(m).to_json(orient='values')

#pd.DataFrame(objets_levees_dump).to_json('../data_4_tp/objets_leves.json')
#pd.DataFrame(objets_non_levees_dump).to_json('../data_4_tp/objets_non_leves.json')

for key, val in objets_levees_dump.items():
	print(val)
	break
file = open("../data_4_tp/objets_leves_deux_dates.json","w")
json.dump(objets_levees_dump,file, indent=True)
file.close()
file = open("../data_4_tp/objets_non_leves_deux_dates.json","w")
json.dump(objets_non_levees_dump,file, indent=True)
file.close()
