import APIInterface
from datetime import datetime, timedelta, timezone

four_hour_bar_list = []

def initList(symbol):
    begin_date = datetime.now(timezone.utc) - timedelta(days=30)
    begin_date = begin_date.isoformat().replace("+00:00", "Z")
    historical_data = APIInterface.getHistoricalData(symbol, '4H', limit=15, start_date=begin_date)
    print(historical_data)
    # for data_bit in historical_data:
    #     data_bit.__dict__["_raw"]
    
initList("AAPL")