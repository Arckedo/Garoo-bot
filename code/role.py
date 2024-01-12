
class _Player:
    def __init__(self, id, is_alive):
        self.id = id
        self.is_alive = is_alive


class _Role(_Player):
    def __init__(self, id, is_alive, role):
        super().__init__(id, is_alive)
        self.role = role


#region Roles

class Werewolf(_Role):
    def __init__(self, id, is_alive):
        super().__init__(id, is_alive, role="werewolf")

    def night_action(self):
        print("C'est au tour du werewolf\nQui veut tu tuer se soir ?")
        print()

class Villager(_Role):
    def __init__(self, id, is_alive):
        super().__init__(id, is_alive, role="villager")


class Seer(_Role):
    def __init__(self, id, is_alive):
        super().__init__(id, is_alive, role="seer")
    
    def night_action(self):
        print("C'est au tour du Seer\nQui veut tu regarder se soir ?")
        print()

class Witch(_Role):
    def __init__(self, id, is_alive):
        super().__init__(id, is_alive, role="witch")
    
    def night_action(self):
        print("C'est au tour de la witch\nVeut tu utiliser tes potions se soir ?")
        print()

class Hunter(_Role):
    def __init__(self, id, is_alive):
        super().__init__(id, is_alive, role="hunter")
        
    def dawn_action(self):
        print("C'est au tour du Hunter\nQui veut tu viser se matin ?")
        print()

class Thief(_Role):
    def __init__(self, id, is_alive):
        super().__init__(id, is_alive, role="thief")

    def night_action(self):
        print("C'est au tour du Thief\nA qui veut tu voler une carte ?")
        print()

#endregion


night_action_list = [Werewolf, Seer, Witch, Thief]
dawn_action_list = [Hunter]
day_action_list = []
twilight_action_list = []

role_order = ["werewolf", "seer", "witch", "thief", "hunter", "villager"]

def role_order_sort(role):
    return role_order.index(role)