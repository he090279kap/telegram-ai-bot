import logging
import openai
import config
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext

# Логирование
logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)

# Функция для общения с OpenAI
def chat_with_ai(prompt):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}]
        )
        return response["choices"][0]["message"]["content"]
    except Exception as e:
        return f"Ошибка: {e}"

# Обработчик команды /start
async def start(update: Update, context: CallbackContext) -> None:
    await update.message.reply_text("🤖 Привет! Я AI-бот. Напиши мне что-нибудь!")

# Обработчик текстовых сообщений
async def handle_message(update: Update, context: CallbackContext) -> None:
    user_text = update.message.text
    ai_response = chat_with_ai(user_text)
    await update.message.reply_text(ai_response)

# Основная функция запуска бота
def main():
    app = Application.builder().token(config.TELEGRAM_BOT_TOKEN).build()
    
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("🤖 Бот запущен!")
    app.run_polling()

if __name__ == "__main__":
    main()
