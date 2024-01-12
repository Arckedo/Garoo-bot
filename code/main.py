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
        # Give a class and a Role to each player
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
            player = player_class(id = player_id, is_alive = "alive")
            self.player_list.append(player)




    def _turn(self):

        if self.turn_count == 0:
            print("-----------------Jour 0-------------------")
            print("Le jeu commence !")
            print("Elisez le nouveau maire !")


        self.turn_count += 1


        def night_turn(self):
            print("-----------------Nuit {}-------------------".format(self.turn_count))
            for player in self.player_list:
                if type(player) in night_action_list:
                    player.night_action()
            
        def dawn_turn(self):
            print("-----------------Aube {}-------------------".format(self.turn_count))
            for player in self.player_list:
                if type(player) in dawn_action_list:
                    player.dawn_action()

        def day_turn(self):
            print("-----------------Jour {}-------------------".format(self.turn_count))
            for player in self.player_list:
                if type(player) in day_action_list:
                    player.day_action()
            

        def twilight_turn(self):
            print("-----------------Crépuscule {}-------------------".format(self.turn_count))
            for player in self.player_list:
                if type(player) in twilight_action_list:
                    player.twilight_action()


        night_turn(self)
        dawn_turn(self)
        day_turn(self)
        twilight_turn(self)

    def end(self):
        pass



if __name__ == "__main__":
    id_list = [1, 2, 3, 4, 5]
    role_list = ["werewolf", "villager", "seer", "witch", "hunter"]

    game = Game(id_list, role_list, turn_count=0)
    game.start()

    for player in game.player_list:
        print(f"Player {player.id} with role {player.role}")
    
    game._turn()