"""
Este módulo implementa un servidor Flask para el juego NotCoin, manejando las interacciones
con un bot de Telegram y sirviendo una página web donde los usuarios pueden jugar.
"""

import os
from flask import Flask, request, jsonify, render_template
import telebot

API_TOKEN = 'HRKU-523405b4-331b-40f7-84ba-f745b8471e07'
bot = telebot.TeleBot(API_TOKEN)
app = Flask(__name__)

# Almacenamiento sencillo para las puntuaciones de los usuarios
user_scores = {}

@app.route('/')
def index():
    """Renderiza la página principal del juego."""
    return render_template('index.html')

@app.route('/update_score', methods=['POST'])
def update_score():
    """Actualiza la puntuación del usuario."""
    data = request.json
    user_id = data['user_id']
    score = data['score']
    user_scores[user_id] = score
    return jsonify(success=True)

@bot.message_handler(commands=['start', 'play'])
def send_welcome(message):
    """Maneja el comando /start y /play para iniciar el juego."""
    user_id = message.chat.id
    user_scores[user_id] = 0
    bot.reply_to(message, "¡Bienvenido al juego NotCoin! Haz clic en el enlace para jugar: [Jugar NotCoin](http://TU_DOMINIO_HEROKU/)")

@app.route('/' + API_TOKEN, methods=['POST'])
def get_message():
    """Recibe las actualizaciones del bot de Telegram."""
    bot.process_new_updates([telebot.types.Update.de_json(request.stream.read().decode("utf-8"))])
    return "¡", 200

@app.route("/webhook")
def webhook():
    """Configura el webhook para el bot de Telegram."""
    bot.remove_webhook()
    bot.set_webhook(url='https://TU_DOMINIO_HEROKU/' + API_TOKEN)
    return "¡", 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get('PORT', 5000)))
