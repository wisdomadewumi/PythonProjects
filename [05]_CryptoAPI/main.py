from requests import Request, Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import json
import pandas as pd

# The following two lines are crucial for displaying the entire DataFrame in your terminal.
# They override Pandas' default display settings which truncate wide DataFrames.
pd.set_option('display.max_columns', None)
pd.set_option('display.width', 1000)
# You may also want to set max_rows if your data has many rows, to avoid truncation.
pd.set_option('display.max_rows', None)

url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'
parameters = {
    'start': '1',
    'limit': '5000',
    'convert': 'USD'
}
headers = {
    'Accepts': 'application/json',
    'X-CMC_PRO_API_KEY': '4e724473-916b-44ec-920f-23146ebaab30',
}

session = Session()
session.headers.update(headers)

try:
    response = session.get(url, params=parameters)
    data = json.loads(response.text)
    print(data)
except (ConnectionError, Timeout, TooManyRedirects) as e:
    print(e)

#________________________________________
pd.json_normalize(data['data'])