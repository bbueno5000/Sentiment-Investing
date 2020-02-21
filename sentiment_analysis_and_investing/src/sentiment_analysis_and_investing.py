"""
DOCSTRING
"""
import datetime
import math
from matplotlib import pyplot
from matplotlib import style
import pandas
import pandas_datareader


style.use('ggplot')

def automatic_moving_average(
    ticker_symbol, 
    denominator_1=275, 
    denominator_2=110, 
    denominator_3=55, 
    denominator_4=5.5):
    """
    DOCSTRING
    """
    dataframe_a = pandas.read_csv('data/stocks_sentdex_1-6-2016.csv')
    dataframe_a = dataframe_a[dataframe_a.type == ticker_symbol.lower()]
    count = dataframe_a['type'].value_counts()
    count = int(count[ticker_symbol])
    moving_average_1 = dataframe_a['value'].rolling(count/denominator_1)
    moving_average_2 = dataframe_a['value'].rolling(count/denominator_2)
    moving_average_3 = dataframe_a['value'].rolling(count/denominator_3)
    moving_average_4 = dataframe_a['value'].rolling(count/denominator_4)
    starting_point = int(math.ceil(count/denominator_4))
    dataframe_a['MA1'] = moving_average_1
    dataframe_a['MA2'] = moving_average_2
    dataframe_a['MA3'] = moving_average_3
    dataframe_a['MA4'] = moving_average_4
    dataframe_a = dataframe_a[starting_point:]
    del dataframe_a['MA100']
    del dataframe_a['MA250']
    del dataframe_a['MA500']
    del dataframe_a['MA5000']
    dataframe_a['position'] = map(
        calculate_position, 
        dataframe_a['MA1'], 
        dataframe_a['MA2'],
        dataframe_a['MA3'],
        dataframe_a['MA4']
        )
    axis_1 = pyplot.subplot(2, 1, 1)
    dataframe_a['close'].plot(label='Price')
    pyplot.legend()
    axis_2 = pyplot.subplot(2, 1, 2, sharex=axis_1)
    dataframe_a['MA1'].plot(label=str(count/denominator_1)+'MA')
    dataframe_a['MA2'].plot(label=str(count/denominator_2)+'MA')
    dataframe_a['MA3'].plot(label=str(count/denominator_3)+'MA')
    dataframe_a['MA4'].plot(label=str(round(count/denominator_4), 1)+'MA')
    pyplot.legend()
    pyplot.show()

def calculate_position(moving_average_1, moving_average_2, moving_average_3, moving_average_4):
    """
    DOCSTRING
    """
    if moving_average_4 > moving_average_1 > moving_average_2 > moving_average_3:
        return 1
    elif moving_average_1 > moving_average_4 > moving_average_2 > moving_average_3:
        return 2
    elif moving_average_1 > moving_average_2 > moving_average_4 > moving_average_3:
        return 3
    elif moving_average_1 > moving_average_2 > moving_average_3 > moving_average_4:
        return 4
    elif moving_average_1 < moving_average_2 < moving_average_3 < moving_average_4:
        return -4
    elif moving_average_1 < moving_average_2 < moving_average_4 < moving_average_3:
        return -3
    elif moving_average_1 < moving_average_4 < moving_average_2 < moving_average_3:
        return -2
    elif moving_average_4 < moving_average_1 < moving_average_2 < moving_average_3:
        return -1
    else:
        return None

def introduction():
    """
    DOCSTRING
    """
    sp500 = pandas_datareader.data.get_data_yahoo(
        '%5EGSPC', 
        start=datetime.datetime(2000, 10, 1),
        end=datetime.datetime(2012, 1, 1)
        )
    sp500.to_csv('sp500_ohlc.csv')
    dataframe_a = pandas.read_csv('sp500_ohlc.csv', index_col='Date', parse_dates=True)
    dataframe_a['high_minus_low'] = dataframe_a.High - dataframe_a.Low
    close = dataframe_a['Adj Close']
    moving_average = close.rolling(50).mean()
    axis_1 = pyplot.subplot(2, 1, 1)
    axis_1.plot(close, label='sp500')
    axis_1.plot(moving_average, label='ma50')
    pyplot.legend()
    axis_2 = pyplot.subplot(2, 1, 2, sharex=axis_1)
    axis_2.plot(dataframe_a['high_minus_low'], label='H-L')
    pyplot.legend()
    pyplot.show()

def modify_dataset():
    """
    DOCSTRING
    """
    dataframe_a = pandas.read_csv('data/stocks_sentdex_1-6-2016.csv')
    dataframe_a['time'] = pandas.to_datetime(dataframe_a['time'], unit='s')
    dataframe_a = dataframe_a.set_index('time')
    dataframe_a.to_csv('data/stocks_sentdex_1-6-2016_full.csv')

def outlier_fixing(ticker_symbol):
    """
    DOCSTRING
    """
    dataframe_a = pandas.read_csv('data/stocks_sentdex_1-6-2016.csv')
    dataframe_a = dataframe_a[dataframe_a.type == ticker_symbol.lower()]
    axis_1 = pyplot.subplot(2, 1, 1)
    dataframe_a['close'].plot(label='Price')
    pyplot.legend()
    dataframe_a['std'] = dataframe_a['close'].rolling(25, min_periods=1).std()
    dataframe_a = dataframe_a[dataframe_a['std']<20]
    axis_2 = pyplot.subplot(2, 1, 2, sharex=axis_1)
    dataframe_a['std'].plot(label='Deviation')
    pyplot.legend()
    pyplot.show()

def single_stock(ticker_symbol):
    """
    DOCSTRING
    """
    dataframe_a = pandas.read_csv(
        'data/stocks_sentdex_1-6-2016.csv', 
        index_col='time', 
        parse_dates=True
        )
    dataframe_a = dataframe_a[dataframe_a.type == ticker_symbol.lower()]
    moving_average_500 = dataframe_a['value'].rolling(500).mean()
    axis_1 = pyplot.subplot(2, 1, 1)
    dataframe_a['close'].plot(label='Price')
    pyplot.legend()
    axis_2 = pyplot.subplot(2, 1, 2, sharex=axis_1)
    moving_average_500.plot(label='ma500')
    pyplot.legend()
    pyplot.show()

if __name__ == '__main__':
    outlier_fixing('btcusd')