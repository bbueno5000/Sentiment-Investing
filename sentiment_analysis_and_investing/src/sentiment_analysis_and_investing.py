"""
DOCSTRING
"""
import datetime
import pandas
import pandas_datareader
from matplotlib import pyplot
from matplotlib import style

style.use('ggplot')

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
    standard_deviation['std'].plot(label='Deviation')
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