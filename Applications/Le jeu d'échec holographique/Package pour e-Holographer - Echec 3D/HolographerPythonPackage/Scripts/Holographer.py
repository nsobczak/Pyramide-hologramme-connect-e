﻿#################################################
### Package Holographer pour le e-Holographer ###
#################################################

#%%_______________________________________________________________________________________________
import Constellation
import FusionImagesCreationPlateau as FICP
import ScriptRpi as SR
import os

# Initialisation variables globales
listeDesPieces = []	
IdProcI = 0 
cheminScriptVideo = "/home/pi/Desktop/scriptsRpi/bash/scriptVideo"
cheminScriptImage = "/home/pi/Desktop/scriptsRpi/bash/scriptImage"
cheminIdImage = "/home/pi/Desktop/scriptsRpi/bash/IdImage"
cheminIdVideo = "/home/pi/Desktop/scriptsRpi/bash/IdVideo"

#%%______________________________________________________________________________
#===== Message Callbacks =====

#Connexion démarrée
@Constellation.MessageCallback()
def InfosConnection():
	"Bouton qui écrit 'connecté' dans la console log"

	Constellation.WriteInfo("Holographer connecté à Constellation")


#En cours de jeu
@Constellation.MessageCallback()
def MAJPlateau(caseDeDepart, caseDarrivee):
	"Bouton qui génère le plateau suivant à partir de 2 integer - mettre 0, 0 pour générer le plateau initial"
	
	global IdProcI
	
	Constellation.WriteInfo( "MAJ du plateau lancee | [case de depart = " + str(caseDeDepart) + " | case d'arrivee = " + str(caseDarrivee) + "]" )

	global listeDesPieces 
	global cheminIdImage
        global cheminScriptImage

	if ((caseDeDepart == 0) and (caseDarrivee == 0)):
		#Creation du plateau de départ quand on est en cours de jeu
		Constellation.WriteInfo( "Initialisation du plateau" )
		listeDesPieces = FICP.creePlateauHolographique(nomImage, [], 0, 0)
		
		#Fermeture d'une eventuelle image
		if (IdProcI): 
			os.system( "kill " + str(IdProcI) )

		#Affichage de l'image
		IdProcI = SR.showImage(cheminScriptImage)

		Constellation.WriteInfo("Génération du plateau terminée")

	else:
		#Mise A Jour (MAJ) de la position des pieces sur le plateau
		listeDesPieces = FICP.creePlateauHolographique(nomImage, listeDesPieces, caseDeDepart, caseDarrivee)

		#Fermeture d'une eventuelle image
		if (IdProcI):
			os.system( "kill " + str(IdProcI) )

		#Affichage de l'image
		IdProcI = SR.showImage(cheminScriptImage)
		
		Constellation.WriteInfo("Maj plateau terminée")



#A utiliser quand on aura cree des animations pour les combats entre les différentes pièces
@Constellation.MessageCallback()
def AnimationCombat():
	"Bouton qui lance une animation de combat"

	Constellation.WriteInfo("Animation de combat lancée")



#Fin du jeu
@Constellation.MessageCallback()
def FinDuJeu():
	"Bouton qui signale la fin du jeu"

	Constellation.WriteWarn("Game Over")



#===== State Object =====

#Lancé au démarrage du package
def OnStart():
	#State Object
	Constellation.PushStateObject("Holographer", { "Sender": "Holographer" }, "Info", { "Device_Id": "RPi", "Etat du package":"lancé" })



#%%____________________________________________________________________________________
#Démarrage du package

Constellation.Start(OnStart);
