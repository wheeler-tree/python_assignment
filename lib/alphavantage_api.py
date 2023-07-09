from typing import Optional
import requests


class AlphaVantageAPI:
    DEFAULT_FUNC = "TIME_SERIES_DAILY_ADJUSTED"
    DEPRECATION_LIMIT_DAYS = 14
    DEFAULT_META_DATA = "Meta Data"
    DEFAULT_SYMBOL_DATA = "2. Symbol"
    DEFAULT_DATA_KEY = "Time Series (Daily)"
    FUNC_DATA_KEY = {"TIME_SERIES_DAILY_ADJUSTED": "Time Series (Daily)"}

    def __init__(self, api_key: str, func: Optional[str] = DEFAULT_FUNC):
        self.api_key = api_key
        self.func = func
    
    def get_daily_data_json(self, symbol_code: str) -> str:
        url = f'https://www.alphavantage.co/query?function={self.func}&datatype=json&symbol={symbol_code}&outputSize=compact&apikey={self.api_key}'
        return requests.get(url)