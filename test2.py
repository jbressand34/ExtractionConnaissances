# endoding : utf-8
import json
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import cmocean
file = open("../data_4_tp/data_parcelle.json")
data_parcels = json.load(file)
file.close()

parcelles = ["C57","C295","C310","C63","C58","C46",\
"C297","C289","C64","C51"]


#cmdict = cmocean.tools.get_dict(cmocean.cm.matter, N=len(parcelles))

file = open("../data_4_tp/data_matrix.json","r")
data = json.load(file)
file.close()
"""
r,g,b=np.array(cmdict["red"]),np.array(cmdict["green"]),np.array(cmdict["blue"])

cm=np.concatenate((r,g,b))
"""

colors = cm.rainbow(np.linspace(0,1,len(parcelles)))

def compute_ndvi(img):
    R=np.array(img[2])
    PIR=np.array(img[6])
    return(PIR-R)/(PIR+R)


i=0
parcel_test=np.array(list(data_parcels.values()))
plt.figure(figsize=(15,10))
plt.imshow(compute_ndvi(data["20160806"]),cmap="gray")

for p in parcelles:
    try:
        p=np.array(data_parcels[p])
        plt.scatter(p[:,0],p[:,1],c=colors[i])
    except:
        pass
    i+=1

plt.show()