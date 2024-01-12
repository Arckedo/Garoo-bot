
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


class Villager(_Role):
    def __init__(self, id, is_alive):
        super().__init__(id, is_alive, role="villager")


class Seer(_Role):
    def __init__(self, id, is_alive):
        super().__init__(id, is_alive, role="seer")
    
    def night_action():
        pass

class Witch(_Role):
    def __init__(self, id, is_alive):
        super().__init__(id, is_alive, role="witch")

class Hunter(_Role):
    def __init__(self, id, is_alive):
        super().__init__(id, is_alive, role="hunter")

class Thief(_Role):
    def __init__(self, id, is_alive):
        super().__init__(id, is_alive, role="thief")

#endregion


night_action_list = [Werewolf, Seer, Witch, Thief]
dawn_action_list = [Hunter]
day_action_list = []
twilight_action_list = []

role_order = ["werewolf", "seer", "witch", "hunter", "thief", "hunter", "villager"]

def role_order_sort(role):
    return role_order.index(role)