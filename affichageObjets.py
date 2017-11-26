import json
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.cm as cm

matrices = {}

file = open("../data_4_tp/data_matrix.json","r")
data = json.load(file)
file.close()

for key in data:
	matrice = np.array(data[key])
	#print(matrice.shape)
	matrices.update({ key : matrice})
file.close()
"""
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
"""


file_objet_leves = open("../data_4_tp/objets_leves.json", "r")
objets_leves = json.load(file_objet_leves).keys()
file_objet_leves.close()

file_objet_non_leves = open("../data_4_tp/objets_non_leves.json", "r")
objets_non_leves = json.load(file_objet_non_leves).keys()
file_objet_non_leves.close()

objets_leves = list(objets_leves)
objets_non_leves = list(objets_non_leves)

"""
print(objets_leves)
print(objets_non_leves)

file = open("../data_4_tp/objets_pixels.json","w")
json.dump(pixels_objet, file)
file.close()
"""
def compute_ndvi(img):
	R=np.array(img[2])
	PIR=np.array(img[6])
	return(PIR-R)/(PIR+R)


file = open("../data_4_tp/objets_pixels.json","r")
pixels_objets =  json.load(file)
file.close()

file = open("../data_4_tp/parcelles_levees.json","r")
parcelles_levees = json.load(file)
file.close()

dates = ["20160806", "20161003", "20161102", "20161122","20161202"]

file = open("../data_4_tp/data_parcelle.json", "r")
data_parcels = json.load(file)
file.close()

plt.figure(figsize=(15,10))
i = 1
for date in dates:
	plt.subplot(2,5,i)
	i += 1
	plt.title("P " + date)
	plt.imshow(compute_ndvi(data[dates[0]]),cmap="gray")
	for parcelle, date_levee in parcelles_levees.items():
		p = np.array(data_parcels[parcelle])
		if int(date_levee) <= int(date):
			plt.scatter(p[:,0],p[:,1],c="green")
		else:
			plt.scatter(p[:,0],p[:,1],c="red")



for date in dates:
	plt.subplot(2,5,i)
	i += 1
	plt.title("O " + date)
	plt.imshow(compute_ndvi(data[dates[0]]),cmap="gray")
	for obj in objets_leves:
		tab = obj.split(" ")
		date_obj = tab[0]
		if obj in pixels_objets:
			p = np.array(pixels_objets[obj])
			#print(obj+str(p))
			if date == date_obj:
				try :
					plt.scatter(p[:,0],p[:,1],c="green")
				except :
					print(str(p) + obj)
					raise

	for obj in objets_non_leves:
		tab = obj.split(" ")
		date_obj = tab[0]
		if obj in pixels_objets:
			p = np.array(pixels_objets[obj])
			if date == date_obj:
				try:
					plt.scatter(p[:,0],p[:,1],c="red")
				except :
					print(str(p) + obj)
					raise


plt.savefig("../data_4_tp/objets_sans_splite.png")
#plt.show()


	



