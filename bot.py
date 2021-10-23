import websocket, json, pprint, talib, numpy

SOCKET = "wss://stream.binance.com:9443/ws/ethusdt@kline_1m"


RSI_PERIOD = 14 #! this 14 means the indicator is calculated using the last 14 candles or last 14 bars on the price chart(Default is 14). 
RSI_OVERBOUGHT = 70 #! this 70 means if the rsi calculation's result is 70, it defines its overbought. so its time to Sell!! (Default is 70)
RSI_OVERSOLD = 30 #! this 30 means if the rsi calculation's result is 30, it defines its oversold. so its time to Buy!! (Default is 30)
TRADE_SYMBOL = "ETHUSD" #! this ETHUSD means which coin or stock that will trade (Symbols from binance) (Default is ETHUSD but can be any coin)
TRADE_QUANTITY = 0.001 #! this 0.010 means how many piece to buy (etc: 0.001 eth = 38,63334 TL)
closes = []
in_position = False

def on_open(ws):
    print("opened connection")

def on_close(ws):
    print("closed connection")

def on_message(ws, message):
    global closes
    
    print('received message')
    json_message = json.loads(message)
    pprint.pprint(json_message)

    candle = json_message['k']

    is_candle_closed = candle['x']
    close = candle['c']

    if is_candle_closed:
        print("candle closed at {}".format(close))
        closes.append(float(close))
        print("closes")
        print(closes)

        if len(closes) > RSI_PERIOD:
            np_closes = numpy.array(closes)
            rsi = talib.RSI(np_closes, RSI_PERIOD)
            print("all rsis calculated so far")
            print(rsi)
            last_rsi = rsi[-1]
            print("the current rsi is{}".format(last_rsi))

            if last_rsi > RSI_OVERBOUGHT:
                if in_position:
                    print("Its time so SELL!! SELL!! SELL!!")
                    #! Put binance sell logic here
                else:
                    print("It is OVERBOUGHT, but we dont own any, nothing to do")

            if last_rsi < RSI_OVERSOLD:
                if in_position:
                    print("It is OVERSOLD, but you already own it, noting to do")
                else:
                    print("Oversold!! Its time to BUY!! BUY!! BUY!!")
                    #! Put binance buy logic here
    

ws = websocket.WebSocketApp(SOCKET, on_open=on_open, on_close=on_close, on_message=on_message)
ws.run_forever()