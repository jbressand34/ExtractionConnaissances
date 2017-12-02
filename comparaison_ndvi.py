import json
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import keras
from keras.models import model_from_json
from matplotlib.backends.backend_pdf import PdfPages


json_modele = open("../data_4_tp/modele.json", "r")
modele = model_from_json(json_modele.readline())
json_modele.close()
modele.load_weights('../data_4_tp/modele_poids.h5')

file = open("../data_4_tp/data_matrix.json","r")
data = json.load(file)
file.close()

file = open("../data_4_tp/data_parcelle.json")
data_parcels = json.load(file)
file.close()

file = open("../data_4_tp/parcelles_levees.json","r")
parcelles_date = json.load(file)
file.close()

dates = ["20160806", "20161003", "20161102", "20161122","20161202"]

observations_parcelles = {}
ndvi_parcelles = {}

def compute_ndvi(img):
	R=np.array(img[2])
	PIR=np.array(img[6])
	return(PIR-R)/(PIR+R)

for date in dates[2:]:
	parcelles_levees = []
	parcelles_non_levees = []

	for parcelle in parcelles_date:
		pixels_levees = []
		pixels_non_levees = []
		for pixel in data_parcels[parcelle]:
			sample = []
			for i in range(0,10):
				sample.append([data[date][i][pixel[0]][pixel[1]]])
			if compute_ndvi(sample) > 0.4:
				pixels_levees.append(pixel)
			else:
				pixels_non_levees.append(pixel)
		if len(pixels_levees) != 0:		
			parcelles_levees.append(pixels_levees)
		if len(pixels_non_levees) != 0:		
			parcelles_non_levees.append(pixels_non_levees)
	ndvi_parcelles[date] = {
		"levees": parcelles_levees,
		"non_levees": parcelles_non_levees
		}


for date in dates[2:]:
	parcelles_levees = []
	parcelles_non_levees = []

	for parcelle, date_parcelle in \
	parcelles_date.items():
		pixels = data_parcels[parcelle]
		if int(date)>=int(date_parcelle):
			parcelles_levees.append(pixels)
		else:
			parcelles_non_levees.append(pixels)
				
	observations_parcelles[date] = {
		"levees": parcelles_levees,
		"non_levees": parcelles_non_levees
		}

pdf = PdfPages("../data_4_tp/comparaison_ndvi.pdf")


for date in dates[2:]:
	plt.figure()#figsize=(150,100)
	plt.subplot(1,2,1)
	plt.title(date + " observations")
	plt.imshow(compute_ndvi(data["20160806"]),cmap="gray")
	for pixels in observations_parcelles[date]["levees"]:  
		p = np.array(pixels)
		plt.scatter(p[:,0],p[:,1],c='green')
	for pixels in observations_parcelles[date]["non_levees"]:	
		p = np.array(pixels)
		plt.scatter(p[:,0],p[:,1],c='red')

	plt.subplot(1,2,2)
	plt.title(date + " ndvi")
	plt.imshow(compute_ndvi(data["20160806"]),cmap="gray")

	for pixels in ndvi_parcelles[date]["levees"]:  
		p = np.array(pixels)
		plt.scatter(p[:,0],p[:,1],c='green')
	for pixels in ndvi_parcelles[date]["non_levees"]:  
		p = np.array(pixels)
		plt.scatter(p[:,0],p[:,1],c='red')
	plt.show()
	#pdf.savefig()
pdf.close()
