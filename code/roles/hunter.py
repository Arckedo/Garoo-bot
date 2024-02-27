from roles.role import Role
from bot.interactions import GarooVote


class Hunter(Role):
    def __init__(self, lst_player):
        super().__init__(
            lst_player,
            image_link="https://th.bing.com/th/id/OIG1.NRxdBY8IRZ_5GTtIsfHH?pid=ImgGn",
            description="Le Chasseur, toujours en embuscade, riposte avec sa flèche mortelle dès qu'il est attaqué par les Loups-Garous. Sa mort est une revanche : il choisit une cible à emporter avec lui dans la tombe, bouleversant le cours du jeu.",
        )

    def day_action(self, game):
        if self.lst_player[0].is_alive == True:
            return

        lst_alive = game.alive_sort()

        interface = GarooVote(
            entries=game.entries(lst_alive),
            filter=[player.id for player in self.lst_player],
        )
        dico_vote = self.send_embed_role_interface(
            game,
            interface=interface,
            title="🏹 __Chasseur__ 🏹",
            description="Tu as été tué.e ! Il est temps de te venger !!!",
        )

        max_keys = [
            key for key, value in dico_vote.items() if value == max(dico_vote.values())
        ]

        for role in game.role_list:
            for player in role.lst_player:
                if player.id == max_keys[0]:
                    player.is_alive = False

    def __str__(self) -> str:
        return "Chasseur"
