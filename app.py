
import os
import telebot
import sqlite3

from helpers.db import create_table, add_chatlog, get_recent_chatlog, delete_chatlog

from helpers.ai import lango, speak, transcribe


TOKEN = os.environ.get('TELEGRAM_TOKEN')

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    # conn = sqlite3.connect('lango.db')
    # delete_chatlog(conn, message.from_user.id)
    bot.reply_to(message, "Welcome to LanGo, your language learning friend! What do you want us to do today?\n\nWe have a few options:\n\n- Word Game: I ask you a word in French or English you tell me what it means in the other language.\n\n- Phrase Game: I ask you a phrase in French or English you tell me its equivalent in the other language.\n\n- Hotel Game: Where I assume the role of a hotel receptionist and you a guest.\n\nYou can respond with voice or chat, but I like voice better 😎 \n\nFor example if you want to play the Hotel Game, you can say 'Let's play a Hotel Game, you be a receptionist and I a guest'")

@bot.message_handler(content_types=["voice"])
def handle_voice(message):    
    conn = sqlite3.connect('lango.db')
    create_table(conn)
    file_info = bot.get_file(message.voice.file_id)
    audio_url = f"https://api.telegram.org/file/bot{TOKEN}/{file_info.file_path}"
    add_chatlog(conn, message.from_user.id, role='user', content=transcribe(audio_url))
    history = get_recent_chatlog(conn, message.from_user.id)
    chat = lango(history, message.from_user.first_name)
    add_chatlog(conn, message.from_user.id, role='assistant', content=chat.get('content'))
    bot.send_voice(message.chat.id, speak(chat.get('content')))
    bot.reply_to(message, chat.get('content'))

@bot.message_handler(func=lambda msg: True)
def echo_all(message):
    conn = sqlite3.connect('lango.db')
    create_table(conn)
    add_chatlog(conn, message.from_user.id, role='user', content=message.text)
    history = get_recent_chatlog(conn, message.from_user.id, 1000)
    chat = lango(history, message.from_user.first_name)
    add_chatlog(conn, message.from_user.id, role='assistant', content=chat.get('content'))
    bot.send_voice(message.chat.id, speak(chat.get('content')))
    bot.reply_to(message, chat.get('content'))

bot.infinity_polling()