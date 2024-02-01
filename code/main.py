import random
from role import *

class Game:
    def __init__(self, id_list: list, turn_count: int, start_role_list: list = None, role_list: list = None):
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
        self.list_killed_night = []
        self.list_not_killed_yet = id_list

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
            # INTERACTION À REMPLACER (Front)
            print("-----------------Nuit {}-------------------".format(self.turn_count))

            for role in self.role_list:
                if type(role) in night_action_list:
                    role.night_action(game=self)


        def day_turn(self):
            # INTERACTION À REMPLACER (Front)
            print("-----------------Jour {}-------------------".format(self.turn_count))
            
            for role in self.role_list:
                if type(role) in day_action_list:
                    role.day_action(game=self)
            
            def day_vote(self):
                # INTERACTION À REMPLACER (Front)



                print("Abat les loups: C'est l'heure de voter !")
                # Initialisation des variables pour le décompte des votes
                nb_voter = 0
                dic_vote = {}

                # Parcourt la liste des rôles pour permettre à chaque joueur vivant de voter
                for role in self.role_list:
                    for player in role.lst_player:
                        if player.is_alive:
                            
                            # Fonction interne pour mettre à jour le dictionnaire des votes
                            def vote_dic(i):
                                if vote in dic_vote:
                                    dic_vote[vote] += i
                                else:
                                    dic_vote[vote] = i

                            nb_voter += 1
                            # Interaction avec l'utilisateur pour obtenir le vote du joueur
                            vote = input(f"Qui veux-tu voter ? Joueur {player.id}\nRéponse:")
                            print(vote)

                            # Attribution du poids du vote en fonction du rôle du joueur (double vote pour le maire)
                            if player.is_mayor():
                                vote_dic(2)
                            else:
                                vote_dic(1)

                # Calcul du nombre total de votes           
                nb_vote = sum(dic_vote.values())

                victim_voted = False

                if nb_voter == nb_vote:
                    # Détermination du joueur sélectionné par le plus de votes
                    max_vote = max(dic_vote.values())
                    
                    index_max_vote = 0
                    for vote_value in dic_vote.values():
                        if vote_value == max_vote:
                            index_max_vote += 1
                        if index_max_vote > 1:
                            print("Egalité, au maire de départagé !")
                            return

                    for role in self.role_list:
                        for player in role.lst_player:
                            if player.is_alive:
                                # Attribution du statut de maire au joueur ayant reçu le plus de votes
                                if player.id in dic_vote.keys():
                                    if dic_vote[player.id] == max_vote:
                                        player.is_mayor = True
                                        victim_voted = True
                                        print("Le nouveau maire est : ", player.id)
                if victim_voted == False:
                    # Appel récursif pour effectuer un nouveau tour de vote si il y a eu un problème
                    mayor_vote(self)            
            day_vote(self)

        def mayor_vote(self):
            # INTERACTION À REMPLACER (Front)




            print("Élisez le nouveau maire !")
            # Initialisation des variables pour le décompte des votes
            nb_voter = 0
            dic_vote = {}
            # Parcourt la liste des rôles pour permettre à chaque joueur vivant de voter
            for role in self.role_list:
                for player in role.lst_player:
                    if player.is_alive:

                        # Fonction interne pour mettre à jour le dictionnaire des votes
                        def vote_dic(i):
                            if vote in dic_vote:
                                dic_vote[vote] += i
                            else:
                                dic_vote[vote] = i

                        nb_voter += 1
                        
                        # Interaction avec l'utilisateur pour obtenir le vote du joueur
                        vote = int(input(f"Qui veux-tu voter ? Joueur {player.id}\nRéponse:"))
                        print(vote)
                        
                        # Attribution du poids du vote
                        vote_dic(1)

            # Calcul du nombre total de votes            
            nb_vote = sum(dic_vote.values())
            
            mayor_voted = False

            # Vérification si tous les votants ont exprimé leur vote
            if nb_voter == nb_vote:
                # Détermination du joueur sélectionné par le plus de votes
                max_vote = max(dic_vote.values())
                
                index_max_vote = 0
                for vote_value in dic_vote.values():
                    if vote_value == max_vote:
                        index_max_vote += 1
                    if index_max_vote > 1:
                        print("Egalité ! On recommence !")
                        mayor_vote(self)
                        return

                for role in self.role_list:
                    for player in role.lst_player:
                        if player.is_alive:
                            # Attribution du statut de maire au joueur ayant reçu le plus de votes
                            if player.id in dic_vote.keys():
                                if dic_vote[player.id] == max_vote:
                                    player.is_mayor = True
                                    mayor_voted = True
                                    print("Le nouveau maire est : ", player.id)
            if mayor_voted == False:
                # Appel récursif pour effectuer un nouveau tour de vote si il y a eu un problème
                mayor_vote(self)


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















if __name__ == "__main__":
    id_list = [1, 2, 3, 4, 5]
    role_list = ["werewolf", "villager", "seer", "witch", "hunter"]

    game = Game(id_list, turn_count = 0,start_role_list = role_list)
