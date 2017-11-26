# encoding : utf-8
import json
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

file = open("../data_4_tp/objets_leves_deux_dates.json")
data_objets_leves = json.load(file)
file.close()

file = open("../data_4_tp/objets_non_leves_deux_dates.json")
data_objets_non_leves = json.load(file)
file.close()

delta_ndvi_pixels_leves = []
delta_ndvi_pixels_non_leves = []

vert_pixels_leves = []
vert_pixels_non_leves = []

rvi_pixels_leves = []
rvi_pixels_non_leves = []

nbIR = 7
nbR = 2

for obj, val in data_objets_leves.items():
	tab = json.loads(val)
	before = tab[1]
	levee = tab[0]
	for i in range(0,len(before)):
		signaux_pixel = levee[i]
		signaux_prev_pixel = before[i]
		ndvi = ((signaux_pixel[nbIR]-signaux_pixel[nbR])/\
		(signaux_pixel[nbIR]+signaux_pixel[nbR]))*100+100
		ndvi_prev = ((signaux_prev_pixel[nbIR]-signaux_prev_pixel[nbR])/\
		(signaux_prev_pixel[nbIR]+signaux_prev_pixel[nbR]))*100+100
		delta = int(ndvi-ndvi_prev)
		delta_ndvi_pixels_leves.append(delta)
		vert = (signaux_pixel[1]-signaux_prev_pixel[1])
		vert_pixels_leves.append(vert)
		rvi = signaux_pixel[6]/signaux_pixel[2]
		rvi_prev = signaux_prev_pixel[6]/signaux_prev_pixel[2]
		rvi_pixels_leves.append(rvi-rvi_prev)

for obj, val in data_objets_non_leves.items():
	tab = json.loads(val)
	before = tab[1]
	levee = tab[0]
	for i in range(0,len(before)):
		signaux_pixel = levee[i]
		signaux_prev_pixel = before[i]
		ndvi = ((signaux_pixel[nbIR]-signaux_pixel[nbR])/\
		(signaux_pixel[nbIR]+signaux_pixel[nbR]))*100+100
		ndvi_prev = ((signaux_prev_pixel[nbIR]-signaux_prev_pixel[nbR])/\
		(signaux_prev_pixel[nbIR]+signaux_prev_pixel[nbR]))*100+100
		delta = int(ndvi-ndvi_prev)
		delta_ndvi_pixels_non_leves.append(delta)
		vert = (signaux_pixel[1]-signaux_prev_pixel[1])
		vert_pixels_non_leves.append(vert)
		rvi = signaux_pixel[6]/signaux_pixel[2]
		rvi_prev = signaux_prev_pixel[6]/signaux_prev_pixel[2]
		rvi_pixels_non_leves.append(rvi-rvi_prev)


print(delta_ndvi_pixels_leves[:20])
print(delta_ndvi_pixels_non_leves[:20])

delta1 = np.array(delta_ndvi_pixels_leves)
delta2 = np.array(delta_ndvi_pixels_non_leves)

vert1 = np.array(vert_pixels_leves)
vert2 = np.array(vert_pixels_non_leves)

print("levee : "+str(np.mean(delta1)))
print("non levee : "+str(np.mean(delta2)))

print("\nVert:\n")

print(vert_pixels_leves[:20])
print(vert_pixels_non_leves[:20])

print("levee : "+str(np.mean(vert1)))
print("non levee : "+str(np.mean(vert2)))	

print("\nRVI:\n")

print(rvi_pixels_leves[:20])
print(rvi_pixels_non_leves[:20])

rvi1 = np.array(rvi_pixels_leves)
rvi2 = np.array(rvi_pixels_non_leves)
print("levee : "+str(np.mean(rvi1)))
print("non levee : "+str(np.mean(rvi2)))		