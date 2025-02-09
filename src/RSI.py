import statistics

rsi_values = {}
indicator_constant = 14
max_length = 255

def updateRSIValues(values, symbol):
    if symbol not in rsi_values:
        rsi_values[symbol] = []
        # first only two values can be calculated
        rsi_values[symbol].append(calculateRSIValue(values[len(values) - 14 - 1:-1]))
        rsi_values[symbol].append(calculateRSIValue(values[len(values)- 14:]))
        return
    # the next values can be added to the list
    rsi_values[symbol].append(calculateRSIValue(values[len(values) - indicator_constant:]))
    if len(rsi_values) > max_length:
        rsi_values.pop(0)

def calculateRSIValue(values):
    losses = []
    gains = []
    for entry in values:
        if entry.close - entry.open < 0:
            losses.append(entry.open - entry.close)
        else:
            gains.append(entry.close - entry.open)

    average_loss = statistics.mean(losses)
    average_gain = statistics.mean(gains)

    rsi_value = 100 - ( 100 / (1+(average_gain/average_loss)))
    return rsi_value

def getRSIValue(symbol):
    """
    retunrs the RSI Values of the symbol
    """
    return rsi_values[symbol] if symbol in rsi_values else None
