from bot.bot import run_bot
import nest_asyncio

BOT_TOKEN = "MTE5NDk1Njc5NDgxMjk2NDg3NA.GCPSAS.E3H2t7u5TTwt_rFgaTdQ3lQpsrM-Ip4d7fy1zg"

# Rend les appels imbriqués de "run_until_complete()" possibles
# Merci stackoverflow
nest_asyncio.apply()

run_bot(BOT_TOKEN)
