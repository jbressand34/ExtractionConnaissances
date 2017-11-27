# encoding : utf-8
import json
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import keras
from keras.layers import Dense, Flatten
from keras.layers import Conv2D, MaxPooling2D
from keras.models import Sequential

file = open("../data_4_tp/objets_splites_leves_trois_dates.json")
data_objets_leves = json.load(file)
file.close()

file = open("../data_4_tp/objets_splites_non_leves_trois_dates.json")
data_objets_non_leves = json.load(file)
file.close()

pixels_leves = []
for objet, val1 in data_objets_leves.items():
	tab = json.loads(val1)
	for i in range(0,len(tab[0])):
		t = []
		for j in range(0,3):
			for signal in tab[j][i]:
				t.append(signal)
		pixels_leves.append(t)

pixels_non_leves = []
for objet, val1 in data_objets_non_leves.items():
	tab = json.loads(val1)
	for i in range(0,len(tab[0])):
		t = []
		for j in range(0,3):
			for signal in tab[j][i]:
				t.append(signal)
		pixels_non_leves.append(t)

print("Nombre de pixels leves : "+str(len(pixels_leves)))
print("Nombre de pixels non leves : "+str(len(pixels_non_leves)))
x_train = [] #nbPixel * 10
x_test = []
y_train = []
y_test = []
h = 30

for i in range(0,int(len(pixels_leves)/2)):
	x_train.append(pixels_leves[2*i])
	x_test.append(pixels_leves[2*i+1])
	y_train.append(1)
	y_test.append(1)

for i in range(0,int(len(pixels_non_leves)/2)):
	x_train.append(pixels_non_leves[2*i])
	x_test.append(pixels_non_leves[2*i+1])
	y_train.append(0)
	y_test.append(0)

x_train = np.array(x_train)
x_test = np.array(x_test)
y_train = np.array(y_train)
y_test = np.array(y_test)

x_train = x_train.reshape(x_train.shape[0], 1, h, 1)
x_test = x_test.reshape(x_test.shape[0], 1, h, 1)
mon_shape = (1,h,1)

#print(x_train[0])

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

#print("min : "+str(min)+", max : "+str(max))

x_train = (x_train - min)/(max-min)
x_test = (x_test - min)/(max-min)

#print(x_train[0])

y_train = keras.utils.to_categorical(y_train, 2)
y_test = keras.utils.to_categorical(y_test, 2)

#print(y_train[0])

model = Sequential()

model.add(Conv2D(32,kernel_size=(1,2), activation='relu', input_shape=mon_shape, strides=(1,2)))
model.add(MaxPooling2D(pool_size=(1,2), strides=(1,1)))
model.add(Conv2D(64,kernel_size=(1,2), activation='relu', strides=(1,2)))
model.add(MaxPooling2D(pool_size=(1,2), strides=(1,1)))
model.add(Conv2D(64,kernel_size=(1,2), activation='relu', strides=(1,2)))
model.add(MaxPooling2D(pool_size=(1,2), strides=(1,1)))
model.add(Flatten())
model.add(Dense(1000, activation='relu'))
model.add(Dense(2, activation='softmax'))
#print(model.output_shape)

model.compile(loss=keras.losses.categorical_crossentropy,
	optimizer=keras.optimizers.Adam(),
	metrics=['accuracy'])

mon_batch_size = 128
epo=10

model.fit(x_train, y_train,
	batch_size=mon_batch_size,
	epochs=epo,
	verbose=1,
	validation_data=(x_test,y_test),
	shuffle=True)

#np.argsort(model.predict(np.array([x_train[0]])))

score = model.evaluate(x_test,y_test,verbose=0)
print("Score exactitude : "+str(score))