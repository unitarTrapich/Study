from flask import Flask, render_template, request
from flask_socketio import SocketIO, emit
import requests
import threading
import time

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app, cors_allowed_origins="*")

# курсы валют
current_rates = {}

# список клиентов
subscriptions = {}

# фукнция получения курсов
def fetch_currency_rates():
    url = "https://www.cbr-xml-daily.ru/daily_json.js"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            return data.get("Valute", {})ы
        
    except Exception as e:
        print(f"Error fetching currency rates: {e}")

    return {}

# функция обновления курсов
def update_rates_periodically():
    global current_rates
    while True:
        current_rates = fetch_currency_rates()
        notify_subscribers()

        time.sleep(60)

# функция уведомлений подписчиков
def notify_subscribers():
    for client_id, subscribed_currencies in subscriptions.items():
        if subscribed_currencies:
            filtered_rates = {code: current_rates[code] for code in subscribed_currencies if code in current_rates}
            socketio.emit('update', {'rates': filtered_rates}, to=client_id)



@app.route('/')
def index():
    return render_template('index.html')



@socketio.on('connect')
def on_connect():
    client_id = request.sid
    subscriptions[client_id] = []
    emit('connected', {'id': client_id})



@socketio.on('subscribe')
def on_subscribe(data):
    client_id = request.sid
    currency_codes = data.get('currencies', [])
    subscriptions[client_id] = currency_codes
    emit('subscribed', {'currencies': currency_codes})


@socketio.on('disconnect')
def on_disconnect():
    client_id = request.sid
    subscriptions.pop(client_id, None)


if __name__ == '__main__':
    # Запуск фоновой задачи
    thread = threading.Thread(target=update_rates_periodically)
    thread.daemon = True
    thread.start()

    # Запуск сервера
    socketio.run(app, host='0.0.0.0', port=5000)
