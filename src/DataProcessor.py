import APIInterface
from datetime import datetime, timedelta, timezone

class BarDataPoint:
    def __init__(self, timestamp, low, high, open, close, volume):
        self.timestamp = timestamp
        self.low = low
        self.high = high
        self.open = open
        self.close = close
        self.volume = volume
    
    def updatingLow(self, low):
        if low < self.low:
            self.low = low
    
    def updatingLastTimestamp(self, timestamp):
        if timestamp > self.timestamp:
            self.timestamp = timestamp
    
    def updatingHigh(self, high):
        if high > self.high:
            self.high = high

    def updatingClose(self, close):
        self.close = close
    
    def updatingVolume(self, volume):
        self.volume += volume


symbol_data_dictionary = {}

def initList(symbol):
    '''
    initiates the list with four hour values and the last value with actual data for the given symbol
    '''
    if symbol not in symbol_data_dictionary:
        symbol_data_dictionary[symbol] = []
        four_hour_bar_list = symbol_data_dictionary[symbol]
    # old data in list
    begin_date = datetime.now(timezone.utc) - timedelta(days=30)
    begin_date = begin_date.isoformat().replace("+00:00", "Z")
    historical_data = APIInterface.getHistoricalData(symbol, '4H', limit=15, start_date=begin_date, sort="desc")
    
    for data_point in historical_data['bars'][symbol]:
        data = BarDataPoint(datetime.fromisoformat(data_point['t'].replace("Z", "+00:00")), float(data_point['l']), float(data_point['h']), float(data_point['o']), float(data_point['c']), int(data_point['v']))
        four_hour_bar_list.insert(0, data)
    
    # actual data in list
    begin_date = four_hour_bar_list[-1].timestamp + timedelta(seconds=1)
    begin_date = begin_date.isoformat().replace("+00:00", "Z")
    actual_data = APIInterface.getHistoricalData(symbol, '5Min', limit=1000, start_date=begin_date, sort="asc")

    if len(actual_data['bars'][symbol]) > 0:
        # add a new point to the list(with the data of the last one)
        new_entry = actual_data['bars'][symbol][0]
        point = BarDataPoint(datetime.fromisoformat(new_entry['t'].replace("Z", "+00:00")), float(new_entry['l']), float(new_entry['h']), float(new_entry['o']), float(new_entry['c']), int(new_entry['v']))
        four_hour_bar_list.append(point)
        # and actualyze it
        for data_point in actual_data['bars'][symbol][1:]:
            four_hour_bar_list[-1].updatingLow(float(data_point['l']))
            four_hour_bar_list[-1].updatingLastTimestamp(datetime.fromisoformat(data_point['t'].replace("Z", "+00:00")))
            four_hour_bar_list[-1].updatingHigh(float(data_point['h']))
            four_hour_bar_list[-1].updatingClose(float(data_point['c']))
            four_hour_bar_list[-1].updatingVolume(int(data_point['v']))

def actualyzeList(symbol):
    '''
    This function is called every 5 minutes and checks if the data for the given symbol has changed.
    If the data has changed, the symbol list will be updated. Else not.
    '''
    if symbol in symbol_data_dictionary:
        four_hour_bar_list = symbol_data_dictionary[symbol]
    else:
        raise ValueError("the list of the symbol is not initialized yet")

    begin_date = four_hour_bar_list[-1].timestamp + timedelta(seconds=1)
    begin_date = begin_date.isoformat().replace("+00:00", "Z")
    actual_data = APIInterface.getHistoricalData(symbol, '5Min', limit=1000, start_date=begin_date, sort="asc")
    # check if there is any new data
    if symbol in actual_data['bars']:
        # check if a new data point must be created
        new_time = datetime.fromisoformat(actual_data['bars'][symbol][0]['t'].replace("Z", "+00:00"))
        delta_time = new_time - four_hour_bar_list[-2].timestamp
        
        if delta_time > timedelta(hours=4):
            new_entry = actual_data['bars'][symbol][0]
            point = BarDataPoint(datetime.fromisoformat(new_entry['t'].replace("Z", "+00:00")), float(new_entry['l']), float(new_entry['h']), float(new_entry['o']), float(new_entry['c']), int(new_entry['v']))
            four_hour_bar_list.pop(0)
            four_hour_bar_list.append(point)
        else:
            data_point = actual_data['bars'][symbol][0]
            four_hour_bar_list[-1].updatingLow(float(data_point['l']))
            four_hour_bar_list[-1].updatingLastTimestamp(datetime.fromisoformat(data_point['t'].replace("Z", "+00:00")))
            four_hour_bar_list[-1].updatingHigh(float(data_point['h']))
            four_hour_bar_list[-1].updatingClose(float(data_point['c']))
            four_hour_bar_list[-1].updatingVolume(int(data_point['v']))

def getData(symbol):
    '''
    returns the data of the given symbol
    '''
    return symbol_data_dictionary[symbol]