from discord import ApplicationContext, Bot, ButtonStyle, Cog, Colour, Embed, Interaction, Member, User, slash_command
from discord.ui import View, Button
from main_game import Game
from bot.interactions import GarooClient
import asyncio

# Nombre minimum de joueurs pour commencer une partie
MINIMUM_PLAYERS = 3


class StartEmbed(Embed):
    def __init__(self, author: Member) -> None:
        super().__init__(
            title=f"{author.display_name} organise une partie de loup-garou !",
            description="Cliquez sur **Rejoindre** pour commencer la partie.",
            colour=Colour.green()
        )


class StartView(View):
    def __init__(self, event: asyncio.Event) -> None:
        super().__init__()
        self.event = event
        self.player_list: list[User] = []
        button = Button(label=f"Rejoindre 0/{MINIMUM_PLAYERS}", style=ButtonStyle.green)
        self.add_item(button)

    async def interaction_check(self, interaction: Interaction) -> bool:
        if not interaction.user in self.player_list:
            self.player_list.append(interaction.user)
            self.children[0].label = f"Rejoindre {len(self.player_list)}/{MINIMUM_PLAYERS}"
            await interaction.response.send_message(f"{interaction.user.mention} a rejoins la partie.")

        if len(self.player_list) >= MINIMUM_PLAYERS:
            self.children[0].disabled = True
            self.children[0].style = ButtonStyle.gray
            self.children[0].label = "Partie commencée !"
            self.event.set()

        await interaction.message.edit(view=self)
        return False


class GarooCommands(Cog):
    def __init__(self, bot) -> None:
        self.bot: Bot = bot

    @slash_command(name="loupgarou")
    async def new_game(self, ctx: ApplicationContext):
        """Démarre une nouvelle partie de Loup-Garou 🐺"""

        # Crée l'interface, puis l'envoie et attend les résultats
        embed = StartEmbed(ctx.author)
        view = StartView(asyncio.Event())
        await ctx.respond(embed=embed, view=view)
        await view.event.wait()

        # Envoie la liste des participants quand la partie commence
        await ctx.send(
            "La partie commence avec les joueurs : "
            + ", ".join([player.mention for player in view.player_list])
        )

        client = GarooClient(self.bot, ctx.channel)
        #id_list = [508005660516941824, 1204803272347619474, 663518185068429332]
        id_list = [p.id for p in view.player_list]
        role_list = ["werewolf", "villager", "villager"]
        game = Game(client, id_list, role_list, turn_count=0)

        # /!\ PLACEHOLDER : id de Rag
        await client.setup_werewolf_channel([508005660516941824])

        await ctx.respond("La partie a été créée et débutera sous peu.")
        for id,role in game.dic_role_sort().items():
            print(f"Player {id} with role {[role]}")
        game._turn()


# Fonction nécéssaire au chargement de l'extension par py-cord
def setup(bot):
    bot.add_cog(GarooCommands(bot))