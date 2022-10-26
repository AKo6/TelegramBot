import requests, json
from config import keys

class ConvertionException(Exception):
    pass

class BotConverter:
    @staticmethod
    def get_price(quote: str, base: str, amount: str):

        if quote == base:
            raise ConvertionException(f'Нельзя конвертировать одинаковые валюты {base}.')

        try:
            quote_ticker = keys[quote]
        except KeyError:
            raise ConvertionException(f'Не могу обработать валюту {quote}.\n'\
                                      'Возможно вы ввели название валюты с маленькой буквы.')

        try:
            base_ticker = keys[base]
        except KeyError:
            raise ConvertionException(f'Не могу обработать валюту {base}.\n'\
                                      'Возможно вы ввели название валюты с маленькой буквы.')

        try:
            amount = float(amount)
        except ValueError:
            raise ConvertionException(f'Не могу обработать количество {amount}.')

        r = requests.get(f'https://min-api.cryptocompare.com/data/price?fsym={quote_ticker}&tsyms={base_ticker}')
        total_base = json.loads(r.content)[keys[base]] * amount

        return total_base