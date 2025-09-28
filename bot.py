import os
import pandas as pd
from rapidfuzz import process
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

# Load responses from CSV
def load_responses():
    df = pd.read_csv("responses.csv")
    responses = {}
    for _, row in df.iterrows():
        keyword = str(row["keyword"]).strip().lower()
        response = str(row["response"]).strip()
        responses[keyword] = response
    return responses

responses = load_responses()

# /start command
def start(update, context):
    update.message.reply_text("✅ Bot is working! Send me a message.")

# Handle messages
def handle_message(update, context):
    text = update.message.text.lower()
    match, score, _ = process.extractOne(text, responses.keys())
    if score > 60:  # fuzzy match threshold
        update.message.reply_text(responses[match])
    else:
        update.message.reply_text("Sorry, I don’t understand 🤔")

# Main
def main():
    TOKEN = os.getenv("BOT_TOKEN")  # Railway environment variable
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))

    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
