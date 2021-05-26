from requests import get
from bs4 import BeautifulSoup

crypto = True

def stock(stock, exchange):
    global crypto
    if not crypto:
        req = get(f"https://google.com/finance/quote/{stock}:{exchange}").text
    else:
        req = get(f"https://google.com/finance/quote/{stock}-{exchange}").text
    soup = BeautifulSoup(req, "html.parser")
    return float(soup.find("div", class_="fxKbKc").text.replace("$", "").replace(",", "").replace("₹", "").replace("€", ""))

stk = "BTC"
exchange = "INR"
out = stock(stk, exchange)
bought = True
Buy_price = out
going_up = True
sell_price = out
profit = out * -1
print(f"current price: {out}")

while True:
    try:
        if stock(stk, exchange) < out:
            out = stock(stk, exchange)
            if bought and out > Buy_price:
                print("sell", out)
                sell_price = out
                profit = profit + sell_price
                bought = False
            else:
                print(out, bought, profit)
        elif stock(stk, exchange) > out:
            out = stock(stk, exchange)
            if not bought and out < sell_price:
                print("buy", out)
                Buy_price = out
                profit = profit - Buy_price
                bought = True
            else:
                print(out, bought, profit)
    except:
        print(profit)
        
