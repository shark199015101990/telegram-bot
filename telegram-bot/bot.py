from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters
import os
import signal
import sys

# Получаем токен из переменной окружения
BOT_TOKEN = os.getenv("BOT_TOKEN")

if not BOT_TOKEN:
    raise ValueError("BOT_TOKEN не указан!")

# Обработчик команды /start
async def start(update: Update, context):
    await update.message.reply_text("Привет! Я твой новый бот. Как я могу помочь?")

# Обработчик текстовых сообщений
async def echo(update: Update, context):
    user_message = update.message.text
    await update.message.reply_text(f"Ты сказал: {user_message}")

# Обработчик команды /stop
async def stop_bot(update: Update, context):
    # Проверяем, что команда вызвана администратором (по ID)
    admin_id = 1927571708  # Замените на ваш Telegram ID
    if update.message.from_user.id == admin_id:
        await update.message.reply_text("Бот останавливается...")
        # Останавливаем бота
        os.kill(os.getpid(), signal.SIGINT)  # Отправляем сигнал остановки
    else:
        await update.message.reply_text("У вас нет прав для остановки бота.")

# Главная функция
def main():
    application = Application.builder().token(BOT_TOKEN).build()

    # Добавление обработчиков
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("stop", stop_bot))  # Добавляем обработчик /stop
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))

    # Запуск бота
    try:
        application.run_polling()
    except KeyboardInterrupt:
        print("Бот остановлен вручную.")
        sys.exit(0)

if __name__ == "__main__":
    main()