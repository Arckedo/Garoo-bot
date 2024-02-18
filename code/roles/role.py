
from bot.interactions import GarooVote


class Player:
    def __init__(self, id):
        self.id = id
        self.is_alive = True


class _Role:
    def __init__(self, lst_player : list[Player], image_link: str):
        self.lst_player = lst_player
        self.image=image_link

    def send_embed_role(self, game):
        game.client.send_embed(
            title="",
            description="",
            image=self.image
        )

    def send_embed_role_interface(self, game, interface,**kwargs):
        return game.client.send_embed_interface(interface=interface,
            thumbnail =  {"url" : self.image},
            colour= 0x491e43,
            footer = {"text" : f"Nuit {game.turn_count} - {len(game.alive_sort())}/{len(game.id_list)} joueurs en vie", "icon_url" : "https://img.freepik.com/vecteurs-premium/croissant-etoiles-icone-noire-au-clair-lune-symbole-reve-isole-fond-blanc_53562-22909.jpg"},
            **kwargs
        )
#region Roles

class Werewolf(_Role):
    def __init__(self, lst_player, image_link=""):
        super().__init__(lst_player,image_link)

    def night_action(self,game):
        #INTERACTION A REMPLACER (Front)
        lst_alive = game.alive_sort()
        

        stop = False
        while stop == False:
            interface = GarooVote(entries=game.entries(lst_alive) ,filter=[player.id for player in self.lst_player])
            dico_vote = game.client.send_interface("Place au vote des Loups AWOUUUUUU !",interface)
            print(dico_vote)
            
            #Renvoie la liste des clées de dico_vote dont la valeur est la plus grande
            max_keys = [key for key, value in dico_vote.items() if value == max(dico_vote.values())]
    
                
            if len(max_keys) == 1:
                for role in game.role_list:
                    for player in role.lst_player:
                        if player.id == max_keys[0]:
                            player.is_alive = False 
                            stop = True
            else:
                game.client.send(f"Des joueurs ont eu le même nombre de vote ! LES LOUPS DOIVENT SE DECIDER !")
                self.night_action(game)
        #--------------------------

class Villager(_Role):
    def __init__(self, lst_player,image_link=""):
        super().__init__(lst_player,image_link)



class Seer(_Role):
    def __init__(self, lst_player):
        super().__init__(lst_player)

    
    def night_action(self,game = None):
        #INTERACTION A REMPLACER (Front)
        #--------------------------
        pass
        #--------------------------

class Witch(_Role):
    def __init__(self, lst_player):
        super().__init__(lst_player)

    
    def night_action(self,game = None):
        #INTERACTION A REMPLACER (Front)
        #--------------------------
        pass
        #--------------------------

class Hunter(_Role):
    def __init__(self, lst_player):
        super().__init__(lst_player)

        
    def day_action(self,game = None):
        #INTERACTION A REMPLACER (Front)
        #--------------------------
        pass
        #--------------------------

class Thief(_Role):
    def __init__(self, lst_player):
        super().__init__(lst_player,"https://th.bing.com/th/id/OIG4..mnb0SNFkMEkCbq.fqsw?pid=ImgGn")


    def night_action(self,game = None):
        if game.turn_count == 1:
            interface = GarooVote(entries=game.entries(game.alive_sort()) ,filter=[player.id for player in self.lst_player])
            dico_vote = self.send_embed_role_interface(game=game, interface=interface,
                title="Le Voleur",
                description="Volez un joueur !",
                )
            print("Dico vote : ",dico_vote)
            max_keys = [key for key, value in dico_vote.items() if value == max(dico_vote.values())]
            for role in game.role_list:
                for player in role.lst_player:
                    if player.id == max_keys[0]:
                        player.id, self.lst_player[0].id = self.lst_player[0].id, player.id  

    def __str__(self) -> str:
        return "Voleur"
#endregion


night_action_list = [Thief, Werewolf, Seer, Witch]
day_action_list = [Hunter]

role_order = ["thief", "werewolf", "seer", "witch", "hunter", "villager"]

def role_order_sort(role):
    return role_order.index(role)