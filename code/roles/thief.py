from main_game import Game
from roles.role import Role
from bot.interactions import GarooVote, GarooEmbed
from discord import Colour


class Thief(Role):
    def __init__(self, lst_player):
        super().__init__(
            lst_player,
            image_link="https://th.bing.com/th/id/OIG4..mnb0SNFkMEkCbq.fqsw?pid=ImgGn",
            description="Le voleur est un personnage qui a le pouvoir de voler le rôle d'un autre joueur pendant la nuit.",
        )

    def night_action(self, game: Game):
        if game.turn_count != 1:
            return

        interface = GarooVote(
            entries=game.entries(game.alive_sort()),
            filter=[player.id for player in self.lst_player],
        )
        dico_vote = self.send_embed_role_interface(
            game=game,
            interface=interface,
            title="Le Voleur",
            description="Volez un joueur !",
        )
        print("Dico vote : ", dico_vote)
        max_keys = [
            key for key, value in dico_vote.items() if value == max(dico_vote.values())
        ]
        for role in game.role_list:
            for player in role.lst_player:
                if player.id != max_keys[0]:
                    break

                player.id, self.lst_player[0].id = (
                    self.lst_player[0].id,
                    player.id,
                )

                if str(role) == "Loup-Garou":
                    game.client.remove_werewolf(self.lst_player[0].id)
                    game.client.add_werewolf(player.id)

                # message au joueur qui a volé un role
                embed = GarooEmbed(
                    title=f"**{role}**",
                    description=role.description,
                    color=Colour.gold(),
                    thumbnail={"url": role.image},
                )
                dest = game.client.get_user(player.id)
                game.client.send(
                    content="Le voleur a volé ! Voici ton nouveau role:",
                    embed=embed,
                    dest=dest,
                )

                # message au joueur ayant perdu son role
                embed = GarooEmbed(
                    title=f"**{self}**",
                    description=self.description,
                    color=Colour.gold(),
                    thumbnail={"url": self.image},
                )
                dest = game.client.get_user(self.lst_player[0].id)
                game.client.send(
                    content="Le voleur a volé ! Voici ton nouveau role :",
                    embed=embed,
                    dest=dest,
                )

    def __str__(self) -> str:
        return "Voleur"
