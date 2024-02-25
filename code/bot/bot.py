import discord
from bot.interactions import GarooClient, GarooChoose


# Préparation des "intents" (permissions du bot au niveau API)
intents = discord.Intents.default()
intents.message_content = True

# Création de l'objet bot
bot = discord.Bot(intents=intents)

# Les serveurs discord dans lesquels le bot créera des slash commands
bot.debug_guilds = [1194944354859614339]

# Chargement de l'extension (le cog) contenant les commandes
from bot.commands import GarooCommands
bot.add_cog(GarooCommands(bot))


# Ces fonctions sont des évènements gérés par pycord
@bot.event
async def on_ready():
    print(f"Connecté en tant que {bot.user} dans {len(bot.guilds)} guildes")


@bot.event
async def on_message(message: discord.Message):
    if message.author.id == bot.user.id:
        return

    if message.content == "$test":
        # Test
        #------------------------
        """id_list = [1, 2, 3, 4, 5]
        role_list = ["werewolf", "villager", "seer", "witch", "hunter"]
        channel = bot.get_channel(1195494438810701916)
        game = Game(GarooClient(bot, channel), id_list, role_list, turn_count=0)
        game.test()"""
        #------------------------
        channel = bot.get_channel(1195494438810701916)
        client = GarooClient(bot, channel)
        # Rag : 576435921390403623
        # Arckedo : 508005660516941824
        # Armoniake : 663518185068429332
        interface = GarooChoose(["Action A", "Action B"], [576435921390403623, 663518185068429332])
        results = client.send_interface("test", interface)
        print("Resultats :", results)


def run_bot(token: str) -> None:
    bot.run(token)