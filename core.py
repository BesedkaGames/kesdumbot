import os
import telebot
from typing import Any
from dataclasses import dataclass, field

TOKEN = os.environ.get("BOT_TOKEN")
if TOKEN == None:
    try:
        TOKEN = open("secret_token.txt").read()
    except:
        TOKEN = "[CORE] Токен не найден"
        print(TOKEN)
bot = telebot.TeleBot(TOKEN)