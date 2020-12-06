from alpha_vantage.timeseries import TimeSeries
import sys
import pandas as pd

with open('keyfile.txt', 'r') as f:
    key = f.read()

ts = TimeSeries(key=key, output_format='pandas')

dfs = pd.DataFrame()
first_df = 1

for ticker in sys.argv[1:]:
    try:
        data, meta = ts.get_intraday(ticker, outputsize='full')
        #dfs[ticker] = data['4. close'].values
        data[ticker] = data['4. close']
        data = data[[ticker]]
        if first_df:
            dfs = data
            first_df = 0
        else:
            dfs = dfs.join(data)
        print("Data fetched for ticker: {}".format(ticker))
    except Exception as e:
        print("Exception occured for ticker {}".format(ticker))
        print(e)

print(dfs)