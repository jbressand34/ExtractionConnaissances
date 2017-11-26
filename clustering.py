# encoding : utf-8
import json
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
#import keras
from sklearn.cluster import KMeans, MiniBatchKMeans, AgglomerativeClustering
from sklearn.metrics.pairwise import pairwise_distances_argmin


file = open("../data_4_tp/objets_leves.json")
data_objets_leves = json.load(file)
file.close()

file = open("../data_4_tp/objets_non_leves.json")
data_objets_non_leves = json.load(file)
file.close()

objets = {}
X = []
labels_true = []

for obj, val in data_objets_leves.items():
	liste_pixel = json.loads(val)
	liste_signaux = [0 for i in range(0,10)]
	nbPixel = len(liste_pixel)
	if nbPixel > 0:
		for pixel in liste_pixel:
			for i in range(0,10):
				liste_signaux[i]+=pixel[i]
		liste_signaux = np.array(liste_signaux)
		liste_signaux = liste_signaux//nbPixel
		objets.update({obj:liste_signaux})
		X.append(liste_signaux.tolist())
		labels_true.append(1)

for obj, val in data_objets_non_leves.items():
	liste_pixel = json.loads(val)
	liste_signaux = [0 for i in range(0,10)]
	nbPixel = len(liste_pixel)
	if nbPixel > 0:
		for pixel in liste_pixel:
			for i in range(0,10):
				liste_signaux[i]+=pixel[i]
		liste_signaux = np.array(liste_signaux)
		liste_signaux = liste_signaux//nbPixel
		objets.update({obj:liste_signaux})
		X.append(liste_signaux.tolist())
		labels_true.append(0)

"""
for key in objets:
	print(objets[key])
	break
"""

#print(len(X))
X = np.array(X)
#print(X.shape)

#k_means = MiniBatchKMeans(init='k-means++', n_clusters=2,batch_size=45,verbose=1)
k_means = AgglomerativeClustering(n_clusters=2, linkage="ward")
k_means.fit(X)

#k_means_cluster_centers = k_means.cluster_centers_
#labels = pairwise_distances_argmin(X,k_means_cluster_centers)
labels = k_means.labels_
print(labels_true)

print(labels)

tp =0
tn = 0
fp = 0
fn = 0



for i in range(0,len(labels_true)):
	if labels_true[i] == 1:
		if labels[i] == 1:
			tp += 1
		else:
			fn += 1
	else:
		if labels[i] == 0:
			tn += 1
		else:
			fp += 1

precision = tp/(tp+fp)
rappel = tp/(tp+fn)

print("tp : "+str(tp)+", tn : "+str(tn))
print("fp : "+str(fp)+", fn : "+str(fn))
print("precision : "+str(precision))
print("rappel : "+str(rappel))