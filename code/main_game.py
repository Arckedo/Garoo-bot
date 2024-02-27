import random
from roles import *
from bot.interactions import GarooClient, GarooEmbed, GarooVote
from datetime import datetime
from discord import Colour


class Game:
    def __init__(
        self,
        client: GarooClient,
        id_list: list[int],
        turn_count: int,
        game_creator: int,
        role_list: list[Role] = None
    ):
        """
        Initialise la partie avec les paramètres fournis.

        Args:
            client (GarooClient): Client Discord utilisable par le jeu.
            id_list (list): Liste des identifiants des joueurs.
            turn_count (int): Compteur de tours.
            role_list (list): Liste des rôles
            game_creator (int): ID du joueur qui a crée la partie.
            wolf_kill (str, optional): ID du joueur qui a tue le Loup-Garou.
        """

        self.client = client
        self.id_list = id_list
        self.turn_count = turn_count
        self.mayor_id = None
        self.game_creator = game_creator
        self.wolf_kill = None
        self.role_list = self.role_list_creation()
        role_list = sorted(self.role_list, key=role_order_sort)
        self.start(role_list)

        self.alive_notif = self.alive_sort()


    def role_list_creation(self):
        """
        Crée la liste de rôles.

        Returns:
            list: Liste de rôles.
        """
        entries= []
        entries.append(("1", 0))
        entries.append(("2", 1))
        entries.append(("3", 2))
        interface = GarooVote(
            entries=entries,
            filter=[self.game_creator]
        )
        embed= GarooEmbed(
            title = "__Choisissez les rôles__",
            description = (f"Pour commencer la partie, choisissez une liste de roles parmit les 3 suivantes \n1 : {', '.join(roles_combinaton[len(self.id_list)-3][0])}"
                           f"\n2 : {', '.join(roles_combinaton[len(self.id_list)-3][1])}"
                           f"\n3 : {', '.join(roles_combinaton[len(self.id_list)-3][2])}"),
            color = Colour.blue()
        )
        dico_vote = self.client.send_interface(interface=interface, embed=embed)
        max_keys = [
            key
            for key, value in dico_vote.items()
            if value == max(dico_vote.values())
        ]
        return roles_combinaton[len(self.id_list)-3][max_keys[0]]

    def start(self, role_list: list[Role]):
        """
        Démarre la partie en attribuant un rôle à chaque joueur.

        Args:
            role_list (list): Liste des rôles à attribuer à chaque joueur.
        """

        self.role_list: list[Role] = []
        # Mélange les id des joueurs
        shuff_id_list = list(self.id_list)
        random.shuffle(shuff_id_list)

        dict_role_class = {
            "werewolf": Werewolf,
            "villager": Villager,
            "seer": Seer,
            "witch": Witch,
            "hunter": Hunter,
            "thief": Thief,
        }

        # Parcourt les listes de joueurs et de rôles simultanément
        for player_id, str_role in zip(shuff_id_list, role_list):
            # Récupère la classe de rôle correspondante au nom de rôle
            role_class = dict_role_class[str_role]

            # Vérifie si la classe de rôle n'est pas déjà dans la liste de rôles
            if role_class not in self.role_list:
                # Crée un nouveau rôle avec un joueur et l'ajoute à la liste de rôles
                role = role_class([Player(id=player_id)])
                self.role_list.append(role)
            else:
                # Si la classe de rôle est déjà présente, ajoute un nouveau joueur au rôle existant
                for role in self.role_list:
                    if role_class == type(role):
                        role.player_list.append(Player(id=player_id, is_alive=True))

        for role in self.role_list:
            for player in role.lst_player:
                embed = GarooEmbed(
                    title=f"**{role}**",
                    description=role.description,
                    color=Colour.gold(),
                    thumbnail={"url": role.image},
                )
                dest = self.client.get_user(player.id)
                self.client.send(embed=embed, dest=dest)

    def game_loop(self):
        """
        Effectue la boucle du jeu.
        """
        while True:
            if self.turn_count == 0:
                # INTERACTION À REMPLACER (Front)
                self.mayor_vote()

            self.turn_count += 1
            self.night_turn()

            end, winner = self.end()
            if end:
                embed = GarooEmbed(
                    title=f"🔥La Partie est terminée !",
                    description=winner,
                    colour=Colour.green(),
                )
                self.client.send(embed=embed)
                break

            self.day_turn()

            end, winner = self.end()
            if end:
                embed = GarooEmbed(
                    title=f"🔥La Partie est terminée !",
                    description=winner,
                    colour=Colour.green(),
                )
                self.client.send(embed=embed)
                break

    def mayor_vote(self):
        """
        Effectue le processus de vote pour élire le maire de Thiercelieux.

        Si le maire actuel est défini, affiche une interface de vote restreinte
        à tous les joueurs vivants sauf le maire, pour lequel un seul vote est autorisé.
        Si aucun joueur n'est élu lors de ce premier tour, recommence le processus de vote.
        Si un joueur est élu, le désigne comme nouveau maire et met fin au processus de vote.

        Si aucun joueur n'est élu lors du premier tour, affiche une interface de vote pour tous
        les joueurs vivants. En cas d'égalité des votes, le maire est désigné par le joueur
        ayant obtenu le vote du maire actuel. Si aucun joueur n'obtient ce vote, le processus
        de vote est réinitialisé jusqu'à ce qu'un joueur soit élu maire.
        """
        lst_alive = self.alive_sort()
        stop = False

        if self.mayor_id is not None:
            interface = GarooVote(
                entries=self.entries(lst_alive), filter=[self.mayor_id]
            )
            dico_vote = self.game_embed_interface(
                interface=interface,
                title="⚖️ __L'héritage du maire de Thiercelieux__ ⚖️",
                description=("À Thiercelieux, lors de la succession du maire, "
                             "les villageois se réunissent avec gravité. Chacun exprime ses choix, les candidats exposent leurs arguments. "
                             "Les votes sont recueillis, et le nom du successeur est annoncé, marquant ainsi un tournant pour le village."),
                thumbnail={
                    "url": "https://th.bing.com/th/id/OIG3.NTqM_6GH4PlXQHh1fkN8"
                },
            )
            for player in dico_vote:
                if dico_vote[player] == 1:
                    embed = GarooEmbed(
                        title="⚖️ __Le Choix du maire de Thiercelieux__ ⚖️",
                        description=f"Le Maire est {self.mention(player)} !",
                        colour=Colour.green(),
                    )
                    self.client.send(embed=embed)
                    self.mayor_id = player
                    stop = True
            if stop == False:
                self.mayor_vote()

        while stop == False:
            interface = GarooVote(entries=self.entries(lst_alive), filter=lst_alive)

            dico_vote = self.game_embed_interface(
                interface=interface,
                title="⚖️ __Le Choix du maire de Thiercelieux__ ⚖️",
                description=("À Thiercelieux, lors du vote pour le maire, les villageois se réunissent avec sérieux. "
                             "Chacun exprime son choix avec attention. Les candidats font leurs discours, essayant de convaincre. "
                             "Les votes sont déposés dans l'urne. Le nom du nouveau maire est annoncé, scellant ainsi le destin du village."),
                thumbnail={
                    "url": "https://th.bing.com/th/id/OIG2.7ICIfw0NlW2tpNZ8O0Eu"
                },
            )

            # Renvoie la liste des clées de dico_vote dont la valeur est la plus grande
            max_keys = [
                key
                for key, value in dico_vote.items()
                if value == max(dico_vote.values())
            ]

            if len(max_keys) == 1:
                for role in self.role_list:
                    for player in role.lst_player:
                        if player.id == max_keys[0]:
                            player.is_mayor = True

                            embed = GarooEmbed(
                                title="⚖️ __Le Choix du maire de Thiercelieux__ ⚖️",
                                description=f"Le Maire est {self.mention(player.id)} !",
                                colour=Colour.green(),
                            )
                            self.client.send(embed=embed)
                            stop = True
                            self.mayor_id = player.id
            else:
                embed = GarooEmbed(
                    title="⚖️ __Le Choix du maire de Thiercelieux__ ⚖️",
                    description=("Les joueurs suivants ont eu le même nombre de vote : "
                                 ", ".join([self.mention(player) for player in max_keys]) +
                                 " !"),
                    colour=Colour.orange(),
                )
                self.client.send(embed=embed)

    def night_turn(self):
        """
        Effectue les actions de la nuit pour chaque rôle.

        Affiche un message de bonne nuit à tous les joueurs et exécute les actions spécifiques à chaque rôle
        participant pendant la nuit.
        """
        self.game_embed(
            day=False,
            title=f"🌙 __Nuit {self.turn_count}__ 🌙",
            thumbnail={"url": "https://th.bing.com/th/id/OIG2.3wENrtbwnfbEO5lMpuxI"},
            description="Bonne nuit à toutes et à tous !",
        )

        for role in self.role_list:
            if type(role) in night_action_list:
                role.night_action(game=self)

    def day_turn(self):
        """
        Effectue les actions du jour après la nuit.

        Affiche un message indiquant le début du jour, notifie les joueurs décédés et ressuscités pendant la nuit,
        et exécute les actions spécifiques à chaque rôle participant pendant la journée. Si le maire est décédé pendant
        la nuit, lance le processus de vote pour élire un nouveau maire.
        """

        death, resur = self.alive_notification()

        self.game_embed(
            title=f"🌅 __Jour {self.turn_count}__ 🌅",
            thumbnail={"url": "https://th.bing.com/th/id/OIG2.OColV0JanmsfatOIhZge"},
            description=("L'aube éblouit Thiercelieux, Les joueurs suivant sont morts cette nuit : "
                        f"{', '.join(f'{self.mention(player)} : {self.find_role(player)}' for player in death)}"),
        )

        if self.mayor_id in death:
            self.game_embed(title=f"👑 __Le maire est mort__ 👑")
            self.mayor_vote()

        for role in self.role_list:
            if type(role) in day_action_list:
                role.day_action(game=self)

            end, winner = self.end()
            if end:
                return
        # Appel de la fonction de vote
        self.day_vote()

    def day_vote(self):
        """
        Effectue le processus de vote pendant la journée pour condamner un joueur.

        Les joueurs vivants participent au vote pour désigner celui qu'ils croient être un loup-garou.
        En cas de victoire d'un seul joueur, ce dernier est condamné et retiré du jeu. Si le joueur
        condamné est le maire, le jeu annonce sa mort et ouvre un nouveau processus de vote pour élire
        un nouveau maire.

        En cas d'égalité des votes, le maire actuel est appelé à trancher le vote. Si aucun joueur
        n'obtient le vote du maire, le processus de vote est relancé jusqu'à ce qu'un joueur soit condamné.
        """
        lst_alive = self.alive_sort()

        interface = GarooVote(
            entries=self.entries(lst_alive), filter=lst_alive, weight={self.mayor_id: 2}
        )

        dico_vote = self.game_embed_interface(
            interface=interface,
            title="⚖️ __Le Jugement de Thiercelieux__ ⚖️",
            description=("Au crépuscule à Thiercelieux, les villageois se rassemblent en cercle, scrutant les visages avec suspicion. "
                         "Chacun accuse et vote pour celui qu'il croit être un loup-garou. Les cœurs battent la chamade alors que le verdict se profile. "
                         "La tension est à son comble jusqu'à ce que le nom du condamné soit prononcé, "
                         "scellant le destin du village pour cette nuit-là."),
            thumbnail={"url": "https://th.bing.com/th/id/OIG3.Oyo.LIt40eLhGtoZU0T_"},
        )

        # Renvoie la liste des clées de dico_vote dont la valeur est la plus grande
        max_keys = [
            key for key, value in dico_vote.items() if value == max(dico_vote.values())
        ]

        if len(max_keys) == 1:
            for role in self.role_list:
                for player in role.lst_player:
                    if player.id == max_keys[0]:
                        player.is_alive = False
                        self.alive_notification()
                        self.game_embed(
                            title=f"🔥 __{self.name(player.id)} est brulée sur la place de thercelieux!__ 🔥",
                            description=f"Son role était {role} !",
                        )
                        if player.id == self.mayor_id:
                            self.game_embed(title=f"👑 __Le maire est mort__ 👑")
                        self.mayor_vote()
        else:
            interface = GarooVote(
                entries=self.entries(max_keys), filter=[self.mayor_id]
            )
            embed = GarooEmbed(
                title="⚖️ __Le Jugement du Maire__ ⚖️",
                description=("Les joueurs suivants ont eu le même nombre de vote : "
                             ", ".join([self.mention(player) for player in max_keys]) +
                             "\nLe maire va trancher le vote !"),
                colour=Colour.orange(),
            )
            dico_vote = self.client.send_interface(interface=interface, embed=embed)

            max_keys = [
                key
                for key, value in dico_vote.items()
                if value == max(dico_vote.values())
            ]

            for role in self.role_list:
                for player in role.lst_player:
                    if player.id == max_keys[0]:
                        player.is_alive = False
                        self.alive_notification()
                        self.game_embed(
                            title=f"🔥 __{self.name(player.id)} est brulée sur la place de thercelieux!__ 🔥",
                            description=f"Son role était {role} !",
                        )
                        if player.id == self.mayor_id:
                            self.game_embed(title=f"👑 __Le maire est mort__ 👑")
                            self.mayor_vote()

    def end(self):
        """
        Vérifie si la partie est terminée et détermine le vainqueur.

        Returns:
            tuple: Un tuple contenant un booléen indiquant si la partie est terminée et un message de résultat.
                - Si la partie est terminée, le booléen est True et le message indique le vainqueur.
                - Sinon, le booléen est False et le message est None.
        """
        wolf = 0
        villager = 0
        for role in self.role_list:
            for player in role.lst_player:
                if player.is_alive == True:
                    if type(role) == Werewolf:
                        wolf += 1
                    else:
                        villager += 1
        if wolf == 0 and villager == 0:
            return (
                True,
                "**Les Arbres de la forets** ont gagné, les Loups-Garous et les Villageois sont tous morts !",
            )
        elif wolf == 0:
            return (
                True,
                "Les Loups-Garous sont tous morts, **Les villageois ont gagné !**",
            )
        elif villager == 0:
            return (
                True,
                "Les Villageois sont tous morts, **Les Loups-Garous ont gagné !**",
            )
        else:
            return (False, None)

    def alive_sort(self):
        """
        Trie les joueurs vivants et retourne une liste de leurs identifiants.

        Returns:
            list: Liste des identifiants des joueurs vivants.
        """
        lst = []
        for role in self.role_list:
            for player in role.lst_player:
                if player.is_alive == True:
                    lst.append(player.id)
        return lst

    def dic_role_sort(self):
        """
        Trie les joueurs par rôle et retourne un dictionnaire associant chaque joueur à son rôle.

        Returns:
            dict: Dictionnaire associant les identifiants des joueurs à leurs rôles.
        """
        dic = {}
        for role in self.role_list:
            for player in role.lst_player:
                dic[player.id] = str(role)
        return dic

    def alive_notification(self):
        """
        Notifie les événements de décès et de résurrection des joueurs.

        Returns:
            tuple: Une paire de listes contenant les identifiants des joueurs décédés et ressuscités.
        """
        death = []
        resur = []

        for role in self.role_list:
            for player in role.lst_player:
                if player.is_alive == False and player.id in self.alive_notif:
                    death.append(player.id)
                if player.is_alive == True and player.id not in self.alive_notif:
                    resur.append(player.id)
        self.alive_notif = self.alive_sort()
        return death, resur

    def find_role(self, player_id):
        """
        Trouve le rôle d'un joueur à partir de son identifiant.

        Args:
            player_id (int): L'identifiant du joueur.

        Returns:
            str: Le rôle du joueur.
        """
        for role in self.role_list:
            for player in role.lst_player:
                if player.id == player_id:
                    return role

    def name(self, player_id):
        """
        Trouve le rôle d'un joueur à partir de son identifiant.

        Args:
            player_id (int): L'identifiant du joueur.

        Returns:
            str: Le rôle du joueur.
        """
        return self.client.get_user(player_id).display_name

    def mention(self, player_id):
        """
        Renvoie la mention d'un joueur à partir de son identifiant.

        Args:
            player_id (int): L'identifiant du joueur.

        Returns:
            str: La mention du joueur.
        """
        return self.client.get_user(player_id).mention

    def name_lst(self, lst):
        """
        Renvoie une liste des noms d'affichage des joueurs à partir d'une liste d'identifiants.

        Args:
            lst (list): Liste des identifiants des joueurs.

        Returns:
            list: Liste des noms d'affichage des joueurs.
        """
        return [self.client.get_user(player_id).display_name for player_id in lst]

    def mention_lst(self, lst):
        """
        Renvoie une liste des mentions des joueurs à partir d'une liste d'identifiants.

        Args:
            lst (list): Liste des identifiants des joueurs.

        Returns:
            list: Liste des mentions des joueurs.
        """
        return [self.client.get_user(player_id).mention for player_id in lst]

    def entries(self, lst_entries):
        """
        Trie et renvoie une liste de tuples contenant les noms d'affichage et les identifiants des joueurs.

        Args:
            lst_entries (list): Liste des identifiants des joueurs.

        Returns:
            list: Liste de tuples contenant les noms d'affichage et les identifiants des joueurs.
        """
        lst_entries.sort()
        lst = []
        for player_id in lst_entries:
            lst.append((self.client.get_user(player_id).display_name, player_id))
        return lst

    def game_embed(self, day=True, **kwargs):
        """
        Crée un embed pour la partie en cours.

        Args:
            day (bool, optional): Indique si c'est le jour ou la nuit. Par défaut, True.
            **kwargs: Arguments supplémentaires à passer à l'embed.

        Returns:
            discord.Message: Message contenant l'embed créé.
        """
        if day == True:
            footer = {
                "text": f"Jour {self.turn_count} - {len(self.alive_sort())}/{len(self.id_list)} joueurs en vie",
                "icon_url": "https://media.istockphoto.com/id/1210517109/vector/sun-icon-vector-for-your-web-design-logo-ui-illustration.jpg?s=612x612&w=0&k=20&c=-HOJe8OyVmap1_0NDUotr2vjZ3TxVKCGA2ga9H7klvU=",
            }
        else:
            footer = {
                "text": f"Nuit {self.turn_count} - {len(self.alive_sort())}/{len(self.id_list)} joueurs en vie",
                "icon_url": "https://static.vecteezy.com/ti/vecteur-libre/p1/5569430-lune-nuit-clair-de-lune-minuit-icone-solide-illustrationle-modele-de-logo-adapte-a-de-nombreux-usages-gratuit-vectoriel.jpg",
            }

        embed = GarooEmbed(
            author={
                "name": f"GarooBot - Partie de {self.client.get_user(self.game_creator).display_name}",
                "icon_url": "https://cdn.discordapp.com/avatars/1194956794812964874/029a2286b5d3df9632402b7db7336a71.webp",
            },
            colour=0x6C58FF,
            footer=footer,
            timestamp=datetime.now(),
            **kwargs,
        )
        return self.client.send(embed=embed)

    def game_embed_interface(self, interface, day=True, **kwargs):
        """
        Crée un embed pour l'interface de jeu en cours.

        Args:
            interface (discord.ui.View): L'interface de jeu.
            day (bool, optional): Indique si c'est le jour ou la nuit. Par défaut, True.
            **kwargs: Arguments supplémentaires à passer à l'embed.

        Returns:
            discord.Message: Message contenant l'interface de jeu et l'embed créés.
        """
        if day == True:
            footer = {
                "text": f"Jour {self.turn_count} - {len(self.alive_sort())}/{len(self.id_list)} joueurs en vie",
                "icon_url": "https://media.istockphoto.com/id/1210517109/vector/sun-icon-vector-for-your-web-design-logo-ui-illustration.jpg?s=612x612&w=0&k=20&c=-HOJe8OyVmap1_0NDUotr2vjZ3TxVKCGA2ga9H7klvU=",
            }
        else:
            footer = {
                "text": f"Nuit {self.turn_count} - {len(self.alive_sort())}/{len(self.id_list)} joueurs en vie",
                "icon_url": "https://img.freepik.com/vecteurs-premium/croissant-etoiles-icone-noire-au-clair-lune-symbole-reve-isole-fond-blanc_53562-22909.jpg",
            }

        embed = GarooEmbed(
            author={
                "name": f"GarooBot - Partie de {self.client.get_user(self.game_creator).display_name}",
                "icon_url": "https://cdn.discordapp.com/avatars/1194956794812964874/029a2286b5d3df9632402b7db7336a71.webp?size=80",
            },
            colour=0x6C58FF,
            footer=footer,
            timestamp=datetime.now(),
            **kwargs,
        )
        return self.client.send_interface(interface=interface, embed=embed)
