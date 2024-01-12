import random
from role import *

class Game:
    def __init__(self, id_list: list,role_list:list,turn_count:int, player_list:list = None):
        self.id_list = id_list
        self.player_list = player_list
        self.role_list = sorted(role_list,key=role_order_sort) #Trier les roles pour les mettre dans l'ordre
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




    def turn(self):
        self.turn_count += 1

        def night_turn(self):
            for player in self.player_list:
                if player in night_action_list:
                    player.action_night()
            
        def dawn_turn(self):
            for player in self.player_list:
                if player in dawn_action_list:
                    player.action_dawn()

        def day_turn(self):
            for player in self.player_list:
                if player in day_action_list:
                    player.action_day()

        def twilight_turn(self):
            for player in self.player_list:
                if player in twilight_action_list:
                    player.action_twilight()

    def end(self):
        pass



if __name__ == "__main__":
    id_list = [1, 2, 3, 4, 5]
    role_list = ["werewolf", "villager", "seer", "witch", "hunter"]

    game = Game(id_list, role_list, turn_count=10)
    game.start()

    for player in game.player_list:
        print(f"Player {player.id} with role {player.role}")









