import json
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import time


file = open("../data_4_tp/objets_pixels.json","r")
pixels_objets =  json.load(file)
file.close()

file_objet_leves = open("../data_4_tp/objets_leves.json", "r")
objets_leves = json.load(file_objet_leves).keys()
file_objet_leves.close()

file_objet_non_leves = open("../data_4_tp/objets_non_leves.json", "r")
objets_non_leves = json.load(file_objet_non_leves).keys()
file_objet_non_leves.close()

objets_leves = list(objets_leves)
objets_non_leves = list(objets_non_leves)


supprime_pixels = []

_pixels = list(pixels_objets.values())
lignes = [val[0] for val in _pixels]
colonnes = [val[1] for val in _pixels]
lignes = np.array(lignes)
colonnes = np.array(colonnes)
l_min = np.min(lignes)
l_max = np.max(lignes)
c_min = np.min(colonnes)
c_max = np.max(colonnes)

nb = (l_max-l_min)*(c_max-c_min)
avancement = -1
compteur = 0
debut = time.time()
encours = time.time()

dates = ["20160806", "20161003", "20161102", "20161122","20161202"]

for l in range(l_min,l_max+1):
	for c in range(c_min,c_max+1):
		if avancement < int(100*compteur/nb):
			avancement = int(100*compteur/nb)
			print(str(avancement)+"% "+str(time.time()-encours)+"s")
			encours = time.time()
		compteur+=1
		pixel = [l,c]
		for date in dates:
			levee = False
			non_levees = False

			for obj in objets_leves:
				date_obj = obj.split(" ")[0]
				if date_obj == date and pixel in pixels_objets[obj]:
					levee = True
					break

			for obj in objets_non_leves:
				date_obj = obj.split(" ")[0]
				if date_obj == date and pixel in pixels_objets[obj]:
					non_levee = True
					break
			if levee and non_levee:
				supprime_pixels.append((date,pixel))
				print("coucou")
print("Fin parcours pixel : "+str(time.time()-debut)+"s")

pixels_objets_splite = {}

for obj in objets_leves :

	date = obj.split(" ")[0]
	pixels = pixels_objets[obj]
	pixels_objets_splite.update({obj:pixels})

	"""
	for tab in supprime_pixels:
		date_p = tab[0]
		p = tab[1]
		if date == date_p and p in pixels:
			pixels.remove(p) #list(filter(lambda a: a!= p, pixels))
	if len(pixels)>0:
		pixels_objets_splite.update({obj:pixels})
	else:
		print("Suppression de lobjet leve : "+obj)
	"""

for obj in objets_non_leves :
	pixels = pixels_objets[obj]
	date = obj.split(" ")[0]
	for tab in supprime_pixels:
		date_p = tab[0]
		p = tab[1]
		if date == date_p and p in pixels:
			pixels.remove(p) #= list(filter(lambda a: a!= p, pixels))
	if len(pixels)>0:
		pixels_objets_splite.update({obj:pixels})

file = open("../data_4_tp/pixels_objets_splite.json", "w")
json.dump(pixels_objets_splite, file,  indent = 1 )
file.close()