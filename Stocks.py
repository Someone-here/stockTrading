import trader

stk = "BTCINR"
trader.setup(stk)
out = trader.quote()
bought = True
Buy_price = out
sell_price = out
profit = out * -1
print(f"current price: {out}")

while True:
    if trader.quote() < out:
        out = trader.quote()
        if bought and out > Buy_price:
            print("sell", out, profit)
            sell_price = out
            profit = profit + sell_price
            bought = False
        else:
            print("value: "+str(out), "Stock held: " + str(bought),
                  "profit: "+str(profit), "GOING DOWN")
    elif trader.quote() > out:
        out = trader.quote()
        if not bought and out < sell_price:
            print("buy", out, profit)
            Buy_price = out
            profit = profit - Buy_price
            bought = True
        else:
            print("value: "+str(out), "Stock held: " + str(bought),
                  "profit: "+str(profit), "GOING UP")
