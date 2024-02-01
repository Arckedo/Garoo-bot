
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
        kill = print(str(input("C'est au tour du werewolf\nQui veut tu tuer se soir ?\nRéponse : ")))
        print()
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
        print(input("C'est au tour du Seer\nQui veut tu regarder se soir ?\nRéponse : "))
        print()
        #--------------------------

class Witch(_Role):
    def __init__(self, lst_player):
        super().__init__(lst_player)

    
    def night_action(self,game = None):
        #INTERACTION A REMPLACER (Front)
        #--------------------------
        print(input("C'est au tour de la witch\nVeut tu utiliser tes potions se soir ?\nRéponse : "))
        print()
        #--------------------------

class Hunter(_Role):
    def __init__(self, lst_player):
        super().__init__(lst_player)

        
    def day_action(self,game = None):
        #INTERACTION A REMPLACER (Front)
        #--------------------------
        print(input("C'est au tour du Hunter\nQui veut tu viser se matin ?\nRéponse : "))
        print()
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