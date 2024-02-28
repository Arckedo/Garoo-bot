from bot.interactions import GarooEmbed


class Player:
    def __init__(self, id: int):
        self.id = id
        self.is_alive = True
        self.is_mayor = False


class Role:
    def __init__(self, lst_player: list[Player], image_link: str, description):
        self.lst_player = lst_player
        self.image = image_link
        self.description = description

    def send_embed_role(self, game, dest=None, **kwargs):
        if dest == None:
            dest = game.client.channel
        embed = GarooEmbed(
            thumbnail={"url": self.image},
            colour=0x491E43,
            footer={
                "text": f"Nuit {game.turn_count} - {len(game.alive_sort())}/{len(game.id_list)} joueurs en vie",
                "icon_url": "https://img.freepik.com/vecteurs-premium/croissant-etoiles-icone-noire-au-clair-lune-symbole-reve-isole-fond-blanc_53562-22909.jpg",
            },
            **kwargs,
        )
        game.client.send(embed=embed, dest=dest)

    def send_embed_role_interface(self, game, interface, dest=None, **kwargs):
        if dest == None:
            dest = game.client.channel
        embed = GarooEmbed(
            thumbnail={"url": self.image},
            colour=0x491E43,
            footer={
                "text": f"Nuit {game.turn_count} - {len(game.alive_sort())}/{len(game.id_list)} joueurs en vie",
                "icon_url": "https://img.freepik.com/vecteurs-premium/croissant-etoiles-icone-noire-au-clair-lune-symbole-reve-isole-fond-blanc_53562-22909.jpg",
            },
            **kwargs,
        )

        return game.client.send_interface(interface=interface, embed=embed, dest=dest)


role_order = ["thief", "seer", "werewolf", "witch", "hunter", "villager"]


def role_order_sort(role):
    return role_order.index(role)
