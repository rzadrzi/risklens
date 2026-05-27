# 01
# daily returns
# volatility
# VaR
# CVaR/ Expected Shortfall
# Maximum Drawdown
import numpy as np
import pandas as pd

def returns(prices: pd.DataFrame) -> pd.DataFrame:
    return prices.pct_change().dropna()

def log_returns(prices: pd.DataFrame) -> pd.DataFrame:
    return np.log(prices/prices.shift(1)).dropna()

def volatility(returns: pd.Series, annualized:bool=False, trading_days:int=252) -> float:
    """

    :param returns:
    :param annualized:
    :param trading_days:
    :return:
    """
    if returns.empty:
        raise ValueError("Returns series is empty.")

    vol = returns.std()

    if annualized:
        vol *= np.sqrt(trading_days)

    return vol


def historical_VaR(returns: pd.Series, confidence_level:float=0.95) -> float:
    """
    Calculate Historical Value at Risk(VaR).

    :param returns: Asset returns series
    :param confidence_level: confidence level (default=0.95)
    :return: Historical Value at Risk(VaR)
    """
    if returns.empty:
        raise ValueError("Returns series is empty.")

    if not 0<confidence_level<1:
        raise ValueError("Confidence level must be between 0 and 1.")

    percentile = (1-confidence_level)*100
    var = np.percentile(returns, percentile)
    return abs(var)


def CVaR(returns: pd.Series, confidence_level:float=0.95)->float:
    """
    Calculate Conditional VaR(CVaR).
    :param returns: Asset returns series
    :param confidence_level: confidence level (default=0.95)
    :return: Conditional VaR(CVaR)
    """
    if returns.empty:
        raise ValueError("Returns series is empty.")

    if not 0 < confidence_level < 1:
        raise ValueError("Confidence level must be between 0 and 1.")
    percentile = (1-confidence_level)*100
    var_threshold = np.percentile(returns, percentile)
    tail_losses = returns[returns <= var_threshold]
    cvar = tail_losses.mean
    return abs(cvar)


def max_drawdown(returns: pd.Series)->float:
    """

    :param returns:
    :return:
    """
    if returns.empty:
        raise ValueError("Returns series is empty.")
    cum = (1+returns).cumprod()
    running_max = (cum.cummax())
    drawdowns = (cum - running_max)/running_max
    max_dd = drawdowns.min()
    return abs(max_dd)
