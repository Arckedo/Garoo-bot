import random
from role import *
from bot.interactions import GarooClient
from bot.interactions import GarooVote
from messages import GarooMessages


class Game:
    def __init__(self,client: GarooClient, id_list: list, turn_count: int, start_role_list: list = None, role_list: list = None):
        """
        Initialise la partie avec les paramètres fournis.

        Args:
            id_list (list): Liste des identifiants des joueurs.
            turn_count (int): Compteur de tours.
            role_list (list, optional): Liste des rôles, dont le premier argument est booléen
        """

        assert(start_role_list != None or role_list != None)



        self.id_list = id_list
        self.turn_count = turn_count

        # Si la role_list n'est pas encore définie, trie les rôles pour les mettre dans l'ordre de passage
        if role_list is None:
            start_role_list = sorted(start_role_list, key=role_order_sort)
            self.start(start_role_list)
        else:
            # Ce coté ne fonctionne pas pour l'instant, si l'on veut reprendre une partie
            self.role_list = role_list
            self._turn()

    def start(self, start_role_list):
        """
        Démarre la partie en attribuant un rôle à chaque joueur.

        Args:
            start_role_list (list): Liste des rôles à attribuer à chaque joueur.
        """

        self.role_list = []
        # Mélange les id des joueurs
        shuff_id_list = list(self.id_list)
        random.shuffle(shuff_id_list)

        dict_role_class = {
            "werewolf": Werewolf,
            "villager": Villager,
            "seer": Seer,
            "witch": Witch,
            "hunter": Hunter,
            "thief": Thief,
            }
        
        # Parcourt les listes de joueurs et de rôles simultanément
        for player_id, str_role in zip(shuff_id_list, start_role_list):
            
            # Récupère la classe de rôle correspondante au nom de rôle
            role_class = dict_role_class[str_role]

            # Vérifie si la classe de rôle n'est pas déjà dans la liste de rôles
            if role_class not in role_list :
                # Crée un nouveau rôle avec un joueur et l'ajoute à la liste de rôles
                role = role_class([Player(id=player_id)] )
                self.role_list.append(role)
            else:
                # Si la classe de rôle est déjà présente, ajoute un nouveau joueur au rôle existant
                for role in role_list:
                    if role_class == type(role):
                        role.player_list.append(Player(id=player_id, is_alive=True))
        
        #Commence le premier tour
        self._turn()



    def _turn(self):
        """
        Effectue un tour de jeu.
        """
        
        # Vérifie si la condition de fin de jeu est atteinte
        #if self.end(self.is_game_finish()):
        #    return

        def night_turn(self):
            
            self.client.send(GarooMessages.nightfall())
            
            for role in self.role_list:
                if type(role) in night_action_list:
                    role.night_action(game=self)


        def day_turn(self):
            
            self.client.send(GarooMessages.daystart())
            
            for role in self.role_list:
                if type(role) in day_action_list:
                    role.day_action(game=self)
            
            def day_vote(self):
                # INTERACTION À REMPLACER (Front)
                lst_alive = self.alive_sort()
                mayor = self.mayor()
                interface = GarooVote(entries=lst_alive ,filter=lst_alive , weight={mayor.id : 2})
                dico_vote = self.client.send_interface("Place au vote des villageois !\n ABAT LES LOUPS !",interface)

            # Appel de la fonction de vote
            day_vote(self)

        def mayor_vote(self):
            # INTERACTION À REMPLACER (Front)
            lst_alive = self.alive_sort()
            interface = GarooVote(entries=lst_alive ,filter=lst_alive)
            dico_vote = self.client.send_interface("Place au vote du Maire !",interface)

        if self.turn_count == 0:
            # INTERACTION À REMPLACER (Front)
            print("-----------------Jour 0-------------------")
            print("Le jeu commence !")
            mayor_vote(self)

        self.turn_count += 1

        night_turn(self)
        day_turn(self)

        self._turn()

    def is_game_finish(self):
        """
        Vérifie si la partie est terminée et renvoie le vainqueur.

        Returns:
            str: "werewolf" si les loups ont gagné, "villager" si les villageois ont gagné, sinon None.
        """
        werewolf_count = 0
        villager_count = 0

        for player in self.player_list:
            if player.is_alive:
                if player.side == "werewolf":
                    werewolf_count += 1
                elif player.side == "villager":
                    villager_count += 1

        if werewolf_count > villager_count:
            return "werewolf"
        elif werewolf_count == 0:
            return "villager"
        else:
            return None

    def end(self, winner):
        """
        Termine la partie en affichant le vainqueur.

        Args:
            winner (str): Le vainqueur de la partie.

        Returns:
            bool: True si la partie est terminée, False sinon.
        """
        if winner is None:
            return False
        elif winner == "werewolf":
            # INTERACTION À REMPLACER (Front)
            print("La partie est terminée !")
            print("Les loups ont gagné !")
            return True
        elif winner == "villager":
            # INTERACTION À REMPLACER (Front)
            print("La partie est terminée !")
            print("Les villageois ont gagné !")
            return True

    #fonction d'utilité
    def alive_sort(self):
        lst = []
        for role in self.role_list:
            for player in role.lst_player:
                if player.is_alive == True:
                    lst.append(player.id)
        return lst

    def mayor(self):
        for role in self.role_list:
            for player in role.lst_player:
                if player.is_mayor == True:
                    return player





if __name__ == "__main__":
    id_list = [1, 2, 3, 4, 5]
    role_list = ["werewolf", "villager", "seer", "witch", "hunter"]

    game = Game(id_list, turn_count=0,start_role_list= role_list)
