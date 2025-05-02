from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters
import os
import psycopg2
from dotenv import load_dotenv
import logging
from watchfiles import run_process
import nest_asyncio

# Разрешаем вложение асинхронных циклов
nest_asyncio.apply()

# Загрузка переменных окружения
load_dotenv()

# Настройка логирования
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Получаем токен и настройки базы данных из .env
BOT_TOKEN = os.getenv("BOT_TOKEN")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_NAME = os.getenv("DB_NAME")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")

if not BOT_TOKEN or not all([DB_USER, DB_PASSWORD, DB_NAME, DB_HOST, DB_PORT]):
    raise ValueError("Не все переменные окружения указаны!")

# Подключение к PostgreSQL
def get_db_connection():
    return psycopg2.connect(
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
        host=DB_HOST,
        port=DB_PORT
    )

# Обработчик команды /start
async def start(update: Update, context):
    await update.message.reply_text("Привет! Я твой новый бот.")

# Обработчик текстовых сообщений
async def echo(update: Update, context):
    await update.message.reply_text(f"Ты сказал: {update.message.text}")

# Главная функция
async def main():
    application = Application.builder().token(BOT_TOKEN).build()

    # Добавление обработчиков
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))

    # Запуск бота
    await application.run_polling()

# Функция для горячей замены кода
def reload_on_change():
    import asyncio
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Бот остановлен вручную.")
        sys.exit(0)

if __name__ == "__main__":
    # Используем watchfiles для мониторинга изменений
    run_process('.', target=reload_on_change, watch_filter=lambda change, path: path.endswith('.py'))