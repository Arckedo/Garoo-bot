from discord import ApplicationContext, Bot, Cog, slash_command
from main_game import Game
from bot.interactions import GarooClient

class GarooCommands(Cog):
    def __init__(self, bot) -> None:
        self.bot: Bot = bot

    @slash_command(name="loupgarou")
    async def new_game(self, ctx: ApplicationContext):
        """Démarre une nouvelle partie de Loup-Garou 🐺"""


        client = GarooClient(self.bot, ctx.channel)
        
        id_list = [508005660516941824, 1204803272347619474, 663518185068429332]
        role_list = ["werewolf", "villager", "villager"]
        game = Game(client, id_list, role_list, turn_count=0)

        await ctx.respond("La partie a été créée et débutera sous peu.")
        for id,role in game.dic_role_sort().items():
            print(f"Player {id} with role {[role]}")
        game._turn()


# Fonction nécéssaire au chargement de l'extension par le bot
def setup(bot):
    bot.add_cog(GarooCommands(bot))