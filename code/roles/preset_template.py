from role import _Player as Player
from typing import Optional


"""
Ce fichier est un example/modèle d'un préréglage de rôle (ici, la sorcière).

Lors de son lancement, le jeu va charger tous les préréglages présents dans le répertoire "roles".
Il reconnaîtra chacun d'eux à l'aide d'attributs normalisés (ex : "team" l'équipe du rôle).
Le préréglage peut avoir des attributs privés servant au fonctionnement interne du rôle (ex : "death_potions" le nombre de potions de mort en réserve).
Enfin, les méthodes normalisées permettent au jeu d'appeler le rôle lorsque c'est son tour (ex : "nighttime_behavior" les actions du rôle pendant la nuit).
"""


class RolePreset:
    def __init__(self) -> None:
        # Attributs dont les noms sont communs à toutes les classes
        # Nécéssaires pour que le jeu charge le rôle correctement
        self.name = "witch"
        self.team = "villagers"
        self.max_players = 1
        self.min_players = 0

        # Attributs spécifiques à cette classe
        # Ils servent au fonctionnement du rôle en lui-même
        self.__death_potions = 1
        self.__life_potions = 1


    def daytime_behavior(self):
        """La sorcière n'a pas de comportement spécial pendant la journée."""
        return


    def nighttime_behavior(self, player_list: list[Player], last_killed: Optional[Player]):
        """La nuit, la sorcière peut soit ressusciter le joueur venant d'être tué
        par les loup-garous, soit tuer un autre joueur, soit ne rien faire."""
        # Cette fonction est grandement simplifiée afin de servir d'exemple

        if last_killed and self.__life_potions > 0:
            # Demander si le joueur veut ressusciter
            last_killed.is_alive = True
            self.__life_potions -= 1

        elif self.__death_potions > 0:
            # Demander si le joueur veut tuer
            player_list[69].is_alive = False
            self.__death_potions -= 1