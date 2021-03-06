# recalbox_fav
Sauvegarde et restauration des status favoris, hidden, playcount, lastplayed de toutes vos gamelists

Comme beaucoup d'entre vous, j'aime bien faire et défaire ma borne, tester des nouveaux "packs" et à chaque fois, je me tapais la sélection de mes favoris, notés précieusement sur un papier.

Donc voilà comment ça fonctionne :
Vous créez un répertoire temporaire sur votre pc, vous y mettez le programme

Puis vous tapez la commande :

python recalbox_fav.py \\recalbox\share\roms backup (suivie des paramètres de votre choix)

Il va vous créer un sous répertoire pour chacun des systèmes, et créer dedans s'il y a lieu de le faire, un fichier favoris.txt, lastplayed.txt, playcount.txt et hidden.txt avec les jeux que vous aviez sélectionné dans chaque gamelist

Ensuite vous bidouillez votre recalbox, rasez tout, etc, bref...

Pour restaurer vos favoris, vous lancez la commande :

python recalbox_fav.py \\recalbox\share\roms restore (suivie des paramètres de votre choix)

Par exemple pour les favoris :

Le programme lit chaque gamelist distante si vous avez un fichier favoris.txt en local, et compare les deux.
Ensuite il ajoute ou modifie la section <favorite> de chaque jeu qu'il retrouve, et que vous aviez mis en favoris dans la gamelist
Enfin il écrit la gamelist.xml résultat en local, dans le sous-répertoire concerné

Je précise en local parce que mon programme n'écrit rien sur le share, vous pouvez même le lancer sur une copie locale de votre carte SD ça marche aussi. Bref, c'est safe, je fais du readonly sur les listes

Ensuite il ne vous reste plus qu'à copier chaque gamelist.xml créée dans le répertoire correspondant de votre recalbox à la place de l'ancienne, et redémarrer emulationstation pour voir vos favoris chéris :)

Le programme peut faire la même chose avec  les playcount, les hidden, les lastplayed, tout ces status à la fois ou individuellement
Il suffit d'indiquer les sections à sauvegarder dans une chaine de caractère unique (syntaxe libre, je fais un parsing dans la chaîne)

Enfin vous devez indiquer si vous souhaitez ou non calculer le hash MD5 de chaque rom pour l'identifier, avec le paramètre hash ou nohash

Exemple :

python recalbox_fav.py \\recalbox\share\roms backup favorite_hidden_lastplayed_playcount hash

python recalbox_fav.py \\recalbox\share\roms backup lastplayedhiddenplaycount hash

python recalbox_fav.py \\recalbox\share\roms backup favoriteonsenfouhiddentralalalastplayed nohash

python recalbox_fav.py \\recalbox\share\roms restore favorite nohash

python recalbox_fav.py \\recalbox\share\roms backup hiddenOSEF hash

:p
Last but not least, vous pouvez ajouter à vos risques et péril le paramètre REMOTE (en majuscule) pour qu'il écrase REELLEMENT vos gamelists directement lors d'une restauration sur la recalbox

Exemple : 

python recalbox_fav.py \\recalbox\share\roms restore hidden hash REMOTE

Rassurez-vous vos gamelists sont juste renommées avec un timestamp avant d'être remplacées par les nouvelles, vous pourrez revenir en arrière indéfiniement

N'hésitez pas à me faire remonter bugs, suggestions ou corrections

Le programme a été testé sous Windows et sur la recalbox 4.1 (linux) avec les mêmes syntaxe

Exemple, sur la recalbox vous avez mis le script dans le SHARE dans un répertoire 'mon_backup'

cd /recalbox/share/mon_backup

python recalbox_fav.py ../roms backup lastplayed-hidden hash
