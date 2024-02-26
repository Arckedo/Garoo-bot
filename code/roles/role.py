from bot.interactions import GarooVote, GarooEmbed
from discord import Colour


class Player:
    def __init__(self, id: int):
        self.id = id
        self.is_alive = True


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


# region Roles


class Werewolf(Role):
    def __init__(self, lst_player):
        super().__init__(
            lst_player,
            image_link="https://th.bing.com/th/id/OIG2.Dz6c9oWL5O98Mv4Vw7.S?w=1024&h=1024&rs=1&pid=ImgDetMain",
            description="Le loup-garou est un être nocturne qui se cache parmi les villageois et qui cherche à éliminer ces derniers pour assurer sa survie.",
        )

    def night_action(self, game):
        # INTERACTION A REMPLACER (Front)
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
                            player.is_alive = False
                            stop = True
            else:
                dico_vote = self.send_embed_role(
                    game,
                    title="🐺 __ LES LOUPS DOIVENT SE DECIDER !__ 🐺",
                    description="Des joueurs ont eu le même nombre de vote !",
                )
                self.night_action(game)
        # --------------------------

    def __str__(self) -> str:
        return "Loup-Garou"


class Villager(Role):
    def __init__(self, lst_player):
        super().__init__(
            lst_player,
            image_link="https://th.bing.com/th/id/OIG4.iSx9lSZEfEWqvQCnPEnb?w=1024&h=1024&rs=1&pid=ImgDetMain",
            description="Les villageois sont des habitants ordinaires de Thiercelieux qui doivent identifier et éliminer les loups-garous pour sauver leur village.",
        )

    def __str__(self) -> str:
        return "Villageois"


class Seer(Role):
    def __init__(self, lst_player):
        super().__init__(
            lst_player,
            image_link="https://th.bing.com/th/id/OIG4.p4Gc8moHi1vpdfcHsYFL?w=1024&h=1024&rs=1&pid=ImgDetMain",
            description="La Voyante, guidée par son don divinatoire, révèle chaque nuit l'identité d'un habitant de Thiercelieux, distinguant les villageois des Loups-Garous. Son pouvoir est une arme à double tranchant : révéler la vérité peut aider le village, mais cela expose également la Voyante au danger mortel des Loups-Garous."
        )

    
    def night_action(self,game = None):
        lst_alive = game.alive_sort()
        interface = GarooVote(entries=game.entries(lst_alive) ,filter=[player.id for player in self.lst_player])
        dico_vote = self.send_embed_role_interface(
            game,
            interface=interface,
            title="🔮 __Magie de la vision__ 🔮",
            description="Veuillez choisir le joueur ou la joueuse dont vous voullez voir le rôle.",
        )
        max_keys = [key for key, value in dico_vote.items() if value == max(dico_vote.values())]

        for role in game.role_list:
            for player in role.lst_player:
                if player.id == max_keys[0]:
                    user = game.client.get_user(self.lst_player[0].id)
                    self.send_embed_role(
                        game,
                        title="🔮 __Magie de la vision__ 🔮",
                        description="Voici le rôle de " + game.name(player.id) + " : " + game.find_role(player.id),
                        dest=user
                    )

    def __str__(self) -> str:
        return "Voyante"
    
class Witch(Role):
    def __init__(self, lst_player):
        super().__init__(
            lst_player,
            image_link="https://th.bing.com/th/id/OIG4.9pbEKgARXLM3iQo47uH6?w=1024&h=1024&rs=1&pid=ImgDetMain",
            description="La sorcière est un personnage qui a le pouvoir de sauver ou d'empoisonner un joueur pendant la nuit.",
        )

    def night_action(self, game=None):
        """
        Effectue l'action de nuit de la sorcière.

        La sorcière a le pouvoir de sauver ou d'empoisonner un joueur pendant la nuit.
        """

        lst_player = []
        for role in game.role_list:
            for player in role.lst_player:
                lst_player.append(player)

        dest = game.client.get_user(self.lst_player[0].id)

        self.send_embed_role(
            game,
            dest=dest,
            title="⚗️ __Pouvoirs de la sorcière__ ⚗️",
            description="La sorcière se tient prete à utiliser ses pouvoirs mais avant elle peut regarder les joueurs en vie :"
            + ", ".join([game.name(player) for player in game.alive_sort()]),
        )

        entries = game.entries([player.id for player in lst_player])
        entries.append(("Ne rien faire", None))
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
                chosen_player = player
                break

        for role in game.role_list:
            for player in role.lst_player:
                if player.id == chosen_player:
                    if player.is_alive == False:
                        player.is_alive = True
                        self.send_embed_role(
                            game,
                            dest=dest,
                            title="⚕️ __Sauvetage de la sorcière__ ⚕️",
                            description=f"{game.name(player)} a été sauvé par la sorcière.",
                        )
                    elif player.is_alive == True:
                        player.is_alive = False
                        self.send_embed_role(
                            game,
                            dest=dest,
                            title="☠️ __Empoisonnement de la sorcière__ ☠️",
                            description=f"{game.name(player)} a été empoisonné par la sorcière.",
                        )

    def __str__(self) -> str:
        return "Sorcière"


class Hunter(Role):
    def __init__(self, lst_player):
        super().__init__(
            lst_player,
            image_link="https://th.bing.com/th/id/OIG1.NRxdBY8IRZ_5GTtIsfHH?pid=ImgGn",
            description="Le Chasseur, toujours en embuscade, riposte avec sa flèche mortelle dès qu'il est attaqué par les Loups-Garous. Sa mort est une revanche : il choisit une cible à emporter avec lui dans la tombe, bouleversant le cours du jeu."
        )

        
    def day_action(self,game = None):
        #INTERACTION A REMPLACER (Front)
        #--------------------------
        lst_alive = game.alive.sort()


        interface = GarooVote(entries=game.entries(lst_alive), filter=[player.id for player in self.lst_player])
        dico_vote = self.send_embed_role_interface(
            game,
            interface = interface,
            title="🏹 __Chasseur__ 🏹",
            description="Tu as été tué.e ! Il est temps de te venger !!!"    
        )

        max_keys = [key for key, value in dico_vote.items() if value == max(dico_vote.values())]
        
        
        for role in game.role_list:
            for player in role.lst_player:
                if player.id == max_keys[0]:
                    player.is_alive = False 

    def __str__(self) -> str:
        return "Chasseur"

class Thief(Role):
    def __init__(self, lst_player):
        super().__init__(
            lst_player,
            image_link="https://th.bing.com/th/id/OIG4..mnb0SNFkMEkCbq.fqsw?pid=ImgGn",
            description="Le voleur est un personnage qui a le pouvoir de voler le rôle d'un autre joueur pendant la nuit.",
        )

    def night_action(self, game=None):
        if game.turn_count == 1:
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
                key
                for key, value in dico_vote.items()
                if value == max(dico_vote.values())
            ]
            for role in game.role_list:
                for player in role.lst_player:
                    if player.id == max_keys[0]:

                        player.id, self.lst_player[0].id = (
                            self.lst_player[0].id,
                            player.id,
                        )

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


# endregion


night_action_list = [Thief, Seer, Werewolf, Witch]
day_action_list = [Hunter]

role_order = ["thief","seer", "werewolf", "witch", "hunter", "villager"]


def role_order_sort(role):
    return role_order.index(role)
