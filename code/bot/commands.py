from discord import (
    ApplicationContext,
    Bot,
    ButtonStyle,
    Cog,
    Colour,
    Embed,
    Interaction,
    Member,
    User,
    slash_command,
    option
)
from discord.ui import View, Button
from main_game import Game
from bot.interactions import GarooClient, GarooEmbed
import asyncio



class StartEmbed(Embed):
    def __init__(self, author: Member) -> None:
        super().__init__(
            title=f"{author.display_name} organise une partie de loup-garou !",
            description="Cliquez sur **Rejoindre** pour commencer la partie.",
            colour=Colour.green(),
        )


class StartView(View):
    def __init__(self, event: asyncio.Event, minimum_players: int) -> None:
        super().__init__()
        self.event = event
        self.player_list: list[User] = []
        self.minimum_players = minimum_players
        button = Button(label=f"Rejoindre 0/{minimum_players}", style=ButtonStyle.green)
        self.add_item(button)

    async def interaction_check(self, interaction: Interaction) -> bool:
        if self.minimum_players < 3:
            self.minimum_players = 3
        if not interaction.user in self.player_list:
            self.player_list.append(interaction.user)
            self.children[0].label = (
                f"Rejoindre {len(self.player_list)}/{self.minimum_players}"
            )
            await interaction.response.send_message(
                embed=GarooEmbed(
                    description=f"{interaction.user.mention} a rejoins la partie.",
                    colour=Colour.green(),
                )
            )

        if len(self.player_list) >= self.minimum_players:
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
    @option("minimum_players", description="Nombre de joueurs minimum", default=3, min_value=3, max_value=10)
    async def new_game(self, ctx: ApplicationContext, minimum_players: int = 3):
        """Démarre une nouvelle partie de Loup-Garou 🐺"""

        # Crée l'interface, puis l'envoie et attend les résultats
        embed = StartEmbed(ctx.author)
        view = StartView(asyncio.Event(), minimum_players=minimum_players)
        await ctx.respond(embed=embed, view=view)
        await view.event.wait()

        # Envoie la liste des participants quand la partie commence

        client = GarooClient(self.bot, ctx.channel)
        # id_list = [508005660516941824, 1204803272347619474, 663518185068429332]
        id_list = [p.id for p in view.player_list]
        role_list = ["thief", "werewolf", "witch"]
        game = Game(
            client, id_list, role_list, turn_count=0, game_creator=ctx.author.id
        )

        # /!\ PLACEHOLDER : id de Rag
        await client.setup_werewolf_channel([508005660516941824])

        await ctx.respond(
            embed=GarooEmbed(
                title="Partie de loup-garou créée !",
                description="La partie démarrera sous peu avec les joueurs suivants : "
                 + str(
                    ", ".join([player.mention for player in view.player_list])
                    + " !\n"
                    + "Bonne chance a tous les joueurs !"
                ),
                colour=Colour.green(),
            )
        )

        for id, role in game.dic_role_sort().items():
            print(f"Player {client.get_user(id).name} with role {[role]}")
        game.game_loop()


# Fonction nécéssaire au chargement de l'extension par py-cord
def setup(bot):
    bot.add_cog(GarooCommands(bot))
