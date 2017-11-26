# encoding : utf-8
import json
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.cm as cm
from operator import itemgetter
import operator
import time

matrices = {}

file = open("../data_4_tp/data_matrix.json","r")
data = json.load(file)
file.close()

for key in data:
    matrice = np.array(data[key])
    #print(matrice.shape)
    matrices.update({ key : matrice})
file.close()

file = open("../data_4_tp/pixels_objets_splite.json")
objets = json.load(file)
file.close()

file_objet_leves = open("../data_4_tp/objets_leves.json", "r")
objets_leves = json.load(file_objet_leves).keys()
file_objet_leves.close()

file_objet_non_leves = open("../data_4_tp/objets_non_leves.json", "r")
objets_non_leves = json.load(file_objet_non_leves).keys()
file_objet_non_leves.close()

objets_leves = list(objets_leves)
objets_non_leves = list(objets_non_leves)

objets_levees_dump = {}
objets_non_levees_dump = {}

for obj_l in objets_leves:
    signaux = []
    date = obj_l.split(" ")[0]
    for p in objets[obj_l]:
        signaux_pixels = []
        for i in range(0, 10):
            signal = data[date][i][p[0]][p[1]]
            signaux_pixels.append(signal)
        signaux.append(signaux_pixels)
    signaux = pd.Series(signaux).to_json(orient='values')
    objets_levees_dump.update({obj_l : signaux })    

for obj_l in objets_non_leves:
    signaux = []
    date = obj_l.split(" ")[0]
    for p in objets[obj_l]:
        signaux_pixels = []
        for i in range(0, 10):
            signal = data[date][i][p[0]][p[1]]
            signaux_pixels.append(signal)
        signaux.append(signaux_pixels)
    signaux = pd.Series(signaux).to_json(orient='values')    
    objets_non_levees_dump.update({obj_l : signaux })    


#print(objets_levees_dump)
file = open("../data_4_tp/objets_leves_splites.json","w")
json.dump(objets_levees_dump,file)
file.close()
file = open("../data_4_tp/objets_non_leves_splites.json","w")
json.dump(objets_non_levees_dump,file)
file.close()
