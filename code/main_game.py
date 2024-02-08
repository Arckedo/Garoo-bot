import random
from roles import *
from bot.interactions import GarooClient
from bot.interactions import GarooVote



class Game:
    def __init__(self, client: GarooClient, id_list: list, start_role_list:list, turn_count:int, role_list:list = None):
        """
        Initialise la partie avec les paramètres fournis.

        Args:
            client (GarooClient): Client Discord utilisable par le jeu.
            id_list (list): Liste des identifiants des joueurs.
            turn_count (int): Compteur de tours.
            role_list (list, optional): Liste des rôles, dont le premier argument est booléen
        """

        assert(start_role_list != None or role_list != None)


        self.client = client
        self.id_list = id_list
        self.turn_count = turn_count

        # Si la role_list n'est pas encore définie, trie les rôles pour les mettre dans l'ordre de passage
        if role_list is None:
            start_role_list = sorted(start_role_list, key=role_order_sort)
            self.start(start_role_list)
        else:
            # Ce coté ne fonctionne pas pour l'instant, si l'on veut reprendre une partie
            self.role_list = role_list
        
        self.alive_notif = self.alive_sort()

        print(self.dic_role_sort())


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
            if role_class not in self.role_list :
                # Crée un nouveau rôle avec un joueur et l'ajoute à la liste de rôles
                role = role_class([Player(id=player_id)] )
                self.role_list.append(role)
            else:
                # Si la classe de rôle est déjà présente, ajoute un nouveau joueur au rôle existant
                for role in self.role_list:
                    if role_class == type(role):
                        role.player_list.append(Player(id=player_id, is_alive=True))
        


    def _turn(self):
        """
        Effectue un tour de jeu.
        """
        
        # Vérifie si la condition de fin de jeu est atteinte
        end , winner = self.end()
        if end:
            self.client.send("La partie est finie.")
            self.client.send(winner)
            return

        def night_turn(self):
            
            self.client.send("La nuit tombe sur Thiercelieux... \nNuit : " + str(self.turn_count))
            
            for role in self.role_list:
                if type(role) in night_action_list:
                    role.night_action(game=self)


        def day_turn(self):
            
            self.client.send("Le jour se lève sur Thiercelieux...\nJour : " + str(self.turn_count))
            
            death, resur = self.alive_notification()
            self.client.send(f"Les joueurs suivant sont morts cette nuit : {death} \n Les joueurs suivant ont été ressucités cette nuit : {resur}")

            if self.find_mayor() is None:
                self.client.send(f"Le Maire est Mort !")
                mayor_vote(self)
            for role in self.role_list:
                if type(role) in day_action_list:
                    role.day_action(game=self)
            
            def day_vote(self):
                # INTERACTION À REMPLACER (Front)
                lst_alive = self.alive_sort()
                mayor = self.find_mayor()

                stop = False
                while stop == False:
                    interface = GarooVote(entries=lst_alive ,filter=lst_alive , weight={mayor.id : 2})
                    dico_vote = self.client.send_interface("Place au vote des villageois !\n ABAT LES LOUPS !",interface)
                    print(dico_vote)
                    
                    #Renvoie la liste des clées de dico_vote dont la valeur est la plus grande
                    max_keys = [key for key, value in dico_vote.items() if value == max(dico_vote.values())]
        
                    
                    if len(max_keys) == 1:
                        for role in self.role_list:
                            for player in role.lst_player:
                                if player.id == max_keys[0]:
                                    player.is_alive = False
                                    self.alive_notification()
                                    self.client.send(f"{player.id} est brulée sur la place de thercelieux!")
                                    self.client.send(f"Son role était {role} !")
                                    if player.id == mayor.id:
                                        player.is_mayor = False
                                        self.client.send(f"Le Maire est mort !")
                                        mayor_vote(self)
                                    stop = True 
                    else:
                        self.client.send(f"Les joueurs suivants ont eu le même nombre de vote : {max_keys} !\nIl n'y aura aucun mort lors de se vote.")
            # Appel de la fonction de vote
            day_vote(self)

        def mayor_vote(self):
            # INTERACTION À REMPLACER (Front)
            lst_alive = self.alive_sort()
            

            stop = False
            while stop == False:
                interface = GarooVote(entries=lst_alive ,filter=lst_alive)
                dico_vote = self.client.send_interface("Place au vote du Maire !",interface)
                print(dico_vote)
                
                #Renvoie la liste des clées de dico_vote dont la valeur est la plus grande
                max_keys = [key for key, value in dico_vote.items() if value == max(dico_vote.values())]
    
                
                if len(max_keys) == 1:
                    for role in self.role_list:
                        for player in role.lst_player:
                            if player.id == max_keys[0]:
                                player.is_mayor = True
                                self.client.send(f"Le Maire est {player.id} !")
                                stop = True
                else:
                    self.client.send(f"Les joueurs suivants ont eu le même nombre de vote : {max_keys} !")
                            
        

        if self.turn_count == 0:
            # INTERACTION À REMPLACER (Front)
            mayor_vote(self)

        self.turn_count += 1

        night_turn(self)
        day_turn(self)
        self._turn()


    def end(self):
        wolf = 0
        villager = 0
        for role in self.role_list:
            for player in role.lst_player:
                if player.is_alive == True:
                    if type(role) == Werewolf:
                        wolf += 1
                    else :
                        villager += 1
        if wolf == 0 and villager == 0:
            return True, "**Les Arbres de la forets**, les Loups-Garous et les Villageois sont tous morts !"
        elif wolf == 0:
            return True, "Les Loups-Garous sont tous morts, **Les villageois ont gagné !**"
        elif villager == 0:
            return True, "Les Villageois sont tous morts, **Les Loups-Garous ont gagné !**"
        else:
            return False, None



    def alive_sort(self):
        lst = []
        for role in self.role_list:
            for player in role.lst_player:
                if player.is_alive == True:
                    lst.append(player.id)
        return lst

    def find_mayor(self):
        for role in self.role_list:
            for player in role.lst_player:
                if player.is_mayor == True:
                    return player
    
    def dic_role_sort(self):
        dic = {}
        for role in self.role_list:
            for player in role.lst_player:
                dic[player.id] = str(role)
        return dic

    def alive_notification(self):
        death = []
        resur = []

        for role in self.role_list:
            for player in role.lst_player:
                if player.is_alive == False and player.id in self.alive_notif:
                    death.append(player.id)
                if player.is_alive == True and player.id not in self.alive_notif:
                    resur.append(player.id)
        self.alive_notif = self.alive_sort()
        return death, resur            
                          
"""
if __name__ == "__main__":
    id_list = [1, 2, 3, 4, 5]
    role_list = ["werewolf", "villager", "seer", "witch", "hunter"]

    game = Game(id_list, role_list, turn_count=0)
    game.start()

    for player in game.player_list:
        print(f"Player {player.id} with role {player.role}")

    game._turn()"""