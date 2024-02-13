import os
import sys

# Obtien le chemin absolu du répertoire parent du répertoire actuel
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

# Ajoute le répertoire parent au chemin de recherche des modules
sys.path.append(parent_dir)

# Importe le module GarooVote relativement
from bot.interactions import GarooVote


class Player:
    def __init__(self, id):
        self.id = id
        self.is_alive = True
        self.is_mayor = False


class _Role:
    def __init__(self, lst_player : list):
        self.lst_player = lst_player

#region Roles

class Werewolf(_Role):
    def __init__(self, lst_player):
        super().__init__(lst_player)

    def night_action(self,game):
        #INTERACTION A REMPLACER (Front)
        lst_alive = game.alive_sort()
        

        stop = False
        while stop == False:
            interface = GarooVote(entries=lst_alive ,filter=[player.id for player in self.lst_player])
            dico_vote = game.client.send_interface("Place au vote des Loups AWOUUUUUU !",interface)
            print(dico_vote)
            
            #Renvoie la liste des clées de dico_vote dont la valeur est la plus grande
            max_keys = [key for key, value in dico_vote.items() if value == max(dico_vote.values())]
    
                
            if len(max_keys) == 1:
                for role in game.role_list:
                    for player in role.lst_player:
                        if game.find_mayor() != None and player.id == game.find_mayor().id:
                            player.is_mayor = False
                        if player.id == max_keys[0]:
                            player.is_alive = False 
                            stop = True
            else:
                game.client.send(f"Des joueurs ont eu le même nombre de vote ! LES LOUPS DOIVENT SE DECIDER !")
                self.night_action(game)
        #--------------------------

class Villager(_Role):
    def __init__(self, lst_player):
        super().__init__(lst_player)



class Seer(_Role):
    def __init__(self, lst_player):
        super().__init__(lst_player)

    
    def night_action(self,game = None):
        #INTERACTION A REMPLACER (Front)
        #--------------------------
        pass
        #--------------------------

class Witch(_Role):
    def __init__(self, lst_player):
        super().__init__(lst_player)

    
    def night_action(self,game = None):
        #INTERACTION A REMPLACER (Front)
        #--------------------------
        pass
        #--------------------------

class Hunter(_Role):
    def __init__(self, lst_player):
        super().__init__(lst_player)

        
    def day_action(self,game = None):
        #INTERACTION A REMPLACER (Front)
        #--------------------------
        pass
        #--------------------------

class Thief(_Role):
    def __init__(self, lst_player):
        super().__init__(lst_player)


    def night_action(self,game = None):
        #INTERACTION A REMPLACER (Front)
        pass
        #--------------------------

#endregion


night_action_list = [Werewolf, Seer, Witch, Thief]
day_action_list = [Hunter]

role_order = ["werewolf", "seer", "witch", "thief", "hunter", "villager"]

def role_order_sort(role):
    return role_order.index(role)