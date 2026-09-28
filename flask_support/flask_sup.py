from flask import Flask
from threading import Thread
import os

app = Flask('')

@app.route('/')
def health_check():
    return "Бот работает", 200

def run_flask():
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port)

flask_thread = Thread(target=run_flask, daemon=True)
flask_thread.start()