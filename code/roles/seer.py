from roles.role import Role
from bot.interactions import GarooVote


class Seer(Role):
    def __init__(self, lst_player):
        super().__init__(
            lst_player,
            image_link="https://th.bing.com/th/id/OIG4.p4Gc8moHi1vpdfcHsYFL?w=1024&h=1024&rs=1&pid=ImgDetMain",
            description="La Voyante, guidée par son don divinatoire, révèle chaque nuit l'identité d'un habitant de Thiercelieux, distinguant les villageois des Loups-Garous. Son pouvoir est une arme à double tranchant : révéler la vérité peut aider le village, mais cela expose également la Voyante au danger mortel des Loups-Garous.",
        )

    def night_action(self, game=None):
        if self.lst_player[0].is_alive == False:
            return

        lst_alive = game.alive_sort()
        interface = GarooVote(
            entries=game.entries(lst_alive),
            filter=[player.id for player in self.lst_player],
        )
        dico_vote = self.send_embed_role_interface(
            game,
            interface=interface,
            title="🔮 __Magie de la vision__ 🔮",
            description="Veuillez choisir le joueur ou la joueuse dont vous voullez voir le rôle.",
        )
        max_keys = [
            key for key, value in dico_vote.items() if value == max(dico_vote.values())
        ]

        for role in game.role_list:
            for player in role.lst_player:
                if player.id == max_keys[0]:
                    user = game.client.get_user(self.lst_player[0].id)
                    self.send_embed_role(
                        game,
                        title="🔮 __Magie de la vision__ 🔮",
                        description="Voici le rôle de "
                        + game.name(player.id)
                        + " : "
                        + str(game.find_role(player.id)),
                        dest=user,
                    )

    def __str__(self) -> str:
        return "Voyante"
