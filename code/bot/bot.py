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


# Pas nécessaire au jeu, utile au développement
@bot.event
async def on_message(message: discord.Message):
    if message.content == "$clean":
        channel = await bot.fetch_channel(1195494438810701916)
        await message.channel.send(f"cleaning {len(channel.threads)} threads...")
        for i, thread in enumerate(channel.threads):
            await thread.delete()
            print(i + 1, "thread cleaned")
        await message.channel.send("cleaning done")


def run_bot(token: str) -> None:
    print("Démarrage du bot...")
    bot.run(token)
