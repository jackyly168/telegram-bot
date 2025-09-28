import csv
from rapidfuzz import fuzz
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

CSV_FILE = "responses.csv"
FUZZY_THRESHOLD = 80  # 0-100, higher = stricter match

# Load responses from CSV
def load_responses():
    responses = {}
    try:
        with open(CSV_FILE, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                keyword = row["keyword"].strip().lower()
                response = row["response"].strip()
                responses[keyword] = response
    except FileNotFoundError:
        print(f"⚠️ Warning: {CSV_FILE} not found.")
    except KeyError:
        print(f"⚠️ Warning: CSV headers must be exactly 'keyword,response'")
    return responses

# /start command
def start(update, context):
    update.message.reply_text("✅ Bot is running! Type something...")

# Handle all messages with fuzzy matching
def handle_message(update, context):
    text = update.message.text.lower().strip()
    responses = load_responses()

    best_match = None
    highest_score = 0

    for keyword, response in responses.items():
        score = fuzz.partial_ratio(keyword, text)
        if score > highest_score:
            highest_score = score
            best_match = response

    if highest_score >= FUZZY_THRESHOLD:
        update.message.reply_text(best_match)
    else:
        update.message.reply_text("❓ Sorry, I don’t understand.")

# Main function
def main():
    TOKEN = "8251217158:AAGCcdrKtqkdf7i_7YbKuljXsTRdTzZWjWY"  
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))

    print("Bot is running... (fuzzy match enabled, supports English + Khmer)")
    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
