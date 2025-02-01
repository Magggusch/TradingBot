import DataProcessor

symbol_list = ['AAPL', 'CRM', 'PLTR', 'GOOG', 'MU', 'NU', 'VST', 'PYPL', 'VRT', 'MRVL', 'APP', 'MDB']

def init():
    for symbol in symbol_list:
        DataProcessor.initList(symbol)

def mainFunction():
    for symbol in symbol_list:
        DataProcessor.actualyzeList(symbol)
        values = DataProcessor.getData(symbol)
        