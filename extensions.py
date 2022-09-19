import requests
import json
from dop import keys

class ApiException(Exception):
    pass

class CryptoConverter:

    @staticmethod
    def convert(quote: str, base: str, amount: str):
        if quote == base:
            raise ApiException(f'Невозможно перевести одинаковые валюты {base}.')

        try:
            quote_ticker = keys[quote]
        except KeyError:
            raise ApiException(f'Не удалось обработать валюту {quote}.')

        try:
            base_ticker = keys[base]
        except KeyError:
            raise ApiException(f'Не удалось обработать валюту {base}.')

        try:
            amount_f = float(amount)
        except ValueError:
            raise ApiException(f'Не удалось обработать количество {amount}.')

        return CryptoConverter.getPrice(quote_ticker, base_ticker, amount_f)

    @staticmethod
    def getPrice(quote_ticker:str, base_ticker:str, amount: float):
        r = requests.get(f'https://min-api.cryptocompare.com/data/price?fsym={quote_ticker}&tsyms={base_ticker}')
        return json.loads(r.content)[base_ticker] * amount
