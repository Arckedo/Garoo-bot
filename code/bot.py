import discord
from main_game import Game
from interactions import GarooClient


# Préparation des "intents" (permissions du bot au niveau API)
intents = discord.Intents.default()
intents.message_content = True

# Création de l'objet bot
bot = discord.Bot(intents=intents)

# Les serveurs discord dans lesquels le bot créera des slash commands
bot.debug_guilds = [1194944354859614339]

# Chargement de l'extension ("cog") contenant les commandes
bot.load_extension("commands")


# Test
#------------------------
id_list = [1, 2, 3, 4, 5]
role_list = ["werewolf", "villager", "seer", "witch", "hunter"]
channel = bot.get_channel(1195494438810701916)
game = Game(GarooClient(bot, channel), id_list, role_list, turn_count=0)
#------------------------


# Ces fonctions sont des évènements gérés par pycord
@bot.event
async def on_ready():
    print(f"We have logged in as {bot.user} in {len(bot.guilds)} guilds")


@bot.event
async def on_message(message: discord.Message):
    if message.author.id == bot.user.id:
        return

    if message.content == "$test":
        game.test_send()


def run_bot(token: str) -> None:
    bot.run(token)