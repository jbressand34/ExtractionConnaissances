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

file = open("../data_4_tp/jeu_test_trois_dates.json","r")
jeu_test = json.load(file)
file.close()

dates = ["20160806", "20161003", "20161102", "20161122","20161202"]

observations_parcelles = {}
predictions_pixels = {}

"""
Pour les trois dernieres dates on affiche deux figures chacun :
1ere figure : les parcelles qui sont levees en vert 
et non levees en rouge
2eme figure : pour chaaue pixel des parcelles, en vert 
si le modele predit que le pixel est levee, rouge sinon

Pour la premiere figure il nous faut pour chaque date:
- une liste de parcelles levees, chaque parcelle 
levee est une liste de pixel
- une liste de parcelles non levees

{
	"date3":{
		"levees": [[pixel, ,pixel], [pixel, ,pixel]...],
		"non_levees": [[pixel, ,pixel], [pixel, ,pixel]...]
	}
	"date4":{
	
	}
	"date5":{
	
	}
}
"""
def compute_ndvi(img):
    R=np.array(img[2])
    PIR=np.array(img[6])
    return(PIR-R)/(PIR+R)


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


"""
Pour la deuxieme figure il nous faut pour chaque date :
- Une liste de pixel levees 
- Une liste de pixels non levees
"""

for date in dates[2:]:
	pixels_levees = []
	pixels_non_levees = []
	date_prev = getDatePrev(date)
	date_prev_prev = getDatePrev(date_prev)
	dates_sample = [date,date_prev,date_prev_prev]

	for parcelle in parcelles_date:
		for pixel in data_parcels[parcelle]:
			sample = []
			for d in dates_sample:
				for i in range(0,10):
					sample.append([data[d][i][pixel[0]][pixel[1]]])
			sample = np.array([[sample]])
			pred = modele.predict(sample)
			prediction = 0
			if pred[0][1]>pred[0][0]:
				prediction = 1		
			if prediction == 1:
				pixels_levees.append(pixel)
			elif prediction == 0:
				pixels_non_levees.append(pixel)
			else:
				raise
	predictions_pixels[date]={
		"levees": pixels_levees,
		"non_levees": pixels_non_levees
	}

for date in predictions_pixels:
	print(date+" : ")
	print("Nombre de pixels levees : "+\
		str(len(predictions_pixels[date]["levees"])))
	print("Nombre de pixels non levees : "+\
		str(len(predictions_pixels[date]["non_levees"])))



#prediction = np.argsort(model.predict())
pdf = PdfPages("../data_4_tp/prediction.pdf")

prediction_rouge = {}
prediction_vert = {}
test_rouge = {}
test_vert = {}
for date in dates[2:]:
	test_rouge[date] = []
	test_vert[date] = []
	prediction_rouge[date] = []
	prediction_vert[date] = []

for i in range(0, len(jeu_test['pixels'])):
	pixel = jeu_test['pixels'][i]
	label = jeu_test['labels'][i]
	date = jeu_test['dates'][i]
	canaux = jeu_test['canaux'][i]
	if label == 1 :
		test_vert[date].append(pixel) 
	else:
		test_rouge[date].append(pixel)

	p = [[val] for val in canaux[0]]+\
	[[val] for val in canaux[1]]+\
	[[val] for val in canaux[2]]
	pred = modele.predict(np.array([[p]]))
	prediction = 0
	if pred[0][1] > pred[0][0]:
		prediction = 1
	if prediction == 1:
		prediction_vert[date].append(pixel)
	else:
		prediction_rouge[date].append(pixel)

for date in dates[2:]:
	plt.figure()#figsize=(150,100)
	plt.subplot(1,2,1)
	plt.title(date + " observations")
	plt.imshow(compute_ndvi(data["20160806"]),cmap="gray")
	"""
	for pixels in observations_parcelles[date]["levees"]:  
		p = np.array(pixels)
		plt.scatter(p[:,0],p[:,1],c='green')
	for pixels in observations_parcelles[date]["non_levees"]:	
		p = np.array(pixels)
		plt.scatter(p[:,0],p[:,1],c='red')
	"""
	if len(test_vert[date])>0:
		p = np.array(test_vert[date])
		plt.scatter(p[:,0],p[:,1],c='green')
	if len(test_rouge[date])>0:
		p = np.array(test_rouge[date])
		plt.scatter(p[:,0],p[:,1],c='red')

	plt.subplot(1,2,2)
	plt.title(date + " predictions")
	plt.imshow(compute_ndvi(data["20160806"]),cmap="gray")
	"""
	if len(predictions_pixels[date]["levees"])>0:  
		p = np.array(predictions_pixels[date]["levees"])
		#print(p.shape)
		plt.scatter(p[:,0],p[:,1],c='green')
	if len(predictions_pixels[date]["non_levees"])>0:
		p = np.array(predictions_pixels[date]["non_levees"])
		#print(p.shape)
		plt.scatter(p[:,0],p[:,1],c='red')
	"""
	if len(prediction_vert[date])>0:
		p = np.array(prediction_vert[date])
		plt.scatter(p[:,0],p[:,1],c='green')
	if len(prediction_rouge[date])>0:
		p = np.array(prediction_rouge[date])
		plt.scatter(p[:,0],p[:,1],c='red')
	plt.show()
	#pdf.savefig()
pdf.close()
