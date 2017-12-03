# encoding : utf-8
import json
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.cm as cm
from operator import itemgetter
import operator
import time

#print("\nCréation de deux fichiers json qui contiennent les objets splités levés et non levés pour trois dates.")

file_config = open("config.json", "r")
config = json.load(file_config)
file_config.close()
path = config["pathToDataDirectory"]

file = open(path+"data_matrix.json","r")
data = json.load(file)
file.close()

file = open(path+"pixel_objet_leve_splite.json", "r")
pixel_obj_leve_splite = json.load(file)
file.close()

file = open(path+"pixel_objet_non_leve_splite.json", "r")
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
	datePrev = getDatePrev(date)
	datePrevPrev = None
	if datePrev != None:
		datePrevPrev = getDatePrev(datePrev)
	matrice = []
	matrice_prev = []
	matrice_prev_prev = []
	for pixel in json.loads(pixels):
		signaux = []
		signaux_prev = []
		signaux_prev_prev = []
		for numsignal in range(0,10):
			signal = data[date][numsignal][pixel[0]][pixel[1]]
			signaux.append(signal)
			if datePrev != None and datePrevPrev != None:
				signal_prev = data[datePrev][numsignal][pixel[0]][pixel[1]]
				signaux_prev.append(signal_prev)
				signal_prev_prev = data[datePrevPrev][numsignal][pixel[0]][pixel[1]]
				signaux_prev_prev.append(signal_prev)
			else:
				print(datePrev)
				raise Exception()
		matrice.append(signaux)
		matrice_prev.append(signaux_prev)
		matrice_prev_prev.append(signaux_prev_prev)
	m = []
	m.append(matrice)
	m.append(matrice_prev)
	m.append(matrice_prev_prev)	
	objets_levees_dump[obj] = pd.Series(m).to_json(orient='values')


for obj, pixels in pixel_obj_non_leve_splite.items():
	tab = obj.split(" ")
	date = tab[0]
	datePrev = getDatePrev(date)
	datePrevPrev = None
	if datePrev != None:
		datePrevPrev = getDatePrev(datePrev)
	matrice = []
	matrice_prev = []
	matrice_prev_prev = []
	for pixel in json.loads(pixels):
		signaux = []
		signaux_prev = []
		signaux_prev_prev = []
		for numsignal in range(0,10):
			signal = data[date][numsignal][pixel[0]][pixel[1]]
			signaux.append(signal)
			if datePrev != None and datePrevPrev != None:
				signal_prev = data[datePrev][numsignal][pixel[0]][pixel[1]]
				signaux_prev.append(signal_prev)
				signal_prev_prev = data[datePrevPrev][numsignal][pixel[0]][pixel[1]]
				signaux_prev_prev.append(signal_prev)
		matrice.append(signaux)
		matrice_prev.append(signaux_prev)
		matrice_prev_prev.append(signaux_prev_prev)
	if len(signaux_prev)>0 and len(signaux_prev_prev)>0:
		m = []
		m.append(matrice)
		m.append(matrice_prev)
		m.append(matrice_prev_prev)	
		objets_non_levees_dump[obj] = pd.Series(m).to_json(orient='values')


pixels_leves = []
for objet, val1 in objets_levees_dump.items():
	tab = json.loads(val1)
	for i in range(0,len(tab[0])):
		t = []
		for j in range(0,3):
			for signal in tab[j][i]:
				t.append(signal)
		pixels_leves.append(t)

pixels_non_leves = []
for objet, val1 in objets_non_levees_dump.items():
	tab = json.loads(val1)
	for i in range(0,len(tab[0])):
		t = []
		for j in range(0,3):
			for signal in tab[j][i]:
				t.append(signal)
		pixels_non_leves.append(t)
"""
print("Nombre de pixels leves : "+str(len(pixels_leves)))
print("Nombre de pixels non leves : "+str(len(pixels_non_leves)))
"""
file = open(path+"objets_splites_leves_trois_dates.json","w")
json.dump(objets_levees_dump,file, indent=True)
file.close()
file = open(path+"objets_splites_non_leves_trois_dates.json","w")
json.dump(objets_non_levees_dump,file, indent=True)
file.close()
