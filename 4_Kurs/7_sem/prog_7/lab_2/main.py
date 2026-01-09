import os
import requests
from flask import Flask, request, jsonify
from multiprocessing import Pool

# Инициализация Flask-приложения (соответствует спецификации WSGI)
app = Flask(__name__)

# Настройки внешнего API (OpenWeatherMap)
API_KEY = ""
BASE_URL = "https://api.openweathermap.org/data/2.5/weather"

# Хранилище для сервиса истории запросов (в памяти приложения)
history_db = []

def fetch_weather_worker(city):
    """
    Воркер для реализации многопроцессности.
    Выполняет запрос к погодному API в отдельном процессе, чтобы 
    избежать блокировки основного потока выполнения.
    """
    params = {
        'q': city,
        'appid': API_KEY,
        'units': 'metric',
        'lang': 'ru'
    }
    try:
        response = requests.get(BASE_URL, params=params, timeout=5)
        return response.json()
    except Exception as e:
        return {"error": str(e)}

@app.route('/weather', methods=['GET'])
def get_weather():
    """
    Сервис получения погоды.
    Использует многопроцессность для обработки запроса.
    """
    city = request.args.get('city')
    if not city:
        return jsonify({"error": "Не указан город"}), 400

    # Создаем пул процессов для параллельного выполнения задачи
    with Pool(processes=2) as pool:
        results = pool.map(fetch_weather_worker, [city])
    
    weather_data = results[0]
    
    # Сохраняем данные в историю, если город найден успешно
    if weather_data.get("cod") == 200:
        history_db.append({
            "city": city, 
            "temp": weather_data['main']['temp'],
            "description": weather_data['weather'][0]['description']
        })
    
    return jsonify(weather_data)

@app.route('/recommend', methods=['POST'])
def recommend():
    """
    Сервис рекомендаций.
    Принимает JSON с данными о погоде и возвращает совет.
    """
    data = request.json
    if not data:
        return jsonify({"error": "Ожидаются данные в формате JSON"}), 400

    temp = data.get('main', {}).get('temp', 20)
    weather_main = data.get('weather', [{}])[0].get('main', '').lower()

    # Логика подбора рекомендаций
    if "rain" in weather_main:
        advice = "Сегодня ожидается дождь, возьмите зонт!"
    elif temp < 10:
        advice = "На улице прохладно, наденьте куртку."
    else:
        advice = "Погода отличная, одевайтесь по вкусу."

    return jsonify({"recommendation": advice})

@app.route('/history', methods=['GET'])
def get_history():
    """
    Сервис истории запросов.
    Предоставляет статистику и список последних городов.
    """
    return jsonify({
        "total_queries": len(history_db),
        "last_10_queries": history_db[-10:]
    })

if __name__ == '__main__':
    # Запуск сервера на порту 8080 (стандарт для Yandex Cloud)
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)