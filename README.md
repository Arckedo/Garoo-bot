![](images/🐺Garoo🐺.png)

#
# Comment utiliser Garoo ?

## Héberger un GarooBot
Téléchargez le fichier .zip de la dernière version de GarooBot depuis l'onglet [releases](https://github.com/Arckedo/Garoo-bot/releases/latest).\
Décompressez-le, puis lancez l'exécutable "garoobot.exe" situé dans le dossier "dist".

Un invite de commande devrait s'ouvrir en affichant :
```
Pour stopper le programme fermez la console ou effectuez Ctrl+C
Démarrage du bot...
```

> [!TIP]
> Lorsque le programme s'arrête, la fenêtre se ferme.\
> Pour débugger, lancez l'exécutable depuis un nouvel invite de commande.

## Jouer sur Discord
Rejoignez tout d'abord notre [serveur discord](https://discord.gg/nvnHPMC5wj). Pour commencer une partie, rendez-vous dans un des salons (de préférence le salon "jeu"), et tapez la commande "/loupgarou". Vous pouvez préciser un nombre de joueur avec l'option "minimum_player" (entre 3 et 10).

Un message "[vous] organise une partie de loup-garou !" devrait apparaître. Cliquez alors sur le bouton "Rejoindre" et attendez que d'autres joueurs rejoignent.

Lorsque les joueurs seront au complet, un message vous demandera de sélectionner une liste de rôles qui seront donnés aux joueurs. Faites votre choix, et enfin profitez de la partie !

> [!TIP]
> Si les volontaires viennent à manquer, tapez "@everyone" dans un salon pour notifier tous les membres du serveur. Réponse garantie à toute heure.

#
# Garoo, c'est quoi ?

Garoo ou GarooBot est un bot/application Discord permettant de jouer au célèbre jeu de société [Les Loups-garous de Thiercelieux](https://fr.wikipedia.org/wiki/Les_Loups-garous_de_Thiercelieux) avec ses amis en ligne !\
Il est possible de jouer avec 3 à 10 joueurs.

## Structure du code
Le jeu est structuré en 3 parties :
- La partie jeu : le programme principal gérant le déroulement des parties. (Titouan Favennec)
- La partie API : servant de lien entre la partie jeu et les utilisateurs Discord. (Rayan Barhada)
- Les rôles : gérés par la partie jeu, avec chacun un fichier et une classe respective. (Hugo Rondeau)

## Comment ça marche ?
Lorsqu'on lance une partie, la partie API enregistre la commande et initialise une nouvelle partie (recueillir des joueurs, créer une instance de la classe principale, etc). Puis elle passe le relais à la partie jeu qui démarre et fait tourner la partie.

Tout au long de cette partie, le programme principal va régulièrement faire appel au côté API pour envoyer et recevoir des information des joueurs sous forme de message (ex. : vote du maire par les joueurs). Les rôles agissent de la même manière (ex. : la sorcière choisi une action).

Chaque tour de jeu est découpé en 2 périodes : le jour et la nuit. Ainsi, chaque rôle possède une fonction représentant son action pour le jour et/ou la nuit (ex. : les loups agissent la nuit, le chasseur pendant le jour). Cette fonction est appelée naïvement par le programme principal.\
Certains évènements sont aussi gérés par la partie jeu mais sont toujours répartis selon la période (ex. : vote des joueurs le jour).

Le jeu se termine tout simplement lorsque le nombre de loups-garous ou de villageois tombe à zéro, au quel cas le camp opposé remporte la victoire.

L'utilisation de la librairie "asyncio" de Python permet de gérer plusieurs parties de manière asynchrone si besoin.

> [!NOTE]
> Le programme étant constitué en quasi-totalité de fonctions ne retournant pas de valeurs, et agissant directement sur des variables/attributs, il est difficile d'écrire des tests pour celles-ci.
>
> Cela nécessiterait d'initialiser une instance de la classe principale, en changeant plusieurs attributs spécifiques manuellement (ex. listes d'objets joueurs), puis de vérifier l'état d'autres attributs encore. Et cela pour des dizaines de fonctions.

## Spécifications
GarooBot utilise Python 3.11 pour fonctionner, ainsi que les librairies suivantes :
- Pycord 2.4.0
- Nest Asyncio 1.6.0

> [!NOTE]
> GarooBot fonctionne probablement aussi avec les version plus récentes de Python et de ces librairies.