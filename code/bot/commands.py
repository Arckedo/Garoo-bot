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
    option,
)
from discord.ui import View, Button
from main_game import Game
from bot.interactions import GarooClient, GarooEmbed
from roles import Werewolf
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
        if not interaction.user in self.player_list:
            self.player_list.append(interaction.user)
            self.children[0].label = (
                f"Rejoindre {len(self.player_list)}/{self.minimum_players}"
            )
            embed = GarooEmbed(
                description=f"{interaction.user.mention} a rejoins la partie.",
                colour=Colour.green(),
            )
            await interaction.response.send_message(embed=embed)

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
    @option(
        "minimum_players",
        description="Nombre de joueurs minimum",
        default=3,
        min_value=3,
        max_value=10,
    )
    async def new_game(self, ctx: ApplicationContext, minimum_players: int = 3):
        """Démarre une nouvelle partie de Loup-Garou 🐺"""

        # Crée l'interface, puis l'envoie et attend les résultats
        embed = StartEmbed(ctx.author)
        view = StartView(asyncio.Event(), minimum_players=minimum_players)
        await ctx.respond(embed=embed, view=view)
        await view.event.wait()

        client = GarooClient(self.bot, ctx.channel)
        id_list = [p.id for p in view.player_list]
        game = Game(client, id_list, turn_count=0, game_creator=ctx.author.id)

        # Détermine la liste des joueurs avec le rôle Loup-Garou
        werewolf_ids = []
        for role in game.role_list:
            if not isinstance(role, Werewolf):
                continue
            for player in role.lst_player:
                werewolf_ids.append(player.id)
            break

        # Créé un salon privé pour les Loups-Garous
        await client.setup_werewolf_channel(werewolf_ids)

        embed = GarooEmbed(
            title="Partie de loup-garou créée !",
            description=(
                "La partie démarrera sous peu avec les joueurs suivants : "
                + ", ".join([player.mention for player in view.player_list])
                + "\nBonne chance a tous les joueurs !"
            ),
            colour=Colour.green(),
        )
        # Envoie la réponse à la commande
        await ctx.respond(embed=embed)

        # Affiche la liste des joueurs avec leur rôle dans la console
        for id, role in game.dic_role_sort().items():
            print(f"Player {client.get_user(id).name} with role {[role]}")

        # Démarre la partie
        async def start():
            await game.game_loop()

        asyncio.create_task(start())

        # On utilise asyncio pour que la fonction actuelle (new_game)
        # se termine sans attendre la fin de game_loop
