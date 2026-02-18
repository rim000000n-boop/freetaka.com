from flask import Flask, render_template, send_from_directory
from flask_socketio import SocketIO, emit
import os
import random
import time

app = Flask(__name__, static_folder='public', static_url_path='')
socketio = SocketIO(app, cors_allowed_origins="*")

# Home route
@app.route('/')
def index():
    return send_from_directory('public', 'index.html')

# Simple Crash Game Logic (Multiplier)
def multiplier_logic():
    while True:
        multiplier = 1.00
        crash_point = round(random.uniform(1.0, 5.0), 2)
        while multiplier < crash_point:
            time.sleep(0.1)
            multiplier += 0.01
            socketio.emit('multiplier_update', {'val': round(multiplier, 2)})
        socketio.emit('crashed', {'final': round(multiplier, 2)})
        time.sleep(3) # Wait before next round

if __name__ == '__main__':
    socketio.start_background_task(multiplier_logic)
    app.run(host='0.0.0.0', port=os.getenv('PORT', 5000))
