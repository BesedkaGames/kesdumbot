import os
import telebot
from threading import Thread

import flask_support.flask_sup

from core import *

from kesly import *
from parties import *
from propreg import *
from reg import *
from spectators import *
from voting import *

if __name__ == "__main__":
    print("Попытка подключения к Telegram API...")
    try:
        bot_info = bot.get_me()
        print(f"УСПЕШНО! @{bot_info.username} (ID: {bot_info.id})")
    except Exception as e:
        print(f"НЕ УДАЛОСЬ подключиться: {e}")
        exit(1)
    
    bot.remove_webhook()
    bot.infinity_polling(timeout=60, long_polling_timeout=60)