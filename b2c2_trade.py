import argparse
import decimal
import sys

import yaml

from src.commands import BaseCommand


def read_yaml_config():
    with open('config.yaml') as f:
        return yaml.safe_load(f)


def query_yes_no(question, default="yes"):
    """Ask a yes/no question via input() and return their answer.

    "question" is a string that is presented to the user.
    "default" is the presumed answer if the user just hits <Enter>.
            It must be "yes" (the default), "no" or None (meaning
            an answer is required of the user).

    The "answer" return value is True for "yes" or False for "no".
    """
    valid = {"yes": True, "y": True, "ye": True, "no": False, "n": False}
    if default is None:
        prompt = " [y/n] "
    elif default == "yes":
        prompt = " [Y/n] "
    elif default == "no":
        prompt = " [y/N] "
    else:
        raise ValueError("invalid default answer: '%s'" % default)

    while True:
        sys.stdout.write(question + prompt)
        choice = input().lower()
        if default is not None and choice == "":
            return valid[default]
        elif choice in valid:
            return valid[choice]
        else:
            sys.stdout.write("Please respond with 'yes' or 'no' " "(or 'y' or 'n').\n")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--instrument',
                        required=True,
                        type=str,
                        help='One of the available instruments to use')
    parser.add_argument('--side',
                        required=True,
                        type=str,
                        choices=['buy', 'sell'],
                        help='The side/action to execute on the instrument')
    parser.add_argument('--quantity',
                        required=True,
                        type=decimal.Decimal,
                        help='The quantity to trade (2 decimal digits for crypto to crypto,'
                             'for the rest, 4 digits precision)')

    config = read_yaml_config()
    base_command = BaseCommand(api_token=config['auth_token'],
                               base_url=config['base_url'],
                               timeout=config['timeout_seconds'],
                               max_retries=config['max_retries'])

    arguments = parser.parse_args()
    quote_response = base_command.request_for_quote(instrument=arguments.instrument,
                                                    side=arguments.side,
                                                    quantity=arguments.quantity)

    continue_to_trade = query_yes_no('Proceed for trade?')
    if continue_to_trade:
        base_command.make_trade(instrument=arguments.instrument,
                                side=arguments.side,
                                quantity=arguments.quantity,
                                price=quote_response['price'],
                                valid_until=quote_response['valid_until'])


if __name__ == "__main__":
    main()
