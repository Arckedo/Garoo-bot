from bot.bot import run_bot
import nest_asyncio

# L'utilité de ce fichier est de pouvoir importer des fichiers
# relativement à la racine (le dossier "code")
#
# Par exemple, importer "bot.interactions.GarooClient" devient
# possible dans le fichier "roles/role.py"

BOT_TOKEN = "MTE5NDk1Njc5NDgxMjk2NDg3NA.GCPSAS.E3H2t7u5TTwt_rFgaTdQ3lQpsrM-Ip4d7fy1zg"

# Rend les appels imbriqués de "run_until_complete()" possibles
# Merci stackoverflow
nest_asyncio.apply()

print("Pour stopper le programme fermez la console ou effectuez Ctrl+C")
run_bot(BOT_TOKEN)
