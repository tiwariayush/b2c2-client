import logging
import uuid

from src.constants import (B2C2_BALANCE_ENDPOINT, B2C2_CURRENCY_ENDPOINT,
                           B2C2_INSTRUMENTS_ENDPOINT,
                           B2C2_REQUEST_FOR_QUOTE_ENDPOINT,
                           B2C2_TRADE_ENDPOINT)
from utils.http_client import HttpClientConnection
from utils.validators import (check_quote_still_valid,
                              validate_minimum_trade_size,
                              validate_price_precision,
                              validate_quantity_precision)

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


class BaseCommand:
    def __init__(self, api_token, base_url, max_retries, timeout):
        self.base_url = base_url
        self.api_token = api_token
        self.max_retries = max_retries
        self.timeout = timeout
        self._connection = HttpClientConnection(api_token=api_token,
                                                base_url=base_url,
                                                max_retries=max_retries,
                                                timeout=timeout)

    def _validate_size_and_precision(self, instrument, quantity, price=None):
        currencies = instrument.split('.')[0]
        to_currency = self.get_currency_info(currencies[3:])

        validate_quantity_precision(to_currency, instrument, quantity)
        validate_minimum_trade_size(to_currency, quantity)
        if price:
            validate_price_precision(price)

    def get_currency_info(self, currency_code):
        """
        Takes the 3 letter of a currency and returns its info
        """
        currencies_info = self.get_supported_currencies()
        if currency_code not in currencies_info:
            logger.error('The currency code provided is not valid')
            return {}
        return currencies_info[currency_code]

    def get_supported_currencies(self):
        json_response = self._connection.get(
            relative_endpoint=B2C2_CURRENCY_ENDPOINT
        )
        return json_response

    def get_instruments(self):
        json_response = self._connection.get(
            relative_endpoint=B2C2_INSTRUMENTS_ENDPOINT
        )
        return json_response

    def show_balance(self):
        json_response = self._connection.get(
            relative_endpoint=B2C2_BALANCE_ENDPOINT
        )
        return json_response

    def request_for_quote(self, instrument, side, quantity):
        # Run validators
        self._validate_size_and_precision(instrument, quantity)
        data = {
            "instrument": instrument,
            "side": side,
            "quantity": str(quantity),
            "client_rfq_id": str(uuid.uuid4())
        }
        json_response = self._connection.post(
            relative_endpoint=B2C2_REQUEST_FOR_QUOTE_ENDPOINT,
            data=data
        )
        print("\n".join(f"{k}: {v}" for k, v in json_response.items()))
        return json_response

    def make_trade(self, instrument, side, quantity, price, valid_until):

        # Check if the quote is still valid or not
        if not check_quote_still_valid(valid_until=valid_until):
            logger.error(f"CFQ was valid till {valid_until}")
            raise RuntimeError("CFQ no longer valid.")

        # validate size and price for the order
        self._validate_size_and_precision(instrument, quantity, price)

        data = {
            "instrument": instrument,
            "side": side,
            "quantity": str(quantity),
            "client_order_id": str(uuid.uuid4()),
            "price": str(price),
            "order_type": "FOK",
            "valid_until": valid_until,
            "executing_unit": "risk-adding-strategy"
        }

        json_response = self._connection.post(
            relative_endpoint=B2C2_TRADE_ENDPOINT,
            data=data
        )

        executed_price = json_response['executed_price']
        if executed_price is None:
            print("Order rejected.")
            return

        print(f'Order info:')
        print("\n".join(f"{k}: {v}" for k, v in json_response.items()))

        balance = self.show_balance()
        print(f'Account Balance: {balance}')
