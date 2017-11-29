# encoding : utf-8
import json
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.cm as cm
from operator import itemgetter
import operator
import time

"""
Permets de construire les fichiers :
pixel_objet_leve_splite.json
pixel_objet_non_leve_splite.json
"""

file_objet = open("../data_4_tp/data_segmentation_objet.json", "r")
objets_pixels = json.load(file_objet)
file_objet.close()

file = open("../data_4_tp/data_parcelle.json", "r")
parcelles_pixels = json.load(file)
file.close()

file = open("../data_4_tp/parcelles_levees.json", "r")
parcelles_dates_levees = json.load(file)
file.close()

"""
On determine quels sont les pixels leves et non leves dans les parcelles
"""

dates = ["20160806", "20161003", "20161102", "20161122","20161202"]

pixels_parcelles_leves = [] #couple (date,pixel)
pixels_parcelles_non_leves = [] #couple (date,pixel)
association_pixel_parcelle = {} # (pixel)->parcelle

for k,t in parcelles_pixels.items():
	for p in t:
		if p[0] not in association_pixel_parcelle:
			association_pixel_parcelle[p[0]] = {}
		association_pixel_parcelle[p[0]][p[1]] = k

array_pixel = np.array([p for k,t in parcelles_pixels.items() for p in t])
l_min = np.min(array_pixel[:,0])
l_max = np.max(array_pixel[:,0])
c_min = np.min(array_pixel[:,1])
c_max = np.max(array_pixel[:,1])
"""
print(l_min)
print(l_max)
print(c_min)
print(c_max)
"""

for nl in range(l_min,l_max+1):
	for nc in range(c_min,c_max+1):
		pixel = [nl,nc]
		exist = False
		for date in dates:
			levee = False
			non_levee = False
			for parcelle, date_parcelle in parcelles_dates_levees.items():
				if pixel in parcelles_pixels[parcelle]:
					if int(date) >= int(date_parcelle):
						levee = True
					else:
						non_levee = True
			if levee and non_levee :
				raise Exception()
			elif levee:
				pixels_parcelles_leves.append((date,pixel))
			elif non_levee:
				pixels_parcelles_non_leves.append((date,pixel))

print("Nombre de pixels leves dans les parcelles : "+str(len(pixels_parcelles_leves)))	
print("Nombre de pixels non leves dans les parcelles : "+str(len(pixels_parcelles_non_leves)))				

communs = []
for tab in pixels_parcelles_non_leves:
	if tab in pixels_parcelles_leves:
		communs.append(tab)

print(communs)

"""
On determine quels sont les objets leves et non leves
On leur enleve les pixels ne correspondant pas à leur etat
"""
support = 2/3
represantativite = 1/3 
#(nbPixelLeves/(nbPixelLeves+nbPixelNonLeves)>support -> objet leve
#(nbPixelLeves/(nbPixelLeves+nbPixelNonLeves)<(1-support) et >0 -> objet non leve

objets_leves = {}
objets_non_leves = {}

for date, objs in objets_pixels.items():
	for obj, pixels in objs.items():
		liste_pixel_leves = []
		liste_pixel_non_leves = []
		liste_pixel_unknown = []
		representativite_parcelle_levee = {}
		representativite_parcelle_non_levee = {}
		for pixel in pixels:
			if (date,pixel) in pixels_parcelles_leves:
				liste_pixel_leves.append(pixel)
				if pixel[0] in association_pixel_parcelle:
					if pixel[1] in association_pixel_parcelle[pixel[0]]:
						parcelle = association_pixel_parcelle[pixel[0]][pixel[1]]
						if parcelle not in representativite_parcelle_levee:
							representativite_parcelle_levee[parcelle] = 1
						else :
							representativite_parcelle_levee[parcelle] += 1
			elif (date,pixel) in pixels_parcelles_non_leves:
				liste_pixel_non_leves.append(pixel)
				if pixel[0] in association_pixel_parcelle:
					if pixel[1] in association_pixel_parcelle[pixel[0]]:
						parcelle = association_pixel_parcelle[pixel[0]][pixel[1]]
						if parcelle not in representativite_parcelle_non_levee:
							representativite_parcelle_non_levee[parcelle] = 1
						else :
							representativite_parcelle_non_levee[parcelle] += 1
			else:
				liste_pixel_unknown.append(pixel)
		nbl = len(liste_pixel_leves)
		nbnl = len(liste_pixel_non_leves)

		representativite_levee = None
		representativite_non_levee = None

		for parcelle in representativite_parcelle_levee:
			nbPixel = len(parcelles_pixels[parcelle])
			representativite_parcelle_levee[parcelle] /= nbPixel

		for parcelle in representativite_parcelle_non_levee:
			nbPixel = len(parcelles_pixels[parcelle])
			representativite_parcelle_non_levee[parcelle] /= nbPixel

		if len(representativite_parcelle_levee.items()) >0:
			rep_levee = np.array(list(representativite_parcelle_levee.values()))
			representativite_levee = np.max(rep_levee)

		if len(representativite_parcelle_non_levee.items()) >0:
			rep_non_levee = np.array(list(representativite_parcelle_non_levee.values()))
			representativite_non_levee = np.max(rep_non_levee)

		if nbl != 0 or nbnl != 0:
			test = nbl/(nbl+nbnl)
			if test >= support:
				liste_pixels = liste_pixel_leves + liste_pixel_unknown
				if representativite_levee != None and representativite_levee > represantativite:
					objets_leves[date+" "+obj] = pd.Series(liste_pixels).to_json(orient='values')
			elif (1-test) >= support:
				liste_pixels = liste_pixel_non_leves + liste_pixel_unknown
				if representativite_non_levee != None and representativite_non_levee > represantativite:
					objets_non_leves[date+" "+obj] = pd.Series(liste_pixels).to_json(orient='values')

print("Nombre d'objet splite leves : "+str(len(list(objets_leves.keys()))))	
print("Nombre d'objet splite non leves : "+str(len(list(objets_non_leves.keys()))))

pixels_leves = [val for obj, t in objets_leves.items() for val in json.loads(t)]
pixels_non_leves = [val for obj, t in objets_non_leves.items() for val in json.loads(t)]

print("Nombre final de pixels leves : "+str(len(pixels_leves)))	
print("Nombre final de pixels non leves : "+str(len(pixels_non_leves)))


file = open("../data_4_tp/pixel_objet_leve_splite.json", "w")
json.dump(objets_leves,file)
file.close()

file = open("../data_4_tp/pixel_objet_non_leve_splite.json", "w")
json.dump(objets_non_leves,file)
file.close()