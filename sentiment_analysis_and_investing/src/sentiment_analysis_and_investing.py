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

if __name__ == '__main__':
    modify_dataset()