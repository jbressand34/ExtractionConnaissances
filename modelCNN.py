# encoding : utf-8
import json
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import keras
from keras.layers import Dense, Flatten
from keras.layers import Conv2D, MaxPooling2D
from keras.models import Sequential
from keras import backend as K
from sklearn.metrics import precision_score, recall_score, f1_score 
import sys
	
file = open("../data_4_tp/jeu_entrainement_trois_dates.json","r")
jeu_entrainement = json.load(file)
file.close()

file = open("../data_4_tp/jeu_test_trois_dates.json","r")
jeu_test = json.load(file)
file.close()

file_config = open("config.json", "r")
config = json.load(file_config)
file_config.close()

x_train = [] #nbPixel * 10
x_test = []
y_train = []
y_test = []

h = 10 * int(config["tailleSequenceInputModele"])
if h > 30:
	raise Exeption("0 < tailleSequenceInputModele <= 3")


for i in range(0, len(jeu_entrainement['labels'])):
	label = jeu_entrainement['labels'][i]
	y_train.append(label)
	canaux = jeu_entrainement['canaux'][i]
	if h == 30:
		x_train.append(canaux[0] + canaux[1] + canaux[2])
	elif h == 20:
		x_train.append(canaux[0] + canaux[1])
	elif h == 10:
		x_train.append(canaux[0])
	else :
		raise Exeption("0 < tailleSequenceInputModele <= 3")	



for i in range(0, len(jeu_test['labels'])):
	label = jeu_test['labels'][i]
	y_test.append(label)
	canaux = jeu_test['canaux'][i]
	if h == 30:
		x_test.append(canaux[0] + canaux[1] + canaux[2])
	elif h == 20:
		x_test.append(canaux[0] + canaux[1])
	elif h == 10:
		x_test.append(canaux[0])
	else :
		raise Exeption("0 < tailleSequenceInputModele <= 3")	


x_train = np.array(x_train)
x_test = np.array(x_test)
y_train = np.array(y_train)
y_test = np.array(y_test)

x_train = x_train.reshape(x_train.shape[0], 1, h, 1)
x_test = x_test.reshape(x_test.shape[0], 1, h, 1)
mon_shape = (1,h,1)

x_train = x_train.astype('float32')
x_test = x_test.astype('float32')

min1 = np.min(x_train)
min2 = np.min(x_test)
min = min1
if min2 < min1:
	min = min2

max1 = np.max(x_train)
max2 = np.max(x_test)
max = max1
if max2 > max1:
	max = max2

x_train = (x_train - min)/(max-min)
x_test = (x_test - min)/(max-min)


y_train = keras.utils.to_categorical(y_train, 2)
y_test = keras.utils.to_categorical(y_test, 2)

model = Sequential()

model.add(Conv2D(32,kernel_size=(1,2), activation='relu', input_shape=mon_shape, strides=(1,2)))
model.add(MaxPooling2D(pool_size=(1,2), strides=(1,1)))
for i in range(1, config["nombreCouches"]):
	model.add(Conv2D(64,kernel_size=(1,2), activation='relu', strides=(1,2)))
	model.add(MaxPooling2D(pool_size=(1,2), strides=(1,1)))
model.add(Flatten())
model.add(Dense(config["nombreNoeudFullyConnected"], activation='relu'))
model.add(Dense(2, activation='softmax'))
#print(model.output_shape)


model.compile(loss=keras.losses.categorical_crossentropy,
	optimizer=keras.optimizers.Adam(),
	metrics=['accuracy'])#decay=0.001

mon_batch_size = 128
epo=config["nombreEpoquesEntrainement"]

model.fit(x_train, y_train,
	batch_size=mon_batch_size,
	epochs=epo,
	verbose=1,
	validation_data=(x_test,y_test),
	shuffle=True)

nbPixelsLevees = 0
nbPixelsNonLevees = 0

predictions_train = model.predict(x_train)
predictions_test = model.predict(x_test)
#Nombre de pixels leves : 1119 non leves : 1104

for pred in predictions_train:
	prediction = 0

	if pred[1]>pred[0]:
		prediction = 1		
	if prediction == 1:
		nbPixelsLevees += 1
	elif prediction == 0:
		nbPixelsNonLevees += 1
for pred in predictions_test:
	prediction = 0

	if pred[1]>pred[0]:
		prediction = 1		
	if prediction == 1:
		nbPixelsLevees += 1
	elif prediction == 0:
		nbPixelsNonLevees += 1

print("Prediction total : "+str(nbPixelsLevees)+" levees, "+\
	str(nbPixelsNonLevees)+" non levees.")
"""		
for i in range(0,10):
	pr = np.argsort(model.predict(np.array([x_train[i]])))
	print(pr)
"""
score = model.evaluate(x_test,y_test,verbose=0)
model.save_weights('../data_4_tp/modele_poids.h5')
fmodel = open("../data_4_tp/modele.json", "w")
fmodel.write(model.to_json())
fmodel.close()

print("Score exactitude : "+str(score))
print("Nombre d'echantillons d'entrainement : "+str(len(x_train.tolist())))
print("Nombre d'echantillons de test : "+str(len(x_test.tolist())))

y_train_pred = model.predict(x_train)
y_train_prediction = [0 if val[0]>val[1] else 1 for val in y_train_pred]

y_test_pred = model.predict(x_test)
y_test_prediction = [0 if val[0]>val[1] else 1 for val in y_test_pred]

y_train_true = [0 if val[0]>val[1] else 1 for val in y_train]
y_test_true = [0 if val[0]>val[1] else 1 for val in y_test]

precision_train = precision_score(y_train_true, \
	y_train_prediction,pos_label=1,average='binary')
precision_test = precision_score(y_test_true, \
	y_test_prediction,pos_label=1,average='binary')

recall_train = recall_score(y_train_true, \
	y_train_prediction,pos_label=1,average='binary')
recall_test = recall_score(y_test_true, \
	y_test_prediction,pos_label=1,average='binary')

f1_train = f1_score(y_train_true, \
	y_train_prediction,pos_label=1,average='binary')
f1_test = f1_score(y_test_true, \
	y_test_prediction,pos_label=1,average='binary')

print("Entrainement, precision:"+str(precision_train)+\
	", rappel:"+str(recall_train)+\
	", fmesure:"+str(f1_train))

resEntrainement = "Entrainement, precision:"+str(precision_train)+\
	", rappel:"+str(recall_train)+\
	", fmesure:"+str(f1_train) + "\n"

resTest = "Test, precision:"+str(precision_test)+\
	", rappel:"+str(recall_test)+\
	", fmesure:"+str(f1_test)+"\n"


print("Test, precision:"+str(precision_test)+\
	", rappel:"+str(recall_test)+\
	", fmesure:"+str(f1_test))

file = open("../data_4_tp/performancesModele.txt","a")
file.write(resEntrainement + resTest)