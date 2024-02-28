print("Pour stopper le programme fermez la console ou effectuez Ctrl+C")

from bot.bot import run_bot
import nest_asyncio
import json

# L'utilité de ce fichier est de pouvoir importer des fichiers
# relativement à la racine (le dossier "code")
#
# Par exemple, importer "bot.interactions.GarooClient" devient
# possible dans le fichier "roles/role.py"

# Rend les appels imbriqués de "run_until_complete()" possibles
# Merci Stack Overflow
nest_asyncio.apply()

try:
    # Tente de récupérer le token depuis un fichier de configuration
    with open("./code/config.json", "r") as f:
        BOT_TOKEN = json.load(f)["BOT_TOKEN"]
    print("Token chargé depuis le fichier config.json")

except (FileNotFoundError, KeyError):
    # Si le fichier n'existe pas ou que le token n'est pas dans le fichier
    BOT_TOKEN = input("Token du bot : ")

finally:
    run_bot(BOT_TOKEN)
