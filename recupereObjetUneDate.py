# encoding : utf-8
import json
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.cm as cm
from operator import itemgetter
import operator
import time

file = open("../data_4_tp/data_matrix.json","r")
data = json.load(file)
file.close()

file = open("../data_4_tp/pixel_objet_leve_splite.json", "r")
pixel_obj_leve_splite = json.load(file)
file.close()

file = open("../data_4_tp/pixel_objet_non_leve_splite.json", "r")
pixel_obj_non_leve_splite = json.load(file)
file.close()

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

objets_levees_dump = {}
objets_non_levees_dump = {}

for obj, pixels in pixel_obj_leve_splite.items():
	tab = obj.split(" ")
	date = tab[0]
	matrice = []
	for pixel in json.loads(pixels):
		signaux = []
		for numsignal in range(0,10):
			signal = data[date][numsignal][pixel[0]][pixel[1]]
			signaux.append(signal)
		matrice.append(signaux)
	m = []
	m.append(matrice)
	objets_levees_dump[obj] = pd.Series(m).to_json(orient='values')


for obj, pixels in pixel_obj_non_leve_splite.items():
	tab = obj.split(" ")
	date = tab[0]
	matrice = []
	for pixel in json.loads(pixels):
		signaux = []
		for numsignal in range(0,10):
			signal = data[date][numsignal][pixel[0]][pixel[1]]
			signaux.append(signal)
		matrice.append(signaux)
	m = []
	m.append(matrice)
	objets_non_levees_dump[obj] = pd.Series(m).to_json(orient='values')


pixels_leves = []
for objet, val1 in objets_levees_dump.items():
	tab = json.loads(val1)
	for i in range(0,len(tab[0])):
		t = []
		for j in range(0,1):
			for signal in tab[j][i]:
				t.append(signal)
		pixels_leves.append(t)

pixels_non_leves = []
for objet, val1 in objets_non_levees_dump.items():
	tab = json.loads(val1)
	for i in range(0,len(tab[0])):
		t = []
		for j in range(0,1):
			for signal in tab[j][i]:
				t.append(signal)
		pixels_non_leves.append(t)

print("Nombre de pixels leves : "+str(len(pixels_leves)))
print("Nombre de pixels non leves : "+str(len(pixels_non_leves)))

file = open("../data_4_tp/objets_splites_leves_une_date.json","w")
json.dump(objets_levees_dump,file, indent=True)
file.close()
file = open("../data_4_tp/objets_splites_non_leves_une_date.json","w")
json.dump(objets_non_levees_dump,file, indent=True)
file.close()
