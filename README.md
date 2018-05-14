# recalbox_fav
Sauvegarde et restauration des status favoris, hidden, playcount, lastplayed de toutes vos gamelists

Comme beaucoup d'entre vous, j'aime bien faire et défaire ma borne, tester des nouveaux "packs" et à chaque fois, je me tapais la sélection de mes favoris, notés précieusement sur un papier.

Donc voilà comment ça fonctionne :
Vous créez un répertoire temporaire sur votre pc, vous y mettez le programme
Ensuite vous l'appelez avec la commande :

python recalbox_fav.py \\recalbox\share\roms backup

Il va vous créer un sous répertoire pour chacun des systèmes, et créer dedans un fichier favoris.txt avec les jeux que vous aviez sélectionné dans chaque gamelist

Ensuite vous bidouillez votre recalbox, rasez tout, etc, bref...

Pour restaurer vos favoris, vous lancez la commande :

python recalbox_fav.py \\recalbox\share\roms restore

Le programme lit chaque gamelist distante si vous avez un fichier favoris.txt en local, et compare les deux.
Ensuite il ajoute ou modifie la section <favorite> de chaque jeu qu'il retrouve, et que vous aviez mis en favoris dans la gamelist
Enfin il écrit la gamelist.xml résultat en local, dans le sous-répertoire concerné

Je précise en local parce que mon programme n'écrit rien sur le share, vous pouvez même le lancer sur une copie locale de votre carte SD ça marche aussi. Bref, c'est safe, je fais du readonly sur les listes

Ensuite il ne vous reste plus qu'à copier chaque gamelist.xml créée dans le répertoire correspondant de votre recalbox à la place de l'ancienne, et redémarrer emulationstation pour voir vos favoris chéris :)

Bientôt il fera pareil pour les playcount, les hidden, peut-être aussi les lastplayed, tout ces status à la fois ou individuellement
