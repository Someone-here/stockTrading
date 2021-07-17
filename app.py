from flask import Flask, render_template
import trader
from datetime import datetime
import threading
import math

app = Flask(__name__)
trader.setup("BTCINR")
Time = datetime.now()

curr_price = trader.quote()
THRESHOLD = 0.0/100
bought = True
Buy_price = curr_price
sell_price = curr_price
buys = []
sells = []
balance = 0
print(f"current price: {curr_price}")
investment = curr_price
data = []

def buy():
    global bought, curr_price, Buy_price, balance, sell_price
    if not bought:
        Buy_price = curr_price
        balance = balance - Buy_price
        bought = True
        print("buy", curr_price, balance)
        buys.append([math.floor(datetime.now().timestamp() * 1000), curr_price])
        

def sell():
    global bought, curr_price, Buy_price, balance, sell_price
    if bought:
        sell_price = curr_price
        balance = balance + sell_price
        bought = False
        print("sell", curr_price, balance)
        sells.append([math.floor(datetime.now().timestamp() * 1000), curr_price])

def stock_log():
    global bought, curr_price, Buy_price, balance, sell_price
    print("value: "+str(curr_price), "Stock held: " + str(bought),
                    "balance: "+str(balance))
    
def getNAV():
    global bought, curr_price, Buy_price, balance, sell_price
    if bought:
        return balance + curr_price
    else:
        return balance

def main():
    global bought, curr_price, Buy_price, balance, sell_price
    while True:
        if trader.quote() < curr_price:
            curr_price = trader.quote()
            data.append([math.floor(datetime.now().timestamp() * 1000), curr_price])
            if bought and curr_price > Buy_price and curr_price - Buy_price >= THRESHOLD * curr_price:
                sell()
            else:
                stock_log()
        elif trader.quote() > curr_price:
            curr_price = trader.quote()
            data.append([math.floor(datetime.now().timestamp() * 1000), curr_price])
            if not bought and curr_price < sell_price and sell_price - curr_price >= (THRESHOLD/2) * curr_price:
                buy()
            else:
                stock_log()
        


@app.route("/")
def home():
    print("/////", Buy_price, curr_price, sell_price)
    return render_template("chart.jinja")

@app.route("/investment")
def initial():
    global investment
    return { "initial":  investment }

@app.route("/info", methods=["POST"])
def info():
    return {
        "data": [
            {
                "type": "line",
                "values": data
            },
            {
                "type": "scatter",
                "values": buys,
                "marker": {
                    "size": 5,
                    "background-color": "#00ff00",
                }
            },
            {
                "type": "scatter",
                "values": sells,
                "marker": {
                    "size": 5,
                    "background-color": "#ff0000",
                }
            }
        ],
        "bought": bought,
        "balance": balance,
        "NAV": getNAV()
        }

@app.route("/zing")
def zing():
    return render_template("zing.jinja")

@app.route("/buy", methods = ["POST"])
def buy_req():
    buy()
    return { "bought": bought }

@app.route("/sell", methods = ["POST"])
def sell_req():
    sell()
    return { "bought": bought }

kwargs = {'host': '127.0.0.1', 'port': 5000, 'threaded': True, 'use_reloader': False, 'debug': True}

flaskThread = threading.Thread(target=app.run, daemon=True, kwargs=kwargs).start()
main()
