import random
from roles import *

class Game:
    def __init__(self, id_list: list,role_list:list,turn_count:int, player_list:list = None):
        self.id_list = id_list
        self.player_list = player_list
        self.role_list = role_list
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
            player = player_class(id = player_id, state = "alive")
            self.player_list.append(player)
            
    def turn(self):
        pass

    def end(self):
        pass



if __name__ == "__main__":
    id_list = [1, 2, 3, 4, 5]
    role_list = ["werewolf", "villager", "seer", "witch", "hunter"]

    game = Game(id_list, role_list, turn_count=10)
    game.start()

    # Accéder aux joueurs créés
    for player in game.player_list:
        print(f"Player {player.id} with role {player.role}")










