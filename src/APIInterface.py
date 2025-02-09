import requests
import Authentication
from urllib.parse import quote
from datetime import datetime, timedelta, timezone

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

def getAvailableCash():
    url = Authentication.BASE_URL_PAPER + "/account"
    print(url)
    data = requests.get(url, headers=headers)
    return float(data.json()["cash"])

def setBuyOrder(symbol, amount):
    url = Authentication.BASE_URL_PAPER + "/orders"
    order_data = {
        "symbol": symbol,
        "qty": amount,     
        "side": "buy",
        "type": "market",  # Market Order (sofortiger Kauf)
        "time_in_force": "gtc"  # Gültig bis ausgeführt oder storniert
    }
    response = requests.post(url, json=order_data, headers=headers).json()
    response_data = {
        "id" : response["id"],
        "timestamp" : datetime.fromisoformat(response["created_at"].replace("Z", "+00:00")),
        "quantity" : amount
    }
    return response_data

def setStopLossOrder(symbol, amount, stopLoss):
    url = Authentication.BASE_URL_PAPER + "/orders"
    # Order-Daten (Stop-Loss)
    order_data = {
        "symbol": symbol,
        "qty": amount,
        "side": "sell",
        "type": "stop",        # Stop Order (wird zur Market Order, wenn der Stop-Preis erreicht ist)
        "stop_price": stopLoss,  # Wenn Apple unter 150 USD fällt, wird die Order aktiviert
        "time_in_force": "gtc" # Gültig, bis sie ausgeführt oder storniert wird
    }
    response = requests.post(url, json=order_data, headers=headers).json()
    response_data = {
        "id" : response["id"],
        "timestamp" : datetime.fromisoformat(response["created_at"].replace("Z", "+00:00")),
        "stopLoss" : stopLoss
    }
    return response_data