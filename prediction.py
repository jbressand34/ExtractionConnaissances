import json
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import keras
from keras.models import model_from_json
from matplotlib.backends.backend_pdf import PdfPages

file_config = open("config.json", "r")
config = json.load(file_config)
file_config.close()
path = config["pathToDataDirectory"]

json_modele = open(path+"modele.json", "r")
modele = model_from_json(json_modele.readline())
json_modele.close()
modele.load_weights(path+'modele_poids.h5')

	
file = open(path+"data_matrix.json","r")
data = json.load(file)
file.close()

file = open(path+"jeu_test_trois_dates.json","r")
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


prediction_rouge = {}
prediction_vert = {}
test_rouge = {}
test_vert = {}
for date in dates[2:]:
	test_rouge[date] = []
	test_vert[date] = []
	prediction_rouge[date] = []
	prediction_vert[date] = []


h = 10 * int(config["tailleSequenceInputModele"])
if h > 30:
	raise Exeption("0 < tailleSequenceInputModele <= 3")


labels = []
trois_canaux = []
for i in range(0, len(jeu_test['pixels'])):
	#label = jeu_test['labels'][i]
	#labels.append(label)
	canaux = jeu_test['canaux'][i]
	if h == 30:
		trois_canaux.append([[canaux[0] + canaux[1] + canaux[2]]])
	elif h == 20:
		trois_canaux.append([[canaux[0] + canaux[1]]])
	elif h == 10:
		trois_canaux.append([[canaux[0]]])
	else :
		raise Exeption("0 < tailleSequenceInputModele <= 3")	


trois_canaux = np.array(trois_canaux)
trois_canaux = trois_canaux.reshape(trois_canaux.shape[0], 1, h, 1)

trois_canaux = trois_canaux.astype('float32')

min = np.min(trois_canaux)
max = np.max(trois_canaux)

trois_canaux = (trois_canaux - min)/(max-min)
#print(trois_canaux[0])

for i in range(0, len(jeu_test['pixels'])):
	pixel = jeu_test['pixels'][i]
	label = jeu_test['labels'][i]
	date = jeu_test['dates'][i]
	canaux = jeu_test['canaux'][i]
	if label == 1 :
		test_vert[date].append(pixel) 
	else:
		test_rouge[date].append(pixel)

pred = modele.predict(np.array(trois_canaux))

index = 0
for p in pred:
	prediction = 0
	pixel = jeu_test['pixels'][index]
	date = jeu_test['dates'][index]
	index += 1
	if p[0] < p[1]:
		prediction = 1
	if prediction == 1:
		prediction_vert[date].append(pixel)
	else:
		prediction_rouge[date].append(pixel)
		

#pdf = PdfPages(path+"prediction.pdf")

for date in dates[2:]:
	plt.figure()#figsize=(150,100)
	plt.subplot(1,2,1)
	plt.title(date + " observations")
	plt.imshow(compute_ndvi(data["20160806"]),cmap="gray")

	if len(test_vert[date])>0:
		p = np.array(test_vert[date])
		plt.scatter(p[:,0],p[:,1],c='green')
	if len(test_rouge[date])>0:
		p = np.array(test_rouge[date])
		plt.scatter(p[:,0],p[:,1],c='red')
	
	plt.subplot(1,2,2)
	plt.title(date + " predictions")
	plt.imshow(compute_ndvi(data["20160806"]),cmap="gray")

	if len(prediction_vert[date])>0:
		p = np.array(prediction_vert[date])
		plt.scatter(p[:,0],p[:,1],c='green')
	if len(prediction_rouge[date])>0:
		p = np.array(prediction_rouge[date])
		plt.scatter(p[:,0],p[:,1],c='red')
	plt.show()
	#pdf.savefig()
#pdf.close()
