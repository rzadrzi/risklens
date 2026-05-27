import pytest
import pandas as pd
from risklens.risk.market_risk import (returns, log_returns, volatility, historical_VaR, CVaR, max_drawdown)

def test_returns():
    prices = pd.Series([100, 110, 121])
    result = returns(prices)
    expected = pd.Series([.10, .10], index=[1,2])
    pd.testing.assert_series_equal(result, expected)

def test_empty_returns():
    empty_series = pd.Series(dtype=float)
    with pytest.raises(ValueError):
        volatility(empty_series)

def test_volatility():
    prices = pd.Series([100, 110, 121])
    result = volatility(prices)
    assert result > 0

def test_historical_VaR():
    returns = pd.Series([0.1, -0.12, ])
