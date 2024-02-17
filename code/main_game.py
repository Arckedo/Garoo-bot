import random
from roles import *
from bot.interactions import GarooClient
from bot.interactions import GarooVote
from datetime import datetime

class Game:
    def __init__(self, client: GarooClient, id_list: list, start_role_list:list, turn_count:int, game_creator: int, role_list:list = None):
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
                role = role_class([Player(id=player_id)] )
                self.role_list.append(role)
            else:
                # Si la classe de rôle est déjà présente, ajoute un nouveau joueur au rôle existant
                for role in self.role_list:
                    if role_class == type(role):
                        role.player_list.append(Player(id=player_id, is_alive=True))
        


    def _turn(self):
        """
        Effectue un tour de jeu.
        """
        
        # Vérifie si la condition de fin de jeu est atteinte
        end , winner = self.end()
        if end:
            self.client.send("> La partie est finie.")
            self.client.send(winner)
            return

        def night_turn(self):
            
            self.client.send("> La nuit tombe sur Thiercelieux... \nNuit : " + str(self.turn_count))
            
            for role in self.role_list:
                if type(role) in night_action_list:
                    role.night_action(game=self)


        def day_turn(self):
            
            self.client.send("> Le jour se lève sur Thiercelieux...\n> Jour : " + str(self.turn_count))
            
            death, resur = self.alive_notification()
            self.client.send(f"> Les joueurs suivant sont morts cette nuit : {self.name_lst(death)} \n> Les joueurs suivant ont été ressucités cette nuit : {self.name_lst(resur)}")

            if self.mayor_id in death:
                self.client.send(f"> Le Maire est Mort !")
                mayor_vote(self)
            for role in self.role_list:
                if type(role) in day_action_list:
                    role.day_action(game=self)
            
            def day_vote(self):
                # INTERACTION À REMPLACER (Front)
                lst_alive = self.alive_sort()

                stop = False
                while stop == False:
                    interface = GarooVote(entries=self.entries(lst_alive) ,filter=lst_alive , weight={self.mayor_id : 2})
                    
                    dico_vote = self.game_embed_interface(interface=interface,
                    title="⚖️ __Le Jugement de Thiercelieux__ ⚖️",
                    description = """Au crépuscule à Thiercelieux, les villageois se rassemblent en cercle, scrutant les visages avec suspicion. 
                    Chacun accuse et vote pour celui qu'il croit être un loup-garou. Les cœurs battent la chamade alors que le verdict se profile. 
                    La tension est à son comble jusqu'à ce que le nom du condamné soit prononcé,
                    scellant le destin du village pour cette nuit-là.""",
                    thumbnail =  {"url" : "https://th.bing.com/th/id/OIG3.Oyo.LIt40eLhGtoZU0T_?w=1024&h=1024&rs=1&pid=ImgDetMain"}
                    )

                    #Renvoie la liste des clées de dico_vote dont la valeur est la plus grande
                    max_keys = [key for key, value in dico_vote.items() if value == max(dico_vote.values())]
        
                    
                    if len(max_keys) == 1:
                        for role in self.role_list:
                            for player in role.lst_player:
                                if player.id == max_keys[0]:
                                    player.is_alive = False
                                    self.alive_notification()
                                    self.client.send(f"> {self.client.get_user(player.id)} est brulée sur la place de thercelieux!")
                                    self.client.send(f"> Son role était {role} !")
                                    if player.id == self.mayor_id:
                                        self.client.send(f"> Le Maire est mort !")
                                        mayor_vote(self)
                                    stop = True 
                    else:
                        self.client.send(f"> Les joueurs suivants ont eu le même nombre de vote : {max_keys} !\n> Il n'y aura aucun mort lors de se vote.")
            # Appel de la fonction de vote
            day_vote(self)

        def mayor_vote(self):
            # INTERACTION À REMPLACER (Front)
            lst_alive = self.alive_sort()
            stop = False
            
            if self.mayor_id is not None:
                interface = GarooVote(entries=lst_alive ,filter=[self.mayor_id])
                dico_vote = self.client.send_interface("> L'ancien Maire doit choisir un sucesseur !",interface)
                for player in dico_vote:
                    if dico_vote[player] == 1:

                        self.mayor__id = dico_vote
                        stop = True
                if stop == False:
                    mayor_vote(self)

            while stop == False:
                interface = GarooVote(entries=self.entries(lst_alive) ,filter=lst_alive)
                dico_vote = self.client.send_interface("> Place au vote du Maire !",interface)

                #Renvoie la liste des clées de dico_vote dont la valeur est la plus grande
                max_keys = [key for key, value in dico_vote.items() if value == max(dico_vote.values())]
    
                
                if len(max_keys) == 1:
                    for role in self.role_list:
                        for player in role.lst_player:
                            if player.id == max_keys[0]:
                                player.is_mayor = True
                                self.client.send(f"> Le Maire est {self.name(player.id)} !")
                                stop = True
                                self.mayor_id = player.id
                else:
                    self.client.send(f"> Les joueurs suivants ont eu le même nombre de vote : {max_keys} !")
        

        if self.turn_count == 0:
            # INTERACTION À REMPLACER (Front)
            mayor_vote(self)

        self.turn_count += 1

        night_turn(self)
        day_turn(self)
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
            return True, "> **Les Arbres de la forets**, les Loups-Garous et les Villageois sont tous morts !"
        elif wolf == 0:
            return True, "> Les Loups-Garous sont tous morts, **Les villageois ont gagné !**"
        elif villager == 0:
            return True, "> Les Villageois sont tous morts, **Les Loups-Garous ont gagné !**"
        else:
            return False, None



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

    def name(self, player_id):
            return self.client.get_user(player_id).display_name    
    
    def name_lst(self, lst):
            return [self.client.get_user(player_id).display_name for player_id in lst]
    
    def entries(self, lst_entries):
            lst = []
            for player_id in lst_entries:
                lst.append((self.client.get_user(player_id).display_name, player_id))
            
            return lst
    
    def game_embed(self, day=True,**kwargs):
        if day == True:
            footer = {"text" : f"Jour {self.turn_count} - {len(self.alive_sort())}/{len(self.id_list)} joueurs en vie", "icon_url" : "https://media.istockphoto.com/id/1210517109/vector/sun-icon-vector-for-your-web-design-logo-ui-illustration.jpg?s=612x612&w=0&k=20&c=-HOJe8OyVmap1_0NDUotr2vjZ3TxVKCGA2ga9H7klvU="}
        else:
            footer = {"text" : f"Nuit {self.turn_count} - {len(self.alive_sort())}/{len(self.id_list)} joueurs en vie", "icon_url" : "https://static.vecteezy.com/ti/vecteur-libre/p1/5569430-lune-nuit-clair-de-lune-minuit-icone-solide-illustrationle-modele-de-logo-adapte-a-de-nombreux-usages-gratuit-vectoriel.jpg"}

        
        return self.client.send_embed(
        author = {"name": f"GarooBot - Partie de {self.client.get_user(self.game_creator).display_name}", "icon_url": "https://cdn.discordapp.com/avatars/1194956794812964874/029a2286b5d3df9632402b7db7336a71.webp?size=80"},
        colour= 0x6c58ff,
        footer=footer,
        timestamp= datetime.now(),
        **kwargs       
        )        


    def game_embed_interface(self,interface,day=True, **kwargs):
        if day == True:
            footer = {"text" : f"Jour {self.turn_count} - {len(self.alive_sort())}/{len(self.id_list)} joueurs en vie", "icon_url" : "https://media.istockphoto.com/id/1210517109/vector/sun-icon-vector-for-your-web-design-logo-ui-illustration.jpg?s=612x612&w=0&k=20&c=-HOJe8OyVmap1_0NDUotr2vjZ3TxVKCGA2ga9H7klvU="}
        else:
            footer = {"text" : f"Nuit {self.turn_count} - {len(self.alive_sort())}/{len(self.id_list)} joueurs en vie", "icon_url" : "https://static.vecteezy.com/ti/vecteur-libre/p1/5569430-lune-nuit-clair-de-lune-minuit-icone-solide-illustrationle-modele-de-logo-adapte-a-de-nombreux-usages-gratuit-vectoriel.jpg"}

        
        return self.client.send_embed_interface(interface=interface ,
        author = {"name": f"GarooBot - Partie de {self.client.get_user(self.game_creator).display_name}", "icon_url": "https://cdn.discordapp.com/avatars/1194956794812964874/029a2286b5d3df9632402b7db7336a71.webp?size=80"},
        colour= 0x6c58ff,
        footer=footer,
        timestamp= datetime.now(),
        **kwargs       
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