from bot.interactions import GarooVote
from roles.role import Role

class Witch(Role):
    def __init__(self, lst_player):
        super().__init__(
            lst_player,
            image_link="https://th.bing.com/th/id/OIG4.9pbEKgARXLM3iQo47uH6?w=1024&h=1024&rs=1&pid=ImgDetMain",
            description="La sorcière est un personnage qui a le pouvoir de sauver ou d'empoisonner un joueur pendant la nuit.",
        )
        self.life_potion = True
        self.death_potion = True

    def night_action(self, game=None):
        """
        Effectue l'action de nuit de la sorcière.

        La sorcière a le pouvoir de sauver ou d'empoisonner un joueur pendant la nuit.
        """
        if self.lst_player[0].is_alive == False and game.wolf_kill != game.name(self.lst_player[0].id):
            return
        
        lst_player = []
        for role in game.role_list:
            for player in role.lst_player:
                lst_player.append(player)

        dest = game.client.get_user(self.lst_player[0].id)

        self.send_embed_role(
            game,
            dest=dest,
            title="⚗️ __Pouvoirs de la sorcière__ ⚗️",
            description="La sorcière se tient prete à utiliser ses pouvoirs mais avant elle peut regarder le joueur mort par les loup-garous : "
            + game.wolf_kill
        )

        entries = game.entries([player.id for player in lst_player])
        entries.append(("Ne rien faire", -1))
        interface = GarooVote(
            entries=entries, filter=[player.id for player in self.lst_player]
        )

        dico_vote = self.send_embed_role_interface(
            game,
            interface=interface,
            title="⚗️ __Pouvoirs de la sorcière__ ⚗️",
            description="""La nuit est sombre et mystérieuse. La sorcière se tient prête à utiliser ses pouvoirs
            pour sauver ou empoisonner un joueur. Faites votre choix avec sagesse.""",
        )

        for player, vote in dico_vote.items():
            if vote == 1:
                if player == -1:
                    return
                chosen_player = player
                break
        
        for role in game.role_list:
            for player in role.lst_player:
                if player.id == chosen_player:
                    if player.is_alive == False and self.life_potion == True:
                        self.life_potion = False
                        player.is_alive = True
                        self.send_embed_role(
                            game,
                            dest=dest,
                            title="⚕️ __Sauvetage de la sorcière__ ⚕️",
                            description=f"{game.name(player.id)} a été sauvé par la sorcière.",
                        )
                        return
                    elif player.is_alive == True and self.death_potion == True:
                        player.is_alive = False
                        self.death_potion = False
                        self.send_embed_role(
                            game,
                            dest=dest,
                            title="☠️ __Empoisonnement de la sorcière__ ☠️",
                            description=f"{game.name(player.id)} a été empoisonné par la sorcière.",
                        )
                        return

        self.send_embed_role(
            game,
            dest=dest,
            title="⚗️ __Pouvoirs de la sorcière__ ⚗️",
            description="La sorcière n'a pas pu sauver ou empoisonner un joueur. Elle doit refaire un choix.",
        )
        self.night_action(game)
    def __str__(self) -> str:
        return "Sorcière"