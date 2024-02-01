from discord import ApplicationContext, Bot, Cog, slash_command
from main_game import Game
from bot.interactions import GarooClient


class GarooCommands(Cog):
    def __init__(self, bot) -> None:
        self.bot: Bot = bot

    @slash_command(name="loupgarou")
    async def new_game(self, ctx: ApplicationContext):
        """Démarre une nouvelle partie de Loup-Garou 🐺"""

        id_list = [1, 2, 3, 4, 5]
        role_list = ["werewolf", "villager", "seer", "witch", "hunter"]
        game = Game(GarooClient(self.bot, ctx.channel), id_list, role_list, turn_count=0)

        await ctx.respond("La partie a été créée et débutera sous peu.")

        game.start()
        for player in game.player_list:
            print(f"Player {player.id} with role {player.role}")
        game._turn()


# Fonction nécéssaire au chargement de l'extension par le bot
def setup(bot):
    bot.add_cog(GarooCommands(bot))