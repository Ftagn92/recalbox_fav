# -*- coding: utf-8 -*-
"""
Created on Mon May 14 01:17:02 2018

@author: Sandro
"""

#Imports
import sys, os, shutil
import xml.etree.cElementTree as ET

def main():
    if len(sys.argv) < 3:
        '''
        Je vérifie la présence des paramètres obligatoires
        1. Répertoire des ROMS (chemin réseau accepté, exemple \\RECALBOX\SHARE\ROMS)
        2. Action
                backup : sauve les favoris en local
                restore : recrée chaque fichier gamelist (toujours en local) avec les favoris correctement flagués
        '''
        print("Usage: {} <path to ROMS directory> <backup/restore>".format(sys.argv[0]))
        exit()
    #Initialisation
    path_roms = sys.argv[1]
    action = sys.argv[2]
    if action == "backup":
        for chemin in os.listdir(path_roms):
            if os.path.isfile(path_roms+'/'+chemin)==False:
                if os.path.exists(path_roms+'/'+chemin+'/gamelist.xml')==True:
                    print(path_roms+'/'+chemin)
                    if os.path.exists('./'+chemin)==False:
                        os.mkdir('./'+chemin)
                    if os.path.exists('./'+chemin+'/favoris.txt')==True:
                        os.remove('./'+chemin+'/favoris.txt')
                    tree = ET.parse(path_roms+'/'+chemin+'/gamelist.xml')
                    racine = tree.getroot()
                    for jeu in racine:
                        fav_yes_no = ''
                        nom_jeu = ''
                        for element in jeu:
                            if element.tag == 'path':
                                nom_jeu = element.text
                            if element.tag == 'favorite':
                                fav_yes_no = element.text
                                if fav_yes_no == 'true':
                                    print('\t'+nom_jeu)
                                    with open('./'+chemin+"/favoris.txt", "a") as myfile:
                                        myfile.write(nom_jeu+'\n')
    if action == "restore":
        for chemin in os.listdir('.'):
                if os.path.isfile('./'+chemin)==False:
                    #C'est un répertoire
                    if os.path.exists('./'+chemin+'/favoris.txt')==True:
                        #On a des favoris sauvegardés
                        if os.path.exists(path_roms+'/'+chemin+'/gamelist.xml')==True:
                            if os.path.exists('./'+chemin+'/gamelist.xml')==True:
                                #On supprime un essai précédent s'il existe
                                os.remove('./'+chemin+'/gamelist.xml')
                            shutil.copyfile(path_roms+'/'+chemin+'/gamelist.xml', './'+chemin+'/gamelist.xml')
                            print('./'+chemin+'/gamelist.xml')
                            #Chargement des favoris sauvegardés
                            with open('./'+chemin+'/favoris.txt') as f:
                                favoris = f.readlines()
                            tree = ET.parse(path_roms+'/'+chemin+'/gamelist.xml')
                            racine = tree.getroot()
                            for jeu in racine:
                                bingo = False
                                nom_jeu = ''
                                for element in jeu:
                                    if element.tag == 'path':
                                        nom_jeu = element.text
                                        if (element.text+'\n') in favoris:
                                            #Le jeu est retenu
                                            bingo = True
                                if bingo == True:
                                    #Pour chaque jeu retenu
                                    bingo = False
                                    for element in jeu:
                                        if element.tag == 'favorite':
                                            #il y a déjà une section favorite
                                            bingo = True
                                            if element.text == 'false':
                                                print('\t'+nom_jeu+ ' : '+element.text+' -> true')
                                                #On l'update
                                                element.text = 'true'
                                            break
                                    if bingo == False:
                                        #Il n'y avait pas de section favorite, on la crée
                                        favori  = ET.SubElement(jeu,"favorite")
                                        favori.text = "true"
                                        print('\t'+nom_jeu+ ' : None -> true')
                            tree.write(open('./'+chemin+'/gamelist.xml', 'wb'))
                                                

if __name__ == "__main__":
    main()
