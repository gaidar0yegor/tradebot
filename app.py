
from flask import Flask, render_template, request
from flask_socketio import SocketIO
import threading
from bot_script import run_trading_bot  # Импортируем функцию бота из файла bot_script.py

# Инициализация Flask и SocketIO
app = Flask(__name__)
socketio = SocketIO(app)

# Хранилище потоков для ботов
bot_threads = []

# Маршрут для главной страницы с формой
@app.route('/')
def index():
    return render_template('index.html')

# Маршрут для запуска бота с параметрами формы
@app.route('/start_bot', methods=['POST'])
def start_bot():
    # Получаем данные из формы
    rsi_period = request.form['rsi_period']
    trade_symbol = request.form['trade_symbol']
    trade_quantity = request.form['trade_quantity']
    budget = request.form['budget']
    stop_loss = request.form['stop_loss']
    ma1 = request.form['ma1']
    ma2 = request.form['ma2']
    ma3 = request.form['ma3']

    # Создаём и запускаем бота в новом потоке
    bot_thread = threading.Thread(target=run_trading_bot, args=(rsi_period, trade_symbol, trade_quantity, budget, stop_loss, ma1, ma2, ma3, socketio.emit))
    bot_thread.start()

    # Добавляем поток в список запущенных ботов
    bot_threads.append(bot_thread)

    return render_template('chart.html', trade_symbol=trade_symbol)

# Обработка подключения клиента через WebSocket
@socketio.on('connect')
def handle_connect():
    print("Клиент подключен")

# Запуск Flask-приложения с поддержкой SocketIO
if __name__ == '__main__':
    socketio.run(app, debug=True)
