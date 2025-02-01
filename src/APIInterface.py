import requests
import Authentication
from urllib.parse import quote

#api = REST(Authentication.APCA_API_KEY_ID, Authentication.APCA_API_SECRET_KEY, Authentication.BASE_URL)
headers = {
    "accept": "application/json",
    "APCA-API-KEY-ID": Authentication.APCA_API_KEY_ID,
    "APCA-API-SECRET-KEY": Authentication.APCA_API_SECRET_KEY
}


def getHistoricalData(symbol, timeframe, limit, start_date, sort):
    '''
    This function gives back the requested historical bar data of the symbol in the given timeframe and a limit, aswell as a start date in a descending order 
    '''
    url = Authentication.BASE_URL_MARKETS + "/bars?symbols=" + symbol + "&timeframe=" + timeframe + "&start="+ quote(start_date) +"&limit=" + str(limit)+ "&sort=" + sort
    print(url)
    historical_Data = requests.get(url, headers=headers)
    return historical_Data.json()
