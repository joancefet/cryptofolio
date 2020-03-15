from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
from cryptocurrencies.models import CryptoCurrency
from requests.exceptions import RequestException
from requests import Request, Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import json


class Command(BaseCommand):
    help = 'Fetch prices from coinmarketcap'

    def handle(self, *args, **options):

        url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'

        headers = {
          'Accepts': 'application/json',
          'X-CMC_PRO_API_KEY': settings.COINBASE_API_KEY,
        }

        session = Session()
        session.headers.update(headers)
        
        parameters = {
          'convert': 'EUR',
        }
        
        try:
            response = session.get(url, params=parameters)
            data = json.loads(response.text)
            
            for d in data['data']:
                crypto_currency = CryptoCurrency.objects.filter(name=d['name'].lower()).first()

                if crypto_currency:
                    price = d['quote']['EUR']['price']
                    crypto_currency.price = price
                    crypto_currency.save()
                    self.stdout.write(self.style.SUCCESS('Successfully fetch price for "%s"' % crypto_currency.name))
        except (ConnectionError, Timeout, TooManyRedirects) as e:
            print(e)