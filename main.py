from risklens.data.fetch_data import fetch_prices
from risklens.analytics.returns import calculate_returns
from risklens.risk.var import historical_var

tickets = ["SPY", "QQQ", "GLD", "TLT", "BTC-USD"]

prices = fetch_prices(tickets, start_date="2020-01-01", end_date="2025-01-01")
returns = calculate_returns(prices)
portfolio_returns = returns.mean(axis=1)

var_95 = historical_var(portfolio_returns, .95)

print(prices.head())
print(portfolio_returns.head())
print(var_95)