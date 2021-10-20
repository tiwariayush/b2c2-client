import datetime
import decimal
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


def get_number_of_decimal_digits(value):
    if not isinstance(value, decimal.Decimal):
        if isinstance(value, str):
            value = float(value)
        value = decimal.Decimal(f'{value:g}')
    digits = value.as_tuple().exponent * (-1)
    return digits


def validate_quantity_precision(to_currency, instrument, quantity):
    """
    Quantity precision (base currency) is 2 decimal digits for
    crypto-to-crypto instruments, 4 for crypto-to-fiat and
    crypto-to-stablecoin instruments.
    :param to_currency: Currency info of the counter currency
    :param instrument: Instrument being traded
    :param quantity: Quantity of the trade
    """
    digits = get_number_of_decimal_digits(quantity)

    decimal_digits_allowed = 2
    if not to_currency['is_crypto']:
        # For the instruments which are not crypto to crypto, we allow
        # upto 4 digits precision
        decimal_digits_allowed = 4

    if digits > decimal_digits_allowed:
        error_message = f"The instrument {instrument} supports " \
                        f"maximum of {decimal_digits_allowed} digits " \
                        f"quantity precision."
        logger.error(error_message)
        raise ValueError(error_message)


def validate_price_precision(price):
    """
    Validate if the price precision (counter currency) is
    always less than or equal 5 significant figures.
    :param price: Price of the trade
    """
    digits = get_number_of_decimal_digits(price)

    if digits > 5:
        error_message = "The price precision is more than " \
                        "5 significant figures."
        logger.error(error_message)
        raise ValueError(error_message)


def validate_minimum_trade_size(currency, quantity):
    """
    Check the minimum trade size for the given currency
    :param currency: Currency info
    :param quantity: Quantity of the trade
    """
    if not isinstance(quantity, decimal.Decimal):
        quantity = decimal.Decimal(quantity)

    if quantity < currency['minimum_trade_size']:
        error_message = f"Minimum trading size for " \
                        f"{currency['readable_name']} not valid"
        logger.error(error_message)
        raise ValueError(error_message)


def check_quote_still_valid(valid_until):
    # check that the RFQ is still valid
    dt_until = datetime.datetime.strptime(
        valid_until, "%Y-%m-%dT%H:%M:%S.%f%z"
    )
    dt_now = datetime.datetime.now(datetime.timezone.utc)
    time_available = dt_now - dt_until
    if time_available.seconds > 10:
        return True
    else:
        return False
