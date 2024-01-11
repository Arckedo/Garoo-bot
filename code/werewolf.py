import random
import * from roles.py

class Game:
    def __init__(self, id_list: list,role_list:list,turn_count:int, player_list = None: list):
        self.id_list = id_list
        self.player_list = player_list
        self.role_list = role_list
        self.turn_count = turn_count

    def start(self):
        # Give a class and a Role to each player
        if player_list == None: 
            self.player_list = []
            shuff_id_list = random.shuffle(self.id_list)

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
            player = player_class(id = player_id, self)
            self.player_list.append(player)
            
    def turn(self):
        pass

    def end(self):
        pass














