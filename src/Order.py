import APIInterface

orders_by_symbol = {}

buy_threshold = 33.3
sell_threshold = 66.6
middle_value = 50.0
quote_per_trade = 0.10 # means 10 % of the complete account money
stoppLoss_trigger = 0.01 # means the stop loss triggers by 1% downwards

def decideAndPerformAction(price, rsi_values, symbol):
    if symbol not in orders_by_symbol:
        orders_by_symbol[symbol] = {}
        orders_by_symbol[symbol]["buy"] = []
        orders_by_symbol[symbol]["sell"] = []
        orders_by_symbol[symbol]["stoploss"] = []
    
    # decide for an action
    buy_signal = decideBuySignal(rsi_values)
    sell_signal = decideSellSignal(rsi_values)
    if (buy_signal == 1) and (sell_signal == 0):
        # buy
        current_available_money = getAccountMoney()
        setBuyOrder(symbol, price, current_available_money)
    elif (buy_signal == 0) and (sell_signal == 1):
        # sell
        setSellOrder(symbol)
    else:
        # no signal, nothing required
        pass
    
    rebalance(symbol, price)

    safeCurrentState()

def decideBuySignal(rsi_values):
    if len(rsi_values) < 2:
        # don't buy or sell
        return 0
    elif rsi_values[-2] < buy_threshold and rsi_values[-1] > buy_threshold:
        # buy
        return 1
    else:
        return 0
    
def decideSellSignal(rsi_values):
    if len(rsi_values) < 2:
        return 0
    elif rsi_values[-2] > sell_threshold and rsi_values[-1] < sell_threshold:
        # goal was reached --> sell
        return 1
    else:
        # goal wasn't reached, but a sell signal isn't given
        return 0
    
def rebalance(symbol, price):
    # look if the trade is in profit and high up the StoppLoss or if the stop loss was triggered and delete all remaining orders
    # if the price is 2% higher then the entry price pull back the Stopploss and set it to brake even(a little above(0.5%))
    # delete all other stopploss orders
    pass

def calculateStopLoss(price):
    return price - (price * stoppLoss_trigger)

def setBuyOrder(symbol, price, money):
    # check if a buy order is already set, if yes, then pass
    if not orders_by_symbol[symbol]["buy"]:
        return
    
    # calculate the volume
    volume = calculateVolume(price, money)
    if volume == 0:
        # not enough money in the account
        return
    stopLoss = calculateStopLoss(price)
    buy_order_data = APIInterface.setBuyOrder(symbol, volume)
    stop_loss_order_data = setStoplossOrder(symbol, volume, stopLoss)

    # safe the orders to the dictionary
    orders_by_symbol[symbol]["buy"].append(buy_order_data)
    orders_by_symbol[symbol]["stoploss"].append(stop_loss_order_data)

def setSellOrder(symbol):
    # check if a position is open, if no pass
    deleteStoplossOrder(symbol)
    # call here the API interface wit all needed information
    # delete all orders of the dictionary
    pass

def getAccountMoney():
    # call API interface here and give the value back
    return APIInterface.getAvailableCash()

def deleteStoplossOrder(symbol):
    # delete the Stoploss order of the symbol
    pass

def setStoplossOrder(symbol, volume, stopLoss):
    return APIInterface.setStopLossOrder(symbol, volume, stopLoss)

def calculateVolume(price, money):
    # calculate the volume (in stocks by using the price and available money)
    circa_amount_off_stocks = int((money*quote_per_trade) / price[-1].close)
    return circa_amount_off_stocks

def loadFromJson():
    # load from json file the current trades
    pass

def safeCurrentState():
    # safe the dictionary localy in json file
    pass 