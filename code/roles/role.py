
from bot.interactions import GarooVote, GarooEmbed
from discord import Colour

class Player:
    def __init__(self, id):
        self.id = id
        self.is_alive = True


class _Role:
    def __init__(self, lst_player : list[Player], image_link: str,description):
        self.lst_player = lst_player
        self.image=image_link
        self.description = description

    def send_embed_role(self, game, **kwargs):
        embed=GarooEmbed(
            thumbnail = {"url" : self.image},
            colour = 0x491e43,
            image=self.image,
            footer = {"text" : f"Nuit {game.turn_count} - {len(game.alive_sort())}/{len(game.id_list)} joueurs en vie",
                      "icon_url" : "https://img.freepik.com/vecteurs-premium/croissant-etoiles-icone-noire-au-clair-lune-symbole-reve-isole-fond-blanc_53562-22909.jpg"},
            **kwargs)
        game.client.send(embed=embed)

    def send_embed_role_interface(self, game, interface,**kwargs):
        embed = GarooEmbed(
            thumbnail = {"url" : self.image},
            colour = 0x491e43,
            footer = {"text" : f"Nuit {game.turn_count} - {len(game.alive_sort())}/{len(game.id_list)} joueurs en vie", 
                      "icon_url" : "https://img.freepik.com/vecteurs-premium/croissant-etoiles-icone-noire-au-clair-lune-symbole-reve-isole-fond-blanc_53562-22909.jpg"},
                      **kwargs)
        
        return game.client.send_interface(interface=interface, embed=embed)
#region Roles

class Werewolf(_Role):
    def __init__(self, lst_player):
        super().__init__(lst_player,
                         image_link="https://th.bing.com/th/id/OIG2.Dz6c9oWL5O98Mv4Vw7.S?w=1024&h=1024&rs=1&pid=ImgDetMain",
                         description="Le loup-garou est un être nocturne qui se cache parmi les villageois et qui cherche à éliminer ces derniers pour assurer sa survie.")

    def night_action(self,game):
        #INTERACTION A REMPLACER (Front)
        lst_alive = game.alive_sort()
        

        stop = False
        while stop == False:
            interface = GarooVote(entries=game.entries(lst_alive) ,filter=[player.id for player in self.lst_player])
            dico_vote = game.client.send_interface(content ="Place au vote des Loups AWOUUUUUU !",interface=interface)
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

    def __str__(self) -> str:
        return "Loup-Garou"
class Villager(_Role):
    def __init__(self, lst_player):
        super().__init__(lst_player,
                         image_link="https://th.bing.com/th/id/OIG4.iSx9lSZEfEWqvQCnPEnb?w=1024&h=1024&rs=1&pid=ImgDetMain",
                         description="Les villageois sont des habitants ordinaires de Thiercelieux qui doivent identifier et éliminer les loups-garous pour sauver leur village.")
    
    def __str__(self) -> str:
        return "Villageois"


class Seer(_Role):
    def __init__(self, lst_player):
        super().__init__(lst_player)

    
    def night_action(self,game = None):
        #INTERACTION A REMPLACER (Front)
        #--------------------------
        lst_alive = game.alive_sort()
        interface = GarooVote(entries=game.entries(lst_alive) ,filter=[player.id for player in self.lst_player])
        dico_vote = game.client.send_interface("Veuillez choisir le joueur ou la joueuse dont vous voullez voir le rôle.",interface)

        max_keys = [key for key, value in dico_vote.items() if value == max(dico_vote.values())]

        for role in game.role_list:
            for player in role.lst_player:
                if player.id == max_keys[0]:
                    user = self.client.get_user(self.id)
                    self.client.send("Voici le rôle de " + str(player) + " :" + str(player.role), dest = user)


        
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
        lst_alive = game.alive.sort()


        interface = GarooVote(entries=game.entries(lst_alive), filter=[player.id for player in self.lst_player])
        dico_vote = game.client.send_interface("Tu as été tué.e ! Il est temps de te venger !!!", interface)
        print(dico_vote)

        max_keys = [key for key, value in dico_vote.items() if value == max(dico_vote.values())]
        
        
        for role in game.role_list:
            for player in role.lst_player:
                if player.id == max_keys[0]:
                    player.is_alive = False 

        #--------------------------


class Thief(_Role):
    def __init__(self, lst_player):
        super().__init__(lst_player,
                         image_link="https://th.bing.com/th/id/OIG4..mnb0SNFkMEkCbq.fqsw?pid=ImgGn",
                         description="Le voleur est un personnage qui a le pouvoir de voler le rôle d'un autre joueur pendant la nuit.")


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
                        
                        embed=GarooEmbed(
                            title = f"**{role}**",
                            description = role.description,
                            color = Colour.gold(),
                            thumbnail = {"url" : role.image})
                        dest = game.client.get_user(player.id)
                        game.client.send(content="Le voleur a volé ! Voici ton nouveau role:",embed=embed, dest=dest)

                        embed=GarooEmbed(
                            title = f"**{self}**",
                            description = self.description,
                            color = Colour.gold(),
                            thumbnail = {"url" : self.image})
                        dest = game.client.get_user(self.lst_player[0].id)
                        game.client.send(content="Le voleur a volé ! Voici ton nouveau role :",embed=embed, dest=dest)                        

    def __str__(self) -> str:
        return "Voleur"
#endregion



night_action_list = [Werewolf, Seer, Witch, Thief]
day_action_list = [Hunter]

role_order = ["thief", "werewolf", "seer", "witch", "hunter", "villager"]

def role_order_sort(role):
    return role_order.index(role)