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
print()
#dfs.to_csv('aggregated_data.csv')

# Optimizer Script
from pypfopt import expected_returns, risk_models
from pypfopt.cla import CLA
from pypfopt.discrete_allocation import DiscreteAllocation, get_latest_prices

exp_returns = expected_returns.mean_historical_return(dfs.dropna())
cov = risk_models.sample_cov(dfs.dropna())

model = CLA(exp_returns, cov)
model.max_sharpe()

weights = model.clean_weights()


print("Proportions of your portfolio")
for k, v in weights.items():
    if v>0.0:
        print("{}---->{}".format(k, round(v, 2)))
print()

print("Number of stocks to buy")
latest_prices = get_latest_prices(dfs)
da = DiscreteAllocation(weights, latest_prices, total_portfolio_value=10000)
allocation, leftover = da.lp_portfolio()
for k, v in allocation.items():
    if v>0.0:
        print("{}---->{}".format(k, round(v, 2)))
print("Leftover from portfolio: ${}".format(round(leftover, 2)))
print()

print("Expected performance of your portfolio")
ann_return, ann_sharpe, ann_volatility = model.portfolio_performance()
print("Annualized Return: {}%".format(round(ann_return, 2)))
print("Annualized Sharpe Ratio: {}".format(round(ann_sharpe, 2)))
print("Annualized Volatility: {}%".format(round(ann_volatility, 2)))
print()
