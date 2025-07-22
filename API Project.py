
"""
API

"""


from requests import Request, Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import json
import pandas as pd

"""
url ='https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'

parameters = {
    'start':'1',
    'limit':'20',
    'convert':'USD'
}
headers = {
    'Accepts': 'application/json',
    'X-CMC_PRO_API_KEY': '0ad53085-1cb2-4eb8-ad9e-3ffbd7e56509',
}

session = Session()
session.headers.update(headers)

try:
    response = session.get(url, params=parameters)
    data = json.loads(response.text)
except (ConnectionError, Timeout, TooManyRedirects) as e:
    print(e)
    

df = pd.json_normalize(data['data'])
df['timestamp'] = pd.to_datetime('now')
"""

pd.set_option('display.max_columns', None) # display all columns in the output

def api_runner():
    global df
    url ='https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'

    parameters = {
        'start':'1',
        'limit':'20', # take only 20 rows
        'convert':'USD'
    }
    headers = {
        'Accepts': 'application/json',
        'X-CMC_PRO_API_KEY': '0ad53085-1cb2-4eb8-ad9e-3ffbd7e56509',
    }

    session = Session()
    session.headers.update(headers)

    try:
        response = session.get(url, params=parameters)
        data = json.loads(response.text)
    except (ConnectionError, Timeout, TooManyRedirects) as e:
        print(e)
        
        
    df = pd.json_normalize(data['data']) # convert data from json
    df['timestamp'] = pd.to_datetime('now') # add time column when data was retreived
    df
    
    # writing data frame into csv
    if not os.path.isfile(r'C:\Users\alisa\Documents\Python\API.csv'):
        df.to_csv(r'C:\Users\alisa\Documents\Python\API.csv', header = 'column_names')
    else:
        df.to_csv(r'C:\Users\alisa\Documents\Python\API.csv', mode = 'a', header = False)



import os
from time import time
from time import sleep

for i in range(100):
    api_runner()
    print('API Runner completed successfully')
    sleep(60) # running every 60 seconds and adds the new data to the existing
exit()

df2 = pd.read_csv(r'C:\Users\alisa\Documents\Python\API.csv') # read csv file

pd.set_option('display.float_format', lambda x: '%.5f' % x) # cut to 5 decimals


# grouping by name, taking columns from 1h to 90 days, and finding mean for every group 
df3 = df2.groupby('name', sort = False)[['quote.USD.percent_change_1h', 'quote.USD.percent_change_24h', 'quote.USD.percent_change_7d', 'quote.USD.percent_change_30d', 'quote.USD.percent_change_60d', 'quote.USD.percent_change_90d']].mean()

df4 = df3.stack() # data type is series for better grouping

df4 = df4.to_frame(name = 'values') # back to data frame

#df4.count()
index = pd.Index(range(120)) 

df5 = df4.reset_index() # new index

df5 = df5.rename(columns = {'level_1': 'percent_change'})

# replacing column names with shorter names
df5['percent_change'] = df5['percent_change'].replace(['quote.USD.percent_change_1h', 'quote.USD.percent_change_24h', 'quote.USD.percent_change_7d', 'quote.USD.percent_change_30d', 'quote.USD.percent_change_60d', 'quote.USD.percent_change_90d'], ['1h', '24h', '7d', '30d', '60d', '90d'])

import seaborn as sns
import matplotlib.pyplot as plt

sns.catplot(x = 'percent_change', y = 'values', hue = 'name', data = df5, kind = 'point')

df10 = df2[['name', 'quote.USD.price', 'timestamp']]
df10 = df10.query("name == 'Bitcoin'")

sns.set_theme(style = 'darkgrid')
sns.lineplot(x = 'timestamp', y = 'quote.USD.price', data = df10)
