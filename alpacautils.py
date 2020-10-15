## Imports
import yfinance as yf
import finviz as fvz
import os
from openpyxl import load_workbook
import pandas as pd
import datetime as dt
import kirkconstants as kc
import updatemms as upm
import tradingutils as trutil
import requests
import numpy as np
import time


def main():
    # Formatting pandas to have 2 decimal points
    apiKey = kc.ALPACA_API_KEY
    secretKey = kc.ALPACA_SECRET_KEY
    print('apiKey: ' + apiKey)
    print('secretKey: ' + secretKey)

if __name__ == "__main__":
    try:
        main()
    except SystemExit as e:
        print('Error Exception triggered')