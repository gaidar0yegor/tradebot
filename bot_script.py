
import websocket, json, talib, numpy
import config
from binance.client import Client
from binance.enums import *
from datetime import datetime

SOCKET = "wss://stream.binance.com:9443/ws/ethusdt@kline_1m"

RSI_PERIOD = 6
RSI_OVERBOUGHT = 70
RSI_OVERSOLD = 40
TRADE_SYMBOL = 'ETHUSD'
TRADE_QUANTITY = 0.01
BUDGET = 100
FRAIS = 0.1
STOP_LOSS = 0.005
MA1 = 2
MA2 = 3
MA3 = 4

# Определение имени файла
now = datetime.now()  # текущая дата и время
START_TIME = now.strftime("%d%m%Y%H%M")
FILE_NAME = TRADE_SYMBOL + START_TIME + "stoplossrsiMA" + '.txt'

# Создание файла
file = open(FILE_NAME, "w")
file.write("START_TIME = " + START_TIME + "\n")
file.write("TRADE_SYMBOL = " + TRADE_SYMBOL + "\n")
file.close()

# Функция добавления строк в файл
def add_file(line):
    try:
        file = open(FILE_NAME, "a")
        file.write(str(line) + "\n")
        file.close()
    except Exception as e:
        print("Произошла ошибка - {}".format(e))
        return True

    return True

# Функция баланса
def balance(negpos, current_bal, current_price, t_quantity):
    try:
        cb = "Текущий баланс -" + str(current_bal)
        print(cb)
        add_file(cb)
        cp = "Текущая цена - " + str(current_price)
        print(cp)
        add_file(cp)
        transac_amount = current_price * t_quantity
        tta = "Сумма транзакции -" + str(transac_amount)
        print(tta)
        add_file(tta)
        current_bal = current_bal + negpos * transac_amount
        ccb = "Текущий баланс" + str(current_bal)
        print(ccb)
        add_file(ccb)
        bbalance.append(float(current_bal))
    except Exception as e:
        print("Произошла ошибка - {}".format(e))
        return True
    return bbalance

# Добавление начальных значений
add_file(f'{RSI_PERIOD = }')
add_file(f'{RSI_OVERBOUGHT = }')
add_file(f'{RSI_OVERSOLD = }')
add_file(f'{TRADE_QUANTITY = }')
add_file(f'{BUDGET = }')
add_file(f'{FRAIS = }')
add_file(f'{STOP_LOSS = }')
add_file(f'{MA1 = }')
add_file(f'{MA2 = }')
add_file(f'{MA3 = }')

closes = []
stploss = [0]
in_position = False
bbalance = [100]
client = Client(config.API_KEY, config.API_SECRET, tld='us')

# Функция для установки стоп-лосса
def stoploss(current_price, STOP_LOSS):
    try:
        if in_position and closes[-1] > closes[-2]:
            stplos = current_price - current_price * STOP_LOSS
            if stploss[-1] < stplos:
                stploss.append(float(stplos))
                print("Текущая цена для стоп-лосса -", current_price)
                print("Процент стоп-лосса -", STOP_LOSS)
                stplos = current_price - current_price * STOP_LOSS
                print("Текущий стоп-лосс - ", stplos)
                print("Текущий стоп-лосс из массива -", stploss[-1])
        else:
            print("СТОП-ЛОСС ОСТАЛСЯ ПРЕЖНИМ", stploss[-1])
    except Exception as e:
        print("Произошла ошибка - {}".format(e))
        return True
    return

# Функция для отправки ордера
def order(side, quantity, symbol, order_type=ORDER_TYPE_MARKET):
    try:
        print("Отправляем ордер")
        # Пример отправки ордера через Binance API (закомментировано)
        # order = client.create_order(symbol=symbol, side=side, type=order_type, quantity=quantity)

        print(symbol, "---", side, "---", order_type, "-----", quantity)
    except Exception as e:
        print("Произошла ошибка - {}".format(e))
        return True

    return True

# Функция обработки открытия WebSocket
def on_open(ws):
    print('Соединение открыто')

# Функция обработки закрытия WebSocket
def on_close(ws):
    print('Соединение закрыто')

# Функция обработки входящего сообщения от WebSocket
def on_message(ws, message):
    global closes, in_position, bbalance

    json_message = json.loads(message)
    candle = json_message['k']
    is_candle_closed = candle['x']
    close = candle['c']

    if is_candle_closed:
        print("Свеча закрылась на уровне {}".format(close))
        closes.append(float(close))
        add_file(f"Свеча закрылась на уровне {closes[-1]}")
        stoploss(closes[-1], STOP_LOSS)

        if len(closes) > MA3:
            np_closes = numpy.array(closes)
            rsi = talib.RSI(np_closes, RSI_PERIOD)
            print("Рассчитаны все значения RSI")
            print("RSI - ", rsi)

            mma1 = talib.MA(np_closes, MA1, 0)
            mma2 = talib.MA(np_closes, MA2, 0)
            mma3 = talib.MA(np_closes, MA3, 0)

            last_rsi = rsi[-1]
            last_ma1 = mma1[-1]
            last_ma3 = mma3[-1]
            
            if closes[-1] < stploss[-1] or (last_ma1 < last_ma3 and mma3[-1] < mma3[-2]):
                if in_position:
                    print("Перекуплено! Продаем!")
                    balance(+1, bbalance[-1], closes[-1], TRADE_QUANTITY)
                    order(SIDE_SELL, TRADE_QUANTITY, TRADE_SYMBOL)
                    in_position = False

ws = websocket.WebSocketApp(SOCKET, on_open=on_open, on_close=on_close, on_message=on_message)
ws.run_forever()
