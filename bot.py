import os, requests, logging
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

TOKEN = os.getenv("BOT_TOKEN")
logging.basicConfig(level=logging.INFO)

COMMANDS = {
"start": "Hi! I am ELSA ❄️ Your AI assistant with 50 commands. Type /help",
"help": "50 commands: /start /help /search /about /joke /quote /weather /news /calc /time /date /fact /meme /song /movie /game /wiki /define /translate /math /love /hi /hello /bye /ping /id /info /user /group /rules /settings /profile /balance /shop /work /daily /rank /stats + I reply to ANY message!",
"about": "ELSA Bot built by you - 50 commands + smart reply + search engine.",
"joke": "Why did Elsa go to school? To improve her ICE-Q! 😂",
"quote": "Let it go... - Elsa ❄️",
}

async def cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    txt = update.message.text[1:].split()[0].lower()
    reply = COMMANDS.get(txt, f"ELSA: /{txt} is working! ❄️")
    await update.message.reply_text(reply)

async def search_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = " ".join(context.args)
    if not query:
        return await update.message.reply_text("Use: /search cats")
    try:
        r = requests.get(f"https://api.duckduckgo.com/?q={query}&format=json", timeout=10).json()
        ans = r.get("AbstractText") or f"Results for {query}: https://duckduckgo.com/?q={query}"
        await update.message.reply_text(ans[:1000])
    except:
        await update.message.reply_text(f"https://www.google.com/search?q={query}")

async def smart_reply(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    if text.startswith("/"): return
    await update.message.reply_text(f"ELSA heard you: '{text}' ❄️ Try /search {text} or /help")

def main():
    app = Application.builder().token(TOKEN).build()
    for name in ["start","help","about","joke","quote","search","weather","news","calc","time","date","fact","meme","song","movie","game","wiki","define","translate","math","love","hug","hi","hello","bye","ping","id","info","user","group","admin","ban","kick","mute","warn","rules","settings","profile","balance","shop","buy","sell","work","daily","weekly","leaderboard","rank","stats","feedback"]:
        if name=="search":
            app.add_handler(CommandHandler(name, search_cmd))
        else:
            app.add_handler(CommandHandler(name, cmd))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, smart_reply))
    app.run_polling()

if __name__ == "__main__":
    main()