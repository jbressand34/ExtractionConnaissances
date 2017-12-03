# encoding : utf-8
import json
import numpy as np
import random

file_config = open("config.json", "r")
config = json.load(file_config)
file_config.close()
path = config["pathToDataDirectory"]

file = open("path/pixel_objet_leve_splite.json", "r")
objets_leves_pixels = json.load(file)
file.close()

file = open("path/pixel_objet_non_leve_splite.json", "r")
objets_non_leves_pixels = json.load(file)
file.close()


file = open("path/objets_splites_leves_trois_dates.json","r")
objets_leves_canaux = json.load(file)
file.close()
file = open("path/objets_splites_non_leves_trois_dates.json","r")
objets_non_leves_canaux = json.load(file)
file.close()


objets_leves = list(objets_leves_pixels.keys())
objets_non_leves = list(objets_non_leves_pixels.keys())

"""
Le but est de creer deux fichiers :
-jeu_entrainement_trois_dates.json
- jeu_test_trois_dates.json

Structure des fichiers :
{
	"pixels": [pixel1,pixel2,...],
	"labels": [1,0,0,1,1,...],
	"dates" : ["20161102", ...]
	"canaux": [
		[[canal1,...,canal10],[canal1,...,canal10],[canal1,...,canal10]],
		[[...],[...],[...]],
		...
	]
}
"""

jeu_entrainement = {
	"pixels": [],
	"labels": [],
	"dates": [],
	"canaux": []
}

jeu_test = {
	"pixels": [],
	"labels": [],
	"dates": [],
	"canaux": []
}

shuffle_entrainement = []
shuffle_test = []

for objet in objets_leves:
	pixels = json.loads(objets_leves_pixels[objet])
	canaux = json.loads(objets_leves_canaux[objet])

	taille = len(pixels)
	if taille != len(canaux[0]):
		print("Nombre de pixels : "+str(taille))
		print("Nombre de canaux : "+str(len(canaux[0])))
		raise
	for i in range(0,taille):
		date = objet.split(" ")[0]

		shuffle_sample = (pixels[i],1,[canaux[0][i],canaux[1][i],canaux[2][i]], date)
		if i % 2 == 0:
			shuffle_entrainement.append(shuffle_sample)
		else:
			shuffle_test.append(shuffle_sample)

for objet in objets_non_leves:
	if objet in list(objets_non_leves_canaux.keys()):	
		pixels = json.loads(objets_non_leves_pixels[objet])
		canaux = json.loads(objets_non_leves_canaux[objet])
		date = objet.split(" ")[0]

		taille = len(pixels)
		if taille != len(canaux[0]):
			print("Nombre de pixels : "+str(taille))
			print("Nombre de canaux : "+str(len(canaux[0])))
			raise
		for i in range(0,taille):
			shuffle_sample = (pixels[i],0,[canaux[0][i],canaux[1][i],canaux[2][i]], date)
			if i % 2 == 0:
				shuffle_entrainement.append(shuffle_sample)
			else:
				shuffle_test.append(shuffle_sample)

random.shuffle(shuffle_entrainement)
random.shuffle(shuffle_test)


for shuffle_sample in shuffle_entrainement:
	pixel = shuffle_sample[0]
	label = shuffle_sample[1]
	canaux = shuffle_sample[2]
	date = shuffle_sample[3]
	jeu_entrainement["pixels"].append(pixel)
	jeu_entrainement["labels"].append(label)
	jeu_entrainement["canaux"].append(canaux)
	jeu_entrainement["dates"].append(date)

for shuffle_sample in shuffle_test:
	pixel = shuffle_sample[0]
	label = shuffle_sample[1]
	canaux = shuffle_sample[2]
	date = shuffle_sample[3]
	jeu_test["pixels"].append(pixel)
	jeu_test["labels"].append(label)
	jeu_test["canaux"].append(canaux)
	jeu_test["dates"].append(date)


file = open("path/jeu_entrainement_trois_dates.json","w")
json.dump(jeu_entrainement,file)
file.close()

file = open("path/jeu_test_trois_dates.json","w")
json.dump(jeu_test,file)
file.close()