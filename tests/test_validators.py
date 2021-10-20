import datetime
from unittest import TestCase

from utils.validators import (check_quote_still_valid,
                              validate_minimum_trade_size,
                              validate_price_precision,
                              validate_quantity_precision)


class TestValidators(TestCase):
    def test_validate_quantity_precision(self):
        to_currency = {
            "stable_coin": False,
            "is_crypto": False,
            "currency_type": "fiat",
            "readable_name": "",
            "long_only": False,
            "minimum_trade_size": 0.01
        }
        quantity = '4.11112'
        instrument = 'BTCUSD.SPOT'
        with self.assertRaises(ValueError):
            validate_quantity_precision(to_currency,
                                        instrument,
                                        quantity)

        to_currency = {
            "stable_coin": False,
            "is_crypto": True,
            "currency_type": "crypto",
            "readable_name": "Bitcoin",
            "long_only": False,
            "minimum_trade_size": 0.001
        }
        quantity = '4.131'
        instrument = 'LTCBTC.SPOT'
        with self.assertRaises(ValueError):
            validate_quantity_precision(to_currency,
                                        instrument,
                                        quantity)

    def test_validate_price_precision(self):
        price = '12.312411'
        with self.assertRaises(ValueError):
            validate_price_precision(price)

    def test_validate_minimum_trade_size(self):
        currency = {
            "stable_coin": False,
            "is_crypto": False,
            "currency_type": "fiat",
            "readable_name": "",
            "long_only": False,
            "minimum_trade_size": 0.01
        }
        quantity = '0.001'
        with self.assertRaises(ValueError):
            validate_minimum_trade_size(currency,
                                        quantity)

    def test_check_quote_still_valid(self):
        dt_now = datetime.datetime.now(datetime.timezone.utc)
        dt_valid_until = dt_now - datetime.timedelta(seconds=15)
        valid_until = dt_valid_until.strftime('%Y-%m-%dT%H:%M:%S.%f%z')
        self.assertTrue(check_quote_still_valid(valid_until))
