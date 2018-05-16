# -*- coding: utf-8 -*-
"""
Created on Mon May 14 01:17:02 2018

@author: Sandro
"""

#Imports
import sys, os, shutil, re
import xml.etree.cElementTree as ET
import hashlib
import datetime, time
def main():
    if len(sys.argv) < 5:
        '''
        Je vérifie la présence des paramètres obligatoires
        1. Répertoire des ROMS (chemin réseau accepté, exemple \\RECALBOX\SHARE\ROMS)
        2. Action
                backup : sauve les favoris en local
                restore : recrée chaque fichier gamelist (toujours en local) avec les favoris correctement flagués
        3. Liste des sections à sauvegarder / restaurer, en une seule chaîne, délimiteurs inutiles
                favorite
                hidden
                playcount
                lastplayed
                Exemple : hidden_playcount, favoritehidden, lastplayed___hidden___playcount_favorite, etc
        4. hash : Hashing des roms pour plus de sécurité / nohash : Pas de hashing (pratique pour des packs de roms dans d'autres langue ou de version différente)
        5. En local ou en REMOTE (écrase ou pas les gamelist de la recalbox). Par défaut en local
        '''
        print("Usage: {} <path to ROMS directory> <backup/restore> <section1_section2_etc> <hash/nohash>".format(sys.argv[0]))
        print("Example :  {} \\RECALBOX\SHARE\ROMS backup favorite_hidden_playcount_lastplayed hash".format(sys.argv[0]))
        print("Example :  {} \\RECALBOX\SHARE\ROMS restore favorite_hidden hash".format(sys.argv[0]))
        print("Example :  {} \\RECALBOX\SHARE\ROMS restore favorite nohash".format(sys.argv[0]))
        print("Add REMOTE to write gamelists to the recalbox (existing gamelists will be renamed and timestamped)")
        print("REMOTE is accepted only with restore action")
        print("Use REMOTE at your own risk.")
        exit()
    #Initialisation
    path_roms = sys.argv[1]
    action = sys.argv[2]
    sections = sys.argv[3]
    hashing = sys.argv[4]
    try:
        remote = sys.argv[5]
    except:
        remote = 'local'
    str_MD5 = ''
    if ((hashing.find('hash') == -1) and (hashing.find('nohash') == -1)):
        print("Wrong hashing parameter :  only accept hash or nohash")
        exit()
    #Quelles sections on traite ?
    backup_favorite = (sections.find('favorite') > -1)
    backup_hidden = (sections.find('hidden') > -1)
    backup_playcount = (sections.find('playcount') > -1)
    backup_lastplayed = (sections.find('lastplayed') > -1)
    if action == "backup":
        for chemin in os.listdir(path_roms):
            if os.path.isfile(path_roms+'/'+chemin)==False:
                if os.path.exists(path_roms+'/'+chemin+'/gamelist.xml')==True:
                    print(path_roms+'/'+chemin)
                    if os.path.exists('./'+chemin)==False:
                        os.mkdir('./'+chemin)
                    #favorite
                    if backup_favorite:
                        if os.path.exists('./'+chemin+'/favoris.txt')==True:
                            os.remove('./'+chemin+'/favoris.txt')
                    #hidden
                    if backup_hidden:
                        if os.path.exists('./'+chemin+'/hidden.txt')==True:
                            os.remove('./'+chemin+'/hidden.txt')
                    #playcount
                    if backup_playcount:
                        if os.path.exists('./'+chemin+'/playcount.txt')==True:
                            os.remove('./'+chemin+'/playcount.txt')
                    #lastplayed
                    if backup_lastplayed:
                        if os.path.exists('./'+chemin+'/lastplayed.txt')==True:
                            os.remove('./'+chemin+'/lastplayed.txt')                        
                    tree = ET.parse(path_roms+'/'+chemin+'/gamelist.xml')
                    racine = tree.getroot()
                    for jeu in racine:
                        fav_yes_no = ''
                        nom_jeu = ''
                        lastplayed = ''
                        playcount = ''
                        hidden = ''
                        MD5_OK = False
                        backup = False
                        for cherche_nom in jeu:
                            #Premier passage pour le nom
                            if cherche_nom.tag == 'path':
                                nom_jeu = cherche_nom.text
                        for element in jeu:
                            #2eme passage pour les données à sauvegarder
                            if backup_favorite == True:
                                if element.tag == 'favorite':
                                    fav_yes_no = element.text
                                    if fav_yes_no == 'true':
                                        print("- favorite")
                                        if MD5_OK == False:
                                            #On ne calcule le hash qu'une fois
                                            str_MD5 = calcul_MD5(path_roms+'/'+chemin+'/'+nom_jeu, hashing)
                                            MD5_OK = True
                                        with open('./'+chemin+"/favoris.txt", "a") as myfile:
                                            myfile.write(str_MD5+'\t'+nom_jeu+'\n')
                                        backup = True
                            if backup_hidden == True:
                                if element.tag == 'hidden':
                                    hidden = element.text
                                    if hidden == 'true':
                                        print("- hidden")
                                        if MD5_OK == False:
                                            #On ne calcule le hash qu'une fois
                                            str_MD5 = calcul_MD5(path_roms+'/'+chemin+'/'+nom_jeu, hashing)
                                            MD5_OK = True
                                        with open('./'+chemin+"/hidden.txt", "a") as myfile:
                                            myfile.write(str_MD5+'\t'+nom_jeu+'\n')
                                        backup = True
                            if backup_playcount == True:
                                if element.tag == 'playcount':
                                    playcount = element.text
                                    print("- playcount: "+str(playcount))
                                    if MD5_OK == False:
                                        #On ne calcule le hash qu'une fois
                                        str_MD5 = calcul_MD5(path_roms+'/'+chemin+'/'+nom_jeu, hashing)
                                        MD5_OK = True
                                    with open('./'+chemin+"/playcount.txt", "a") as myfile:
                                        myfile.write(str_MD5+'\t'+playcount+'\t'+nom_jeu+'\n')
                                    backup = True
                            if backup_lastplayed == True:
                                if element.tag == 'lastplayed':
                                    lastplayed = element.text
                                    print("- lastplayed: "+str(lastplayed))
                                    if MD5_OK == False:
                                        #On ne calcule le hash qu'une fois
                                        str_MD5 = calcul_MD5(path_roms+'/'+chemin+'/'+nom_jeu, hashing)
                                        MD5_OK = True
                                    with open('./'+chemin+"/lastplayed.txt", "a") as myfile:
                                        myfile.write(str_MD5+'\t'+lastplayed+'\t'+nom_jeu+'\n')
                                    backup = True
                        if backup == True:
                            print(str_MD5+'\t'+nom_jeu)
                            print('-'*32)
    if action == "restore":
        for chemin in os.listdir('.'):
                if os.path.isfile('./'+chemin)==False:
                    #C'est un répertoire de sauvegarde
                    if os.path.exists(path_roms+'/'+chemin+'/gamelist.xml')==True:
                        #On rapatrie la gamelist de la recalbox pour faire les modifs
                        if os.path.exists('./'+chemin+'/gamelist.xml')==True:
                            #On supprime un essai précédent s'il existe
                            os.remove('./'+chemin+'/gamelist.xml')
                        shutil.copyfile(path_roms+'/'+chemin+'/gamelist.xml', './'+chemin+'/gamelist.xml')
                        print('./'+chemin+'/gamelist.xml')
                        tree = ET.parse(path_roms+'/'+chemin+'/gamelist.xml')
                        racine = tree.getroot()
                        for jeu in racine:
                            restore = False
                            MD5_OK = False
                            nom_jeu = ''
                            for cherche_nom in jeu:
                                if cherche_nom.tag == 'path':
                                    nom_jeu = cherche_nom.text
                            #favorite
                            if backup_favorite:
                                if os.path.exists('./'+chemin+'/favoris.txt')==True:
                                    #On a des favoris sauvegardés
                                    with open('./'+chemin+'/favoris.txt') as f:
                                        favoris = f.readlines()
                                    bingo = False
                                    for ligne in favoris:   
                                        if ligne.find('\t'+nom_jeu+'\n') > -1:
                                            #Le jeu est retenu
                                            str_MD5 = calcul_MD5(path_roms+'/'+chemin+'/'+nom_jeu, hashing)
                                            MD5_OK = True
                                            if ligne == (str_MD5+'\t'+nom_jeu+'\n'):
                                                bingo = True
                                                break
                                    if bingo == True:
                                        #Pour chaque jeu retenu
                                        print("- favorite")
                                        restore = True
                                        restore_favorite = False
                                        for element in jeu:
                                            if element.tag == 'favorite':
                                                #il y a déjà une section favorite
                                                restore_favorite = True
                                                if element.text == 'false':
                                                    #On l'update
                                                    element.text = 'true'
                                                break
                                        if restore_favorite == False:
                                            #Il n'y avait pas de section favorite, on la crée
                                            favori  = ET.SubElement(jeu,"favorite")
                                            favori.text = "true"
                            #hidden
                            if backup_hidden:
                                if os.path.exists('./'+chemin+'/hidden.txt')==True:
                                    #On a des jeux cachés sauvegardés
                                    with open('./'+chemin+'/hidden.txt') as f:
                                        hidden = f.readlines()
                                    bingo = False
                                    for ligne in hidden:   
                                        if ligne.find('\t'+nom_jeu+'\n') > -1:
                                            #Le jeu est retenu
                                            str_MD5 = calcul_MD5(path_roms+'/'+chemin+'/'+nom_jeu, hashing)
                                            MD5_OK = True
                                            if ligne == (str_MD5+'\t'+nom_jeu+'\n'):
                                                bingo = True
                                                break
                                    if bingo == True:
                                        #Pour chaque jeu retenu
                                        print("- hidden")
                                        restore = True
                                        restore_hidden = False
                                        for element in jeu:
                                            if element.tag == 'hidden':
                                                #il y a déjà une section hidden
                                                restore_hidden = True
                                                if element.text == 'false':
                                                    #On l'update
                                                    element.text = 'true'
                                                break
                                        if restore_hidden == False:
                                            #Il n'y avait pas de section hidden, on la crée
                                            cache  = ET.SubElement(jeu,"hidden")
                                            cache.text = "true"
                            #playcount
                            if backup_playcount:
                                if os.path.exists('./'+chemin+'/playcount.txt')==True:
                                    #On a des compteurs sauvegardés
                                    with open('./'+chemin+'/playcount.txt') as f:
                                        playcount = f.readlines()
                                    bingo = False
                                    total = 0
                                    for ligne in playcount:   
                                        if ligne.find('\t'+nom_jeu+'\n') > -1:
                                            #Le jeu est retenu
                                            str_MD5 = calcul_MD5(path_roms+'/'+chemin+'/'+nom_jeu, hashing)
                                            MD5_OK = True
                                            if ligne[:32] == (str_MD5):
                                                liste = re.split(r'\t+', ligne)
                                                total = liste[1]
                                                print("- playcount : " + total)
                                                bingo = True
                                                break
                                    if bingo == True:
                                        #Pour chaque jeu retenu
                                        restore = True
                                        restore_playcount = False
                                        for element in jeu:
                                            if element.tag == 'playcount':
                                                #il y a déjà une section playcount
                                                restore_playcount = True
                                                #On l'update
                                                element.text = total
                                                break
                                        if restore_playcount == False:
                                            #Il n'y avait pas de section playcount, on la crée
                                            compte  = ET.SubElement(jeu,"playcount")
                                            compte.text = total
                            #lastplayed
                            if backup_lastplayed:
                                if os.path.exists('./'+chemin+'/lastplayed.txt')==True:
                                    #On a des timestamp sauvegardés
                                    with open('./'+chemin+'/lastplayed.txt') as f:
                                        lastplayed = f.readlines()
                                    bingo = False
                                    temps = 0
                                    for ligne in lastplayed:   
                                        if ligne.find('\t'+nom_jeu+'\n') > -1:
                                            #Le jeu est retenu
                                            str_MD5 = calcul_MD5(path_roms+'/'+chemin+'/'+nom_jeu, hashing)
                                            MD5_OK = True
                                            if ligne[:32] == (str_MD5):
                                                liste = re.split(r'\t+', ligne)
                                                temps = liste[1]
                                                print("- lastplayed : " + temps)
                                                bingo = True
                                                break
                                    if bingo == True:
                                        #Pour chaque jeu retenu
                                        restore = True
                                        restore_lastplayed = False
                                        for element in jeu:
                                            if element.tag == 'lastplayed':
                                                #il y a déjà une section lastplayed
                                                restore_lastplayed = True
                                                #On l'update
                                                element.text = temps
                                                break
                                        if restore_lastplayed == False:
                                            #Il n'y avait pas de section lastplayed, on la crée
                                            compte  = ET.SubElement(jeu,"lastplayed")
                                            compte.text = temps
                            if restore == True:
                                print(str_MD5+'\t'+nom_jeu)
                                print('-'*32)
                        tree.write(open('./'+chemin+'/gamelist.xml', 'wb'))
                        if remote == 'REMOTE':
                            ts = time.time()
                            st = datetime.datetime.fromtimestamp(ts).strftime('_%Y%m%d_%H%M%S_')
                            os.rename(path_roms+'/'+chemin+'/gamelist.xml',path_roms+'/'+chemin+'/gamelist_'+st+'.xml')
                            shutil.copyfile('./'+chemin+'/gamelist.xml', path_roms+'/'+chemin+'/gamelist.xml')
                            print('gamelist.xml -> '+ path_roms+'/'+chemin+'/gamelist.xml')
                                                
def calcul_MD5(chemin, hash_ou_pas):
    BUF_SIZE = 65536
    if hash_ou_pas == 'hash': 
        try:
            md5 = hashlib.md5()
            with open(chemin, 'rb') as f:
                while True:
                    data = f.read(BUF_SIZE)
                    if not data:
                        break
                    md5.update(data)
            MD5_final = md5.hexdigest()
        except:
            print('ROM absente : '+ chemin)
            MD5_final = '00000000000000000000000000000000'
    else:
        MD5_final = '00000000000000000000000000000000'
    return MD5_final

if __name__ == "__main__":
    main()
