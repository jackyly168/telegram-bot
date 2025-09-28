import os
import pandas as pd
from rapidfuzz import fuzz
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler, filters

# Load responses
responses_df = pd.read_csv("responses.csv")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("✅ Bot is working! Send me a message.")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.lower()
    found = False
    for _, row in responses_df.iterrows():
        keyword = str(row["keyword"]).lower()
        if fuzz.ratio(text, keyword) > 80:
            await update.message.reply_text(row["response"])
            found = True
            break
    if not found:
        await update.message.reply_text("Sorry, I don’t understand 🤔")

if __name__ == "__main__":
    app = ApplicationBuilder().token(os.getenv("BOT_TOKEN")).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.run_polling()
