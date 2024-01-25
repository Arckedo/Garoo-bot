
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
        player_choosen = int(input("Choisissez le joueur que vous voullez tuer parmi les suivants %r : " %game.id_list))
        for role in game.role_list:
            for player in role.lst_player:
                if player.is_alive and not player in self.lst_player:
                    print("Envoi l'interface choix du villageois à tuer !") 
                    game.list_killed_night.append(player_choosen)
                    game.list_not_killed_yet.remove(player_choosen)
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
        for role in game.role_list:
            for player in role.lst_player:
                if player.is_alive:
                    print("Envoi l'interface choix du joueur que la voyante veux voir")
                    select_player = True
                    if select_player:
                        print(role)
        #--------------------------

class Witch(_Role):
    def __init__(self, lst_player):
        super().__init__(lst_player)
        self.life_potion = 1
        self.death_potion = 1

    
    def night_action(self,game = None):
        #INTERACTION A REMPLACER (Front)
        #--------------------------
        print("Envoi de l'interface pour choisir quellle action faire")
        if self.life_potion == 1 and game.list_killed_night != []:
            print("Envoi de l'interface pour choisir quel joueur la sorcière veut-elle ressuciter")
        if self.death_potion == 1:
            for role in game.role_list:
                for player in role.lst_player:
                    if player.is_alive:
                        print("Envoi de l'interface pour choisir quel joueur la sorcière veut-elle tuer")

        #--------------------------

class Hunter(_Role):
    def __init__(self, lst_player):
        super().__init__(lst_player)

        
    def day_action(self,game = None):
        #INTERACTION A REMPLACER (Front)
        #--------------------------
        for player in self.lst_player:
            if player.id in game.list_killed_night:
                print("Envoi de l'interface pour choisir enver quel joueur le chasseur veut se venger")


        #--------------------------

class Thief(_Role):
    def __init__(self, lst_player):
        super().__init__(lst_player)


    def night_action(self,game = None):
        #INTERACTION A REMPLACER (Front)
        print(input("C'est au tour du Thief\nA qui veut tu voler une carte ?\nRéponse : "))
        print()
        #--------------------------

#endregion


night_action_list = [Werewolf, Seer, Witch, Thief]
day_action_list = [Hunter]

role_order = ["werewolf", "seer", "witch", "thief", "hunter", "villager"]

def role_order_sort(role):
    return role_order.index(role)