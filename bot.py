from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import pandas as pd

# Load CSV
responses_df = pd.read_csv(r"C:\Users\USER\Desktop\bot\responses.csv")

# Start command
def start(update, context):
    update.message.reply_text("✅ Bot is working! Send me a message.")

# Message handler
def handle_message(update, context):
    text = update.message.text.lower()
    response = None
    for _, row in responses_df.iterrows():
        if row['input'].lower() in text:
            response = row['response']
            break
    if response:
        update.message.reply_text(response)
    else:
        update.message.reply_text("Sorry, I don’t understand 🤔")

def main():
    TOKEN = "8251217158:AAGCcdrKtqkdf7i_7YbKuljXsTRdTzZWjWY"
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))

    # Start bot
    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
