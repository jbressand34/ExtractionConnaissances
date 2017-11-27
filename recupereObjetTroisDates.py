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

file = open("../data_4_tp/pixels_objets_splite.json", "r")
pixel_obj_splite = json.load(file)
file.close()

file_objet_leves = open("../data_4_tp/objets_leves.json", "r")
objets_leves = json.load(file_objet_leves).keys()
file_objet_leves.close()

file_objet_non_leves = open("../data_4_tp/objets_non_leves.json", "r")
objets_non_leves = json.load(file_objet_non_leves).keys()
file_objet_non_leves.close()

objets_levees = list(objets_leves)
objets_non_levees = list(objets_non_leves)

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

for obj in objets_levees:
	tab = obj.split(" ")
	date = tab[0]
	datePrev = getDatePrev(date)
	datePrevPrev = None
	if datePrev != None:
		datePrevPrev = getDatePrev(datePrev)
	matrice = []
	matrice_prev = []
	matrice_prev_prev = []
	for pixel in pixel_obj_splite[obj]:
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


for obj in objets_non_levees:
	tab = obj.split(" ")
	date = tab[0]
	datePrev = getDatePrev(date)
	datePrevPrev = None
	if datePrev != None:
		datePrevPrev = getDatePrev(datePrev)
	matrice = []
	matrice_prev = []
	matrice_prev_prev = []
	for pixel in pixel_obj_splite[obj]:
		signaux = []
		signaux_prev = []
		signaux_prev_prev = []
		for numsignal in range(0,10):
			signal = data[date][numsignal][pixel[0]][pixel[1]]
			signaux.append(signal)
			if datePrev != None :
				signal_prev = data[datePrev][numsignal][pixel[0]][pixel[1]]
				signaux_prev.append(signal_prev)
			else :
				signaux_prev.append(0)

			if datePrevPrev != None:
				signal_prev_prev = data[datePrevPrev][numsignal][pixel[0]][pixel[1]]
				signaux_prev_prev.append(signal_prev)
			else:
				signaux_prev_prev.append(0)
		matrice.append(signaux)
		matrice_prev.append(signaux_prev)
		matrice_prev_prev.append(signaux_prev_prev)
	m = []
	m.append(matrice)
	m.append(matrice_prev)
	m.append(matrice_prev_prev)	
	objets_non_levees_dump[obj] = pd.Series(m).to_json(orient='values')

file = open("../data_4_tp/objets_splites_leves_trois_dates.json","w")
json.dump(objets_levees_dump,file, indent=True)
file.close()
file = open("../data_4_tp/objets_splites_non_leves_trois_dates.json","w")
json.dump(objets_non_levees_dump,file, indent=True)
file.close()
