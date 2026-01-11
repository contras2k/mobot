#!/usr/bin/env python3

import os
import logging
from dotenv import load_dotenv
import telebot
from telebot import types

load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")
if not BOT_TOKEN:
    raise RuntimeError("Не найден BOT_TOKEN в .env")

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    handlers=[logging.FileHandler("bot.log"), logging.StreamHandler()]
)

bot = telebot.TeleBot(BOT_TOKEN, parse_mode="HTML")

ROLE_NAME = "Модератор"
ROLE_PROMPT = (
    "Ты — ассистент модератора. Отвечай кратко, структурированно, без жаргона. "
    "Если пользователь просит оценить текст — добавь дисклеймер 'не является окончательным вердиктом'. "
)
DISCLAIMER = (
    "⚠️ Не является окончательным вердиктом. "
    "Примите самостоятельное решение после прочтения текста."
)

def main_menu_kb() -> types.ReplyKeyboardMarkup:
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True)
    kb.row("📌 О боте", "🆘 Помощь")
    kb.row("📈 Что умею", "💬 FAQ")
    return kb

@bot.message_handler(func=lambda m: m.text in ["📌 О боте", "🆘 Помощь", "📈 Что умею", "💬 FAQ"])
def handle_buttons(message: telebot.types.Message):
    mapping = {
        "📌 О боте": send_about,
        "🆘 Помощь": send_help,
        "📈 Что умею": send_capabilities,
        "💬 FAQ": send_faq,
    }
    return mapping[message.text](message)

# Команда /start
@bot.message_handler(commands=['start'])
def send_welcome(message: telebot.types.Message):
# def send_welcome(message):
    bot.reply_to(message, "Привет! Я бот Mobot.", reply_markup=main_menu_kb())

# Команда /help
@bot.message_handler(commands=['help'])
def send_help(message: telebot.types.Message):
    response = (
        "Доступные команды:\n"
        "/start - Приветствие\n"
        "/help - Справка по командам\n"
        "/about - Информация о боте\n"
        "/capabilities - Возможности бота\n"
        "/faq - Часто задаваемые вопросы\n"
        "/ping - Проверка доступности бота"
    )
    bot.reply_to(message, response)

# Команда /about
@bot.message_handler(commands=['about'])
def send_about(message: telebot.types.Message):
    response = (
        "Я бот Mobot, созданный для помощи владельцам сайтов в премодерации отзывов.\n"
        "Моя цель - упростить процесс проверки и публикации отзывов."
    )
    bot.reply_to(message, response)

# Команда /capabilities
@bot.message_handler(commands=['capabilities'])
def send_capabilities(message: telebot.types.Message):
    response = (
        "Возможности бота:\n"
        "- Просмотр отзывов по очереди\n"
        "- Вынесение вердикта по каждому отзыву\n"
        "- Разрешение публикации отзыва\n"
        "- Удаление отзыва\n"
        "- Отправка отзыва администратору\n"
        "- Отложение отзыва в конец очереди"
    )
    bot.reply_to(message, response)

# Команда /faq
@bot.message_handler(commands=['faq'])
def send_faq(message: telebot.types.Message):
    response = (
        "Часто задаваемые вопросы:\n"
        "1. Что такое премодерация отзывов?\n"
        "   Ответ: Это процесс проверки отзывов перед публикацией.\n"
        "2. Какие действия можно предпринять с отзывом?\n"
        "   Ответ: Можно разрешить публикацию, удалить, отправить администратору или отложить.\n"
        "3. Как работает отложение отзыва?\n"
        "   Ответ: Отзыв перемещается в конец очереди для последующей обработки."
    )
    bot.reply_to(message, response)

# Команда /ping
@bot.message_handler(commands=['ping'])
def send_ping(message: telebot.types.Message):
    bot.reply_to(message, "Pong!")


def mini_analysis_template(num: str) -> str:
    return (
        f"<b>Мини-анализ сообщения {num}</b>\n"
        "1) Пригодность к публикации: [да/нет]\n"
        "2) Настроение текста: [положительный/отрицательный]\n"
        "3) Требуются действия: [да/нет]\n"
        f"{DISCLAIMER}"
    )

@bot.message_handler(content_types=["text"])
def handle_text(message: telebot.types.Message):
    text = (message.text or "").strip()
    if text.lower().startswith(("анализ", "разбор")):
        parts = text.split()
        if len(parts) >= 2:
            num = parts[1]
            bot.reply_to(message, mini_analysis_template(num))
            return
        else:
            bot.reply_to(message, "Укажите номер сообщения для анализа.")
            return

if __name__ == "__main__":
    print("Bot is running...")
    bot.infinity_polling(timeout=10, long_polling_timeout=5)
