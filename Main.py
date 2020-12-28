import alpaca_trade_api as trade_api
from yahoo_fin import stock_info as market
import numpy as np
from time import sleep

positions = []
max_price = []
num = []

api = trade_api.REST("PKW3HHMX2XFXKPNHYPF3", "XBqgXGLQ5XK2Vngd8XkPVGid7WYOsDIRyks3Edyq", "https://paper-api.alpaca.markets", "v2")

tickers = market.tickers_sp500()[:100]

last_3 = np.zeros((3, 100))

for x in range(3):
    for y in range(100):
        try:
            last_3[x, y] = market.get_live_price(tickers[y])
        except Exception as ex:
            pass
    sleep(600)

while True:
    potential = np.zeros(100)
    changes1 = (last_3[1] - last_3[0]) / last_3[0]
    changes2 = (last_3[2] - last_3[1]) / last_3[1]
    for x in range(100):
        if changes1[x] > 0 and changes2[x] > 0:
            potential[x] = (changes1[x] + changes2[x])/2.0
    if tickers[np.argmax(potential)] not in positions:
        positions.append(tickers[np.argmax(potential)])
        api.submit_order(tickers[np.argmax(potential)], round(1000 / last_3[2][np.argmax(potential)]), "buy", "market", "day")
        print("Buying", round(1000 / last_3[2][np.argmax(potential)]), "of", tickers[np.argmax(potential)])
        max_price.append(last_3[2][np.argmax(potential)])
        num.append(round(1000 / last_3[2][np.argmax(potential)]))
    last_3[0] = last_3[1][:]
    last_3[1] = last_3[2][:]
    for x in range(100):
        try:
            last_3[2, x] = market.get_live_price(tickers[y])
            if tickers[x] in positions:
                if last_3[2, x] < max_price[positions.index(tickers[x])]:
                    api.submit_order(tickers[x], num[positions.index(tickers[x])], "sell", "market", "day")
                    print("Selling", num[positions.index(tickers[x])], "of", tickers[x])
                    max_price.pop(positions.index(tickers[x]))
                    num.pop(positions.index(tickers[x]))
                    positions.remove(tickers[x])
                else:
                    max_price[positions.index(tickers[x])] = last_3[2, x]
        except Exception as ex:
            pass
    sleep(600)
    for x in range(100):
        try:
            last_3[2, x] = market.get_live_price(tickers[y])
            if tickers[x] in positions:
                if last_3[2, x] < max_price[positions.index(tickers[x])]:
                    api.submit_order(tickers[x], num[positions.index(tickers[x])], "sell", "market", "day")
                    print("Selling", num[positions.index(tickers[x])], "of", tickers[x])
                    max_price.pop(positions.index(tickers[x]))
                    num.pop(positions.index(tickers[x]))
                    positions.remove(tickers[x])
                else:
                    max_price[positions.index(tickers[x])] = last_3[2, x]
        except Exception as ex:
            pass