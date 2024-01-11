class Game:
    def __init__(self, player_list,role_list,turn_count):
        self.player_list = player_list
        self.role_list = role_list
        self.turn_count = turn_count

    def start(self):
        pass

    def turn(self):
        pass

    def end(self):
        pass



class _Player:
    def __init__(self, id, state):
        self.id = id
        self.state = state


class _Role(_Player):
    def __init__(self, id, state, role):
        super().__init__(id, state)
        self.role = role


class Werewolf(_Role):
    def __init__(self, id, state):
        super().__init__(id, state, role="werewolf")


class Villager(_Role):
    def __init__(self, id, state):
        super().__init__(id, state, role="villager")


class Seer(_Role):
    def __init__(self, id, state):
        super().__init__(id, state, role="seer")

class Witch(_Role):
    def __init__(self, id, state):
        super().__init__(id, state, role="witch")

class Hunter(_Role):
    def __init__(self, id, state):
        super().__init__(id, state, role="hunter")

class Thief(_Role):
    def __init__(self, id, state):
        super().__init__(id, state, role="thief")












