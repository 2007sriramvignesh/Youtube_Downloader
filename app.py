import requests
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# === CONFIG ===
TELEGRAM_TOKEN = "8485501826:AAGrvyqyej7dz_JEEyByMORmPYAxsCO5BYM"
OPENROUTER_API_KEY = "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"

# === LLM Function ===
def ask_llm(prompt):
    url = "https://openrouter.ai/api/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json",
        "HTTP-Referer": "http://localhost",   # required by OpenRouter
        "X-Title": "KrishiBot"
    }
    payload = {
        "model": "mistralai/mistral-7b-instruct",
        "messages": [
            {
                "role": "system",
                "content": (
                    "நீங்கள் ஒரு டிஜிட்டல் விவசாய அலுவலர். "
                    "தமிழில் மட்டும் பேசவும். "
                    "எப்போதும் வணக்கம் (உதாரணம்: 'வணக்கம்! எப்படி இருக்கிறீர்கள்?') "
                    "போன்ற தமிழ் வாழ்த்துகளுடன் தொடங்கவும். "
                    "பதில் எளிமையாகவும் சுருக்கமாகவும், விவசாயிக்கு புரியும் பாணியில் இருக்க வேண்டும்."
                )
            },
            {"role": "user", "content": prompt}
        ]
    }

    response = requests.post(url, headers=headers, json=payload, timeout=30)
    data = response.json()
    return data["choices"][0]["message"]["content"].strip()


# === Telegram Handlers ===
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("നമസ്കാരം! 🌱 ഞാൻ നിങ്ങളുടെ ഡിജിറ്റൽ കൃഷി ഓഫീസർ ആണു.")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text
    await update.message.reply_text("⏳ ചിന്തിച്ചുകൊണ്ടിരിക്കുന്നു...")

    try:
        reply = ask_llm(user_text)
        if not reply:
            reply = "⚠️ ക്ഷമിക്കണം, മറുപടി ലഭിച്ചില്ല."
        await update.message.reply_text(reply)
    except Exception as e:
        await update.message.reply_text(f"⚠️ Error: {str(e)}")

# === Main ===
def main():
    app = Application.builder().token(TELEGRAM_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    print("🤖 Bot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()
