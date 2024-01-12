import random
from role import *

class Game:
    def __init__(self, id_list: list,role_list:list,turn_count:int, player_list:list = None):
        self.id_list = id_list
        self.player_list = player_list
        #Trier les roles pour les mettre dans l'ordre de passage
        self.role_list = sorted(role_list,key=role_order_sort) 
        self.turn_count = turn_count

    def start(self):
        # Donne une Class et un Role à chaque Joueur
        if self.player_list == None: 
            self.player_list = []
            shuff_id_list = list(self.id_list)
            random.shuffle(shuff_id_list)

            role_class = {
                "werewolf": Werewolf,
                "villager": Villager,
                "seer": Seer,
                "witch": Witch,
                "hunter": Hunter,
                "thief": Thief,
            }

        for player_id, role in zip(shuff_id_list, self.role_list):
            player_class = role_class[role]
            player = player_class(id = player_id, is_alive = True)
            self.player_list.append(player)

    def is_game_finish(self):
        werewolf_count = 0
        villager_count = 0

        for player in self.player_list:
            if player.is_alive:
                if player.side == "werewolf":
                    werewolf_count += 1
                elif player.side == "villager":
                    villager_count += 1
        #A voir si on garde ca ou si on termine quand tous les villageois sont mort
        #peut mettre les deux dont un qu'ils choissisent en features au pire
        if werewolf_count > villager_count:
            return "werewolf"
        elif werewolf_count == 0:
            return "villager"
        else:
            return None
    
    def end(self, winner):
        if winner == None:
            return False
        elif winner == "werewolf":
            #INTERACTION A REMPLACER (Front)
            #--------------------------
            print("La partie est terminé !")
            print("Les loups ont gagnés !")
            #--------------------------
            return True
        elif winner == "villager":
            #INTERACTION A REMPLACER (Front)
            #--------------------------
            print("La partie est terminé !")
            print("Les villageois ont gagnés !")
            #--------------------------
            return True



    def _turn(self):

        if self.end(self.is_game_finish()):
            return


        def night_turn(self):

            #INTERACTION A REMPLACER (Front)
            #--------------------------
            print("-----------------Nuit {}-------------------".format(self.turn_count))
            #--------------------------

            for player in self.player_list:
                if type(player) in night_action_list:
                    player.night_action()
            
        def dawn_turn(self):

            #INTERACTION A REMPLACER (Front)
            #--------------------------
            print("-----------------Aube {}-------------------".format(self.turn_count))
            print()
            #--------------------------

            for player in self.player_list:
                if type(player) in dawn_action_list:
                    player.dawn_action()

        def day_turn(self):

            #INTERACTION A REMPLACER (Front)
            #--------------------------
            print("-----------------Jour {}-------------------".format(self.turn_count))
            for player in self.player_list:
                if player.is_alive:
                    print(input(f"Qui veut tu voter ? joueur {player.id}\nRéponse:"))
            print()
            #--------------------------

        
            for player in self.player_list:
                if type(player) in day_action_list:
                    player.day_action()
            

        def twilight_turn(self):

            #INTERACTION A REMPLACER (Front)
            #--------------------------
            print("-----------------Crépuscule {}-------------------".format(self.turn_count))
            print()
            #--------------------------

            for player in self.player_list:
                if type(player) in twilight_action_list:
                    player.twilight_action()



        if self.turn_count == 0:

            #INTERACTION A REMPLACER (Front)
            #--------------------------
            print("-----------------Jour 0-------------------")
            print("Le jeu commence !")
            print("Elisez le nouveau maire !")
            #--------------------------
            
            twilight_turn(self)
        
        self.turn_count += 1


        night_turn(self)
        dawn_turn(self)
        day_turn(self)
        twilight_turn(self)

        self._turn()


if __name__ == "__main__":
    id_list = [1, 2, 3, 4, 5]
    role_list = ["werewolf", "villager", "seer", "witch", "hunter"]

    game = Game(id_list, role_list, turn_count=0)
    game.start()

    for player in game.player_list:
        print(f"Player {player.id} with role {player.role}")
    
    game._turn()