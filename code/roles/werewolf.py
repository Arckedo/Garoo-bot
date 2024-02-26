from bot.interactions import GarooVote
from roles.role import Role

class Werewolf(Role):
    def __init__(self, lst_player):
        super().__init__(
            lst_player,
            image_link="https://th.bing.com/th/id/OIG2.Dz6c9oWL5O98Mv4Vw7.S?w=1024&h=1024&rs=1&pid=ImgDetMain",
            description="Le loup-garou est un être nocturne qui se cache parmi les villageois et qui cherche à éliminer ces derniers pour assurer sa survie.",
        )

    def night_action(self, game):
        for player in self.lst_player:
            if player.is_alive == False:
                return

        lst_alive = game.alive_sort()

        stop = False
        while stop == False:
            interface = GarooVote(
                entries=game.entries(lst_alive),
                filter=[player.id for player in self.lst_player],
            )
            dico_vote = self.send_embed_role_interface(
                game,
                interface=interface,
                title="🐺 __Les Loups se réveillent__ 🐺",
                description="Place au vote des Loups AWOUUUUUU !",
            )

            # Renvoie la liste des clées de dico_vote dont la valeur est la plus grande
            max_keys = [
                key
                for key, value in dico_vote.items()
                if value == max(dico_vote.values())
            ]

            if len(max_keys) == 1:
                for role in game.role_list:
                    for player in role.lst_player:
                        if player.id == max_keys[0]:
                            game.wolf_kill = game.name(player.id)
                            player.is_alive = False
                            stop = True
            else:
                dico_vote = self.send_embed_role(
                    game,
                    title="🐺 __ LES LOUPS DOIVENT SE DECIDER !__ 🐺",
                    description="Des joueurs ont eu le même nombre de vote !",
                )
                self.night_action(game)

    def __str__(self) -> str:
        return "Loup-Garou"
