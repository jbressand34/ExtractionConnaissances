# encoding : utf-8
import os, sys, json
import os.path
import numpy as np

file_config = open("config.json", "r")
config = json.load(file_config)
file_config.close()
path = config["pathToDataDirectory"]

def pretraitement():
	os.system("python levees_parcelles.py")
	os.system("python pixel_objet_splite.py")
	os.system("python recupereObjetTroisDates.py")
	os.system("python separation_test_entrainement_trois_dates.py")


def modele():
	if os.path.isfile("path/performancesModele.txt"):
		os.system("rm path/performancesModele.txt")

	for i in range(0,3):
		os.system("python modelCNN.py")
	file = open("path/performancesModele.txt", "r")
	tabPrecisionE = []
	tabRappelE = []
	tabFmesureE = []

	tabPrecisionT = []
	tabRappelT = []
	tabFmesureT = []
	
	for line in file:
		tab = line.split(",")	
		precision = float(tab[1].split(":")[1])
		rappel = float(tab[2].split(":")[1])
		fmesure = float(tab[3].split(":")[1][:-1])
		if tab[0] == "Entrainement":
			tabPrecisionE.append(precision)
			tabRappelE.append(rappel)
			tabFmesureE.append(fmesure)
		elif tab[0] == "Test":
			tabPrecisionT.append(precision)
			tabRappelT.append(rappel)
			tabFmesureT.append(fmesure)
	file.close()

	file = open("path/performancesModele.txt", "a")
	moyPrecisionE = np.mean(np.array(tabPrecisionE))
	moyPrecisionT = np.mean(np.array(tabPrecisionT))
	moyRappelE = np.mean(np.array(tabRappelE))
	moyRappelT = np.mean(np.array(tabRappelT))
	moyFmesureE = np.mean(np.array(tabFmesureE))
	moyFmesureT = np.mean(np.array(tabFmesureT))

	resEntrainement = "Moyennes entrainement, precision:"+str(moyPrecisionE)+\
		", rappel:"+str(moyRappelE)+\
		", fmesure:"+str(moyFmesureE)+"\n"

	resTest = "Moyennes test, precision:"+str(moyPrecisionT)+\
		", rappel:"+str(moyRappelT)+\
		", fmesure:"+str(moyFmesureT)+"\n"

	file.write(resEntrainement + resTest)
	file.close()

if not config["pretraitementDejaFait"]:
	pretraitement()

modele()

if config["visualisationPrediction"]:
	os.system("python prediction.py")
