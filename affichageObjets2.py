import json
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.cm as cm

file = open("../data_4_tp/data_matrix.json","r")
data = json.load(file)
file.close()


file_objet_leves = open("../data_4_tp/pixel_objet_leve_splite.json", "r")
pixels_objets_leves = json.load(file_objet_leves)
file_objet_leves.close()

file_objet_non_leves = open("../data_4_tp/pixel_objet_non_leve_splite.json", "r")
pixels_objets_non_leves = json.load(file_objet_non_leves)
file_objet_non_leves.close()

def compute_ndvi(img):
	R=np.array(img[2])
	PIR=np.array(img[6])
	return(PIR-R)/(PIR+R)

dates = ["20160806", "20161003", "20161102", "20161122","20161202"]

file = open("../data_4_tp/data_parcelle.json", "r")
data_parcels = json.load(file)
file.close()

file = open("../data_4_tp/parcelles_levees.json","r")
parcelles_levees = json.load(file)
file.close()

for date in dates:
	plt.figure(figsize=(150,100))
	i = 1
	plt.subplot(1,2,i)
	i += 1
	plt.title("P " + date)
	plt.imshow(compute_ndvi(data[dates[0]]),cmap="gray")
	for parcelle, date_levee in parcelles_levees.items():
		p = np.array(data_parcels[parcelle])
		if int(date_levee) <= int(date):
			plt.scatter(p[:,0],p[:,1],c="green")
		else:
			plt.scatter(p[:,0],p[:,1],c="red")

	plt.subplot(1,2,i)
	i += 1
	plt.title("O " + date)
	plt.imshow(compute_ndvi(data[dates[0]]),cmap="gray")
	
	for obj, pixels in pixels_objets_leves.items():
		tab = obj.split(" ")
		date_obj = tab[0]
		p = np.array(json.loads(pixels))
			#print(obj+str(p))
		if date == date_obj:
			try :
				plt.scatter(p[:,0],p[:,1],c="green")
			except :
				print(str(p) + obj)
				raise
	
	for obj, pixels in pixels_objets_non_leves.items():
		tab = obj.split(" ")
		date_obj = tab[0]
		p = np.array(json.loads(pixels))
		if date == date_obj:
			try:
				plt.scatter(p[:,0],p[:,1],c="red")
			except :
				print(str(p) + obj)
				raise
	

	plt.savefig("../data_4_tp/objets_splite_"+date+".pdf")
	print("Fin : "+date)

	



