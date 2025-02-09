import DataProcessor
import RSI
import pytz

symbol_list = ['AAPL']
               #, 'CRM', 'PLTR', 'GOOG', 'MU', 'NU', 'VST', 'PYPL', 'VRT', 'MRVL', 'APP', 'MDB']

def init():
    for symbol in symbol_list:
        DataProcessor.initList(symbol)

def mainFunction():
    for symbol in symbol_list:
        # get data from API
        DataProcessor.actualyzeList(symbol)
        values = DataProcessor.getData(symbol)
        # calculate RSI values(at least two and save them)
        RSI.updateRSIValues(values, symbol)
        rsi_values = RSI.getRSIValue(symbol)

# init()
# mainFunction()