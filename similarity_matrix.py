# encoding : utf-8
import json
import numpy as np
import pandas as pd
import time
from matplotlib import colors
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages


def similarity_matrix(valeurs_levees, valeurs_non_levees, division):
	nbT = len(valeurs_levees)
	avancement = -1
	debut = time.time()
	encours = time.time()
	compteur = 0
	matrice_levees = [[0 for i in range(0,nbT)] for i in range(0,nbT)]

	for i in range(0,nbT):
		if int(100*compteur/nbT)>avancement:
			avancement = int(100*compteur/nbT)
			print(str(avancement)+"% "+str(time.time()-encours)+"s")
			encours = time.time()
		compteur += 1	
		x = valeurs_levees[i]
		for j in range(i,nbT):
			y = valeurs_levees[j]

			distance = x - y
			if distance < 0:
				distance = -distance 
			matrice_levees[i][j] = distance
			if j != i:
				matrice_levees[j][i] = distance

	matrice2_levees = []
	tailleChunk = int(nbT/division)
	reste = nbT % tailleChunk
	for i in range(0,division):
		for j in range(i,division):
			sum = 0
			nb = 0
			ideb = i*tailleChunk
			ifin = (i+1)*tailleChunk
			jdeb = j*tailleChunk
			jfin = (j+1)*tailleChunk
			for i2 in range(ideb,ifin):
				for j2 in range(jdeb,jfin):
					sum += matrice_levees[i2][j2]
					nb += 1
			moyenne = sum / nb
			matrice2_levees.append([i,j,moyenne])
			if j != i:
				matrice2_levees.append([j,i,moyenne])
		if reste > 0:
			sum = 0
			nb = 0
			ideb = i*tailleChunk
			ifin = (i+1)*tailleChunk
			jdeb = j*tailleChunk
			for i2 in range(ideb,ifin):
				for j2 in range(jdeb,jdeb+reste):
					sum += matrice_levees[i2][j2]
					nb += 1
			moyenne = sum / nb
			matrice2_levees.append([i,division,moyenne])
			matrice2_levees.append([division,i,moyenne])
	matrice_levees = np.array(matrice2_levees)


	"""
	NON LEVEES
	"""
	nbT = len(valeurs_non_levees)
	avancement = -1
	debut = time.time()
	encours = time.time()
	compteur = 0
	matrice_non_levees = [[0 for i in range(0,nbT)] for i in range(0,nbT)]

	for i in range(0,nbT):
		if int(100*compteur/nbT)>avancement:
			avancement = int(100*compteur/nbT)
			print(str(avancement)+"% "+str(time.time()-encours)+"s")
			encours = time.time()
		compteur += 1	
		x = valeurs_non_levees[i]
		for j in range(i,nbT):
			y = valeurs_non_levees[j]

			distance = x - y
			if distance < 0:
				distance = -distance 
			matrice_non_levees[i][j] = distance
			if j != i:
				matrice_non_levees[j][i] = distance

	matrice2_non_levees = []
	tailleChunk = int(nbT/division)
	reste = nbT % tailleChunk
	for i in range(0,division):
		for j in range(i,division):
			sum = 0
			nb = 0
			ideb = i*tailleChunk
			ifin = (i+1)*tailleChunk
			jdeb = j*tailleChunk
			jfin = (j+1)*tailleChunk
			for i2 in range(ideb,ifin):
				for j2 in range(jdeb,jfin):
					sum += matrice_non_levees[i2][j2]
					nb += 1
			moyenne = sum / nb
			matrice2_non_levees.append([i,j,moyenne])
			if j != i:
				matrice2_non_levees.append([j,i,moyenne])
		if reste > 0:
			sum = 0
			nb = 0
			ideb = i*tailleChunk
			ifin = (i+1)*tailleChunk
			jdeb = j*tailleChunk
			for i2 in range(ideb,ifin):
				for j2 in range(jdeb,jdeb+reste):
					sum += matrice_non_levees[i2][j2]
					nb += 1
			moyenne = sum / nb
			matrice2_non_levees.append([i,division,moyenne])
			matrice2_non_levees.append([division,i,moyenne])
	matrice_non_levees = np.array(matrice2_non_levees)

	"""
	"""

	norm_levees = colors.Normalize(vmin=np.min(matrice_levees[:,2]),vmax=np.max(matrice_levees[:,2]))
	norm_non_levees = colors.Normalize(vmin=np.min(matrice_non_levees[:,2]),vmax=np.max(matrice_non_levees[:,2]))
	cl = [(1,0,0),(1,1,0),(0,1,1),(0,0,1)]
	couleurs = colors.LinearSegmentedColormap.from_list("ma colormap", cl, N=10)

	#fig = plt.subplot(1,2,1)
	fig = plt.figure()
	#ax = fig.add_subplot(1,2,1)
	plt.scatter(matrice_levees[:,0],matrice_levees[:,1],c=matrice_levees[:,2],cmap=couleurs,norm=norm_levees)
	plt.title("Pixels levees")
	def onclick(event):
		numl = int(event.y)
		numc = int(event.x)
		valX = valeurs_levees[numc]
		valY = valeurs_levees[numl]
		print('valx='+ str(valX)+' valy=' + str(valY))

	cid = fig.canvas.mpl_connect('button_press_event', onclick)
	#plt.subplot(1,2,2)
	#ax = fig.add_subplot(1,2,2)
	fig = plt.figure()
	plt.scatter(matrice_non_levees[:,0],matrice_non_levees[:,1],c=matrice_non_levees[:,2],cmap=couleurs,norm=norm_non_levees)
	plt.title("Pixels non levees")
	def onclick(event):
		numl = int(event.y)
		numc = int(event.x)
		valX = valeurs_non_levees[numc]
		valY = valeurs_non_levees[numl]
		print('valx='+ str(valX)+' valy=' + str(valY))

	cid = fig.canvas.mpl_connect('button_press_event', onclick)
	#fig.show()
file = open("../data_4_tp/objets_splites_leves_trois_dates.json")
data_objets_leves = json.load(file)
file.close()

file = open("../data_4_tp/objets_splites_non_leves_trois_dates.json")
data_objets_non_leves = json.load(file)
file.close()

"""
Utilisation des motifs séquentiels :
30 temps -> Tij :image i signal j, (i,j) in [1,..,3]*[1,..,10]

Pour chaque temps on doit définir un ensemble de clusters Cij

Pour chaque cluster  Cij on doit créer les données Dij avec

Dij = ensemble des signaux j des images j 
"""

l1 = [json.loads(val) for key, val in data_objets_leves.items()]
l2 = [json.loads(val) for key, val in data_objets_non_leves.items()]
np_array_levees = [[],[],[]] # 3 * : * 10
np_array_non_levees = [[],[],[]]
for j in range(0,int(len(l1)/2)):
	tab = l1[j]
	for k in range(0,len(tab[0])):
		for i in range(0,3):
			np_array_levees[i].append(tab[i][k]) 
for j in range(0,int(len(l2)/2)):
	tab = l2[j]
	for k in range(0,len(tab[0])):
		for i in range(0,3):
			np_array_non_levees[i].append(tab[i][k]) 


np_array_levees = np.array(np_array_levees)
np_array_non_levees = np.array(np_array_non_levees)
#print(np_array.shape)

donnees_levees = [[] for i in range(0,30)]
donnees_non_levees = [[] for i in range(0,30)]
	
for i in range(0,len(np_array_levees[0])):
	for j in range(0,3):
		for k in range(0,10):
			donnees_levees[j*10+k].append(np_array_levees[j,i,k])

for i in range(0,len(np_array_non_levees[0])):
	for j in range(0,3):
		for k in range(0,10):
			donnees_non_levees[j*10+k].append(np_array_non_levees[j,i,k])

donnees_levees = np.array(donnees_levees) # 30 * nbPixel
donnees_non_levees = np.array(donnees_non_levees) # 30 * nbPixel


division = 100
pdf = PdfPages("../data_4_tp/signaux.pdf")

for i in range(0,30):
	plt.figure(figsize=(25,10))
	plt.title("Temps "+str(i))
	valeurs_levees = donnees_levees[i].tolist()
	valeurs_non_levees = donnees_non_levees[i].tolist()
	valeurs_levees.sort()
	valeurs_non_levees.sort()
	similarity_matrix(valeurs_levees, valeurs_non_levees,division)
	plt.show()
	#pdf.savefig()
	#plt.close()

pdf.close()
