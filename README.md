B2C2 CLI client
---------------
This project contains a B2C2 command line interface client application which uses sandbox API to trade.
It also contains setup file to create a dist and egg for the project and package it.

Setup Instructions
------------------
1. Obtain a token from B2C2 Sandbox API.
2. Update `config.yaml` with the value of `auth_token`.
3. Create python virtual environment using `python3 -m venv ./venv`
4. Activate the venv: `source venv/bin/activate`
5. Install the pre-requisites: `pip install -r requirement.txt`

To create a package:
```
python3 -m pip install --upgrade build
python3 -m build
```



Usage (Requesting Quotes and Executing Trades)
-----
From your CLI
` $ python b2c2_trade.py -h` should give you:
```
usage: b2c2_trade.py [-h] --instrument INSTRUMENT --side {buy,sell} --quantity QUANTITY

optional arguments:
  -h, --help            show this help message and exit
  --instrument INSTRUMENT
                        One of the available instruments to use
  --side {buy,sell}     The side/action to execute on the instrument
  --quantity QUANTITY   The quantity to trade (2 decimal digits for crypto to crypto,for
                        the rest, 4 digits precision)

```

Example to test the implementation of RFQ and trading:
```
python b2c2_trade.py  --instrument 'LTCAUD.SPOT' --side 'buy'  --quantity '1'
```

Some extra commands which call other endpoints:
- ` $ python b2c2_get_instruments.py`
- ` $ python b2c2_show_balance.py`


Running tests
-------------
`python -m unittest discover -v tests `


Further Improvements
--------------------
- Move logging to config level.
- More modular code to support more endpoints.
- Computation of balance before receiving from B2C2.
- Mock tests for HTTP Connection