import random
from roles import *
from bot.interactions import GarooClient
from bot.interactions import GarooVote, GarooEmbed
from datetime import datetime
from discord import Colour


class Game:
    def __init__(self, client: GarooClient, id_list: list, start_role_list: list, turn_count: int, game_creator: int, role_list: list = None):
        """
        Initialise la partie avec les paramètres fournis.

        Args:
            client (GarooClient): Client Discord utilisable par le jeu.
            id_list (list): Liste des identifiants des joueurs.
            turn_count (int): Compteur de tours.
            role_list (list, optional): Liste des rôles, dont le premier argument est booléen
        """

        assert(start_role_list != None or role_list != None)

        self.client = client
        self.id_list = id_list
        self.turn_count = turn_count
        self.mayor_id = None
        self.game_creator = game_creator

        # Si la role_list n'est pas encore définie, trie les rôles pour les mettre dans l'ordre de passage
        if role_list is None:
            start_role_list = sorted(start_role_list, key=role_order_sort)
            self.start(start_role_list)
        else:
            # Ce coté ne fonctionne pas pour l'instant, si l'on veut reprendre une partie
            self.role_list = role_list

        self.alive_notif = self.alive_sort()


    def start(self, start_role_list):
        """
        Démarre la partie en attribuant un rôle à chaque joueur.

        Args:
            start_role_list (list): Liste des rôles à attribuer à chaque joueur.
        """

        self.role_list = []
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
        for player_id, str_role in zip(shuff_id_list, start_role_list):
            # Récupère la classe de rôle correspondante au nom de rôle
            role_class = dict_role_class[str_role]

            # Vérifie si la classe de rôle n'est pas déjà dans la liste de rôles
            if role_class not in self.role_list :
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
                embed=GarooEmbed(
                    title = f"**{role}**",
                    description = role.description,
                    color = Colour.gold(),
                    thumbnail = {"url" : role.image})
                dest = self.client.get_user(player.id)
                self.client.send(embed=embed, dest=dest)
        


    def _turn(self):
        """
        Effectue un tour de jeu.
        """

        def night_turn(self):
            self.game_embed(
                day = False,
                title= f"🌙 __Nuit {self.turn_count}__ 🌙",
                thumbnail = {"url": "https://th.bing.com/th/id/OIG2.3wENrtbwnfbEO5lMpuxI"},
                description = "Bonne nuit à toutes et à tous !"
            )

            for role in self.role_list:
                if type(role) in night_action_list:
                    role.night_action(game=self)


        def day_turn(self):
            death, resur = self.alive_notification()

            self.game_embed(
                title= f"🌅 __Jour {self.turn_count}__ 🌅",
                thumbnail = {"url": "https://th.bing.com/th/id/OIG2.OColV0JanmsfatOIhZge"},
                description = f"""L'aube éblouit Thiercelieux, Les joueurs suivant sont morts cette nuit : {", ".join(f"{self.mention(player)} : {self.find_role(player)}" for player in death)}
                \nLes joueurs suivant ont été ressuscités cette nuit : {", ".join(self.mention_lst(resur))}"""
            )

            if self.mayor_id in death:
                self.game_embed(title= f"👑 __Le maire est mort__ 👑")
                mayor_vote(self)
            for role in self.role_list:
                if type(role) in day_action_list:
                    role.day_action(game=self)

            def day_vote(self):
                # INTERACTION À REMPLACER (Front)
                lst_alive = self.alive_sort()

                interface = GarooVote(entries=self.entries(lst_alive) ,filter=lst_alive ,weight={self.mayor_id : 2})

                dico_vote = self.game_embed_interface(
                    interface=interface,
                    title="⚖️ __Le Jugement de Thiercelieux__ ⚖️",
                    description = """Au crépuscule à Thiercelieux, les villageois se rassemblent en cercle, scrutant les visages avec suspicion.
                    Chacun accuse et vote pour celui qu'il croit être un loup-garou. Les cœurs battent la chamade alors que le verdict se profile.
                    La tension est à son comble jusqu'à ce que le nom du condamné soit prononcé,
                    scellant le destin du village pour cette nuit-là.""",
                    thumbnail =  {"url": "https://th.bing.com/th/id/OIG3.Oyo.LIt40eLhGtoZU0T_"}
                )

                #Renvoie la liste des clées de dico_vote dont la valeur est la plus grande
                max_keys = [key for key, value in dico_vote.items() if value == max(dico_vote.values())]

                if len(max_keys) == 1:
                    for role in self.role_list:
                        for player in role.lst_player:
                            if player.id == max_keys[0]:
                                player.is_alive = False
                                self.alive_notification()
                                self.game_embed(
                                    title = f"🔥 __{self.name(player.id)} est brulée sur la place de thercelieux!__ 🔥",
                                    description = f"Son role était {role} !"
                                )
                                if player.id == self.mayor_id:
                                    self.game_embed(
                                    title= f"👑 __Le maire est mort__ 👑"
                                )
                                mayor_vote(self)
                else:
                    interface = GarooVote(entries=self.entries(max_keys), filter=[self.mayor_id])
                    embed = GarooEmbed(
                        title="⚖️ __Le Jugement du Maire__ ⚖️",
                        description = "Les joueurs suivants ont eu le même nombre de vote : " + str(", ".join([self.mention(player) for player in max_keys])) + " !"+
                        "\nLe maire va trancher le vote !",
                        colour=Colour.orange()
                    )
                    dico_vote = self.client.send_interface(
                        interface=interface,
                        embed=embed
                    )

                    max_keys = [key for key, value in dico_vote.items() if value == max(dico_vote.values())]

                    for role in self.role_list:
                        for player in role.lst_player:
                            if player.id == max_keys[0]:
                                player.is_alive = False
                                self.alive_notification()
                                self.game_embed(
                                    title = f"🔥 __{self.name(player.id)} est brulée sur la place de thercelieux!__ 🔥",
                                    description = f"Son role était {role} !"
                                )
                                if player.id == self.mayor_id:
                                    self.game_embed(title= f"👑 __Le maire est mort__ 👑")
                                    mayor_vote(self)

            # Appel de la fonction de vote
            day_vote(self)

        def mayor_vote(self):
            # INTERACTION À REMPLACER (Front)
            lst_alive = self.alive_sort()
            stop = False

            if self.mayor_id is not None:
                print()
                print(lst_alive)
                print([])
                interface = GarooVote(entries=self.entries(lst_alive) ,filter=[self.mayor_id])
                dico_vote = self.game_embed_interface(
                    interface=interface,
                    title="⚖️ __L'héritage du maire de Thiercelieux__ ⚖️",
                    description = """
                    À Thiercelieux, lors de la succession du maire,
                    les villageois se réunissent avec gravité. Chacun exprime ses choix, les candidats exposent leurs arguments.
                    Les votes sont recueillis, et le nom du successeur est annoncé, marquant ainsi un tournant pour le village.""",
                    thumbnail = {"url": "https://th.bing.com/th/id/OIG3.NTqM_6GH4PlXQHh1fkN8"}
                )
                for player in dico_vote:
                    if dico_vote[player] == 1:
                        embed = GarooEmbed(
                            title="⚖️ __Le Choix du maire de Thiercelieux__ ⚖️",
                            description = f"Le Maire est {self.mention(player)} !",
                            colour=Colour.green()
                        )
                        self.client.send(embed=embed)
                        self.mayor_id = player
                        stop = True
                if stop == False:
                    mayor_vote(self)

            while stop == False:
                interface = GarooVote(entries=self.entries(lst_alive) ,filter=lst_alive)

                dico_vote = self.game_embed_interface(
                    interface=interface,
                    title="⚖️ __Le Choix du maire de Thiercelieux__ ⚖️",
                    description = """À Thiercelieux, lors du vote pour le maire, les villageois se réunissent avec sérieux.
                    Chacun exprime son choix avec attention. Les candidats font leurs discours, essayant de convaincre.
                    Les votes sont déposés dans l'urne. Le nom du nouveau maire est annoncé, scellant ainsi le destin du village.""",
                    thumbnail =  {"url": "https://th.bing.com/th/id/OIG2.7ICIfw0NlW2tpNZ8O0Eu"}
                )

                #Renvoie la liste des clées de dico_vote dont la valeur est la plus grande
                max_keys = [key for key, value in dico_vote.items() if value == max(dico_vote.values())]

                if len(max_keys) == 1:
                    for role in self.role_list:
                        for player in role.lst_player:
                            if player.id == max_keys[0]:
                                player.is_mayor = True

                                embed= GarooEmbed(
                                    title="⚖️ __Le Choix du maire de Thiercelieux__ ⚖️",
                                    description = f"Le Maire est {self.mention(player.id)} !",
                                    colour=Colour.green())
                                self.client.send(embed=embed)
                                stop = True
                                self.mayor_id = player.id
                else:
                    embed = GarooEmbed(
                        title="⚖️ __Le Choix du maire de Thiercelieux__ ⚖️",
                        description = "Les joueurs suivants ont eu le même nombre de vote : " +
                        str(", ".join([self.mention(player) for player in max_keys])) + " !",
                        colour=Colour.orange())
                    self.client.send(embed=embed)

        if self.turn_count == 0:
            # INTERACTION À REMPLACER (Front)
            mayor_vote(self)

        self.turn_count += 1
        night_turn(self)

        end, winner = self.end()
        if end:
            embed= GarooEmbed(
                title = f"🔥La Partie est terminée !",
                description = winner,
                colour = Colour.green()
            )
            self.client.send(embed=embed)
            return

        day_turn(self)

        end, winner = self.end()
        if end:
            embed= GarooEmbed(
                title = f"🔥La Partie est terminée !",
                description = winner,
                colour = Colour.green()
            )
            self.client.send(embed=embed)
            return

        self._turn()


    def end(self):
        wolf = 0
        villager = 0
        for role in self.role_list:
            for player in role.lst_player:
                if player.is_alive == True:
                    if type(role) == Werewolf:
                        wolf += 1
                    else :
                        villager += 1
        if wolf == 0 and villager == 0:
            return (True, "**Les Arbres de la forets** ont gagné, les Loups-Garous et les Villageois sont tous morts !")
        elif wolf == 0:
            return (True, "Les Loups-Garous sont tous morts, **Les villageois ont gagné !**")
        elif villager == 0:
            return (True, "Les Villageois sont tous morts, **Les Loups-Garous ont gagné !**")
        else:
            return (False, None)

    def alive_sort(self):
        lst = []
        for role in self.role_list:
            for player in role.lst_player:
                if player.is_alive == True:
                    lst.append(player.id)
        return lst

    def dic_role_sort(self):
        dic = {}
        for role in self.role_list:
            for player in role.lst_player:
                dic[player.id] = str(role)
        return dic

    def alive_notification(self):
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
        for role in self.role_list:
            for player in role.lst_player:
                if player.id == player_id:
                    return role

    def name(self, player_id):
            return self.client.get_user(player_id).display_name

    def mention(self, player_id):
            return self.client.get_user(player_id).mention

    def name_lst(self, lst):
            return [self.client.get_user(player_id).display_name for player_id in lst]

    def mention_lst(self, lst):
            return [self.client.get_user(player_id).mention for player_id in lst]

    def entries(self, lst_entries):
            lst_entries.sort()
            lst = []
            for player_id in lst_entries:
                lst.append((self.client.get_user(player_id).display_name, player_id))
            return lst

    def game_embed(self, day=True, **kwargs):
        if day == True:
            footer = {"text" : f"Jour {self.turn_count} - {len(self.alive_sort())}/{len(self.id_list)} joueurs en vie",
                      "icon_url" : "https://media.istockphoto.com/id/1210517109/vector/sun-icon-vector-for-your-web-design-logo-ui-illustration.jpg?s=612x612&w=0&k=20&c=-HOJe8OyVmap1_0NDUotr2vjZ3TxVKCGA2ga9H7klvU="}
        else:
            footer = {"text" : f"Nuit {self.turn_count} - {len(self.alive_sort())}/{len(self.id_list)} joueurs en vie",
                      "icon_url" : "https://static.vecteezy.com/ti/vecteur-libre/p1/5569430-lune-nuit-clair-de-lune-minuit-icone-solide-illustrationle-modele-de-logo-adapte-a-de-nombreux-usages-gratuit-vectoriel.jpg"}

        embed = GarooEmbed(
            author = {"name": f"GarooBot - Partie de {self.client.get_user(self.game_creator).display_name}",
            "icon_url": "https://cdn.discordapp.com/avatars/1194956794812964874/029a2286b5d3df9632402b7db7336a71.webp"},
            colour= 0x6c58ff,
            footer=footer,
            timestamp=datetime.now(),
            **kwargs
        )
        return self.client.send(embed=embed)

    def game_embed_interface(self, interface, day=True, **kwargs):
        if day == True:
            footer = {"text" : f"Jour {self.turn_count} - {len(self.alive_sort())}/{len(self.id_list)} joueurs en vie",
                      "icon_url" : "https://media.istockphoto.com/id/1210517109/vector/sun-icon-vector-for-your-web-design-logo-ui-illustration.jpg?s=612x612&w=0&k=20&c=-HOJe8OyVmap1_0NDUotr2vjZ3TxVKCGA2ga9H7klvU="}
        else:
            footer = {"text" : f"Nuit {self.turn_count} - {len(self.alive_sort())}/{len(self.id_list)} joueurs en vie",
                      "icon_url" : "https://img.freepik.com/vecteurs-premium/croissant-etoiles-icone-noire-au-clair-lune-symbole-reve-isole-fond-blanc_53562-22909.jpg"}

        embed= GarooEmbed(
            author = {"name": f"GarooBot - Partie de {self.client.get_user(self.game_creator).display_name}",
            "icon_url": "https://cdn.discordapp.com/avatars/1194956794812964874/029a2286b5d3df9632402b7db7336a71.webp?size=80"},
            colour= 0x6c58ff,
            footer=footer,
            timestamp=datetime.now(),
            **kwargs
        )
        return self.client.send_interface(
            interface=interface ,
            embed=embed
        )


"""
if __name__ == "__main__":
    id_list = [1, 2, 3, 4, 5]
    role_list = ["werewolf", "villager", "seer", "witch", "hunter"]

    game = Game(id_list, role_list, turn_count=0)
    game.start()

    for player in game.player_list:
        print(f"Player {player.id} with role {player.role}")

    game._turn()"""