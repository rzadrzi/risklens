import numpy as np
import pandas as pd

def returns(prices: pd.DataFrame) -> pd.DataFrame:
    """
    return is a profit on an investment
    :param prices:
    :return: returns series
    """
    return prices.pct_change().dropna()

def log_returns(prices: pd.DataFrame) -> pd.DataFrame:
    """
    return is a profit on an investment
    :param prices:
    :return: returns series
    """
    return np.log(prices/prices.shift(1)).dropna()

def volatility(returns: pd.Series, annualized:bool=False, trading_days:int=252) -> float:
    """
    Volatility shows how much a security or market index’s returns fluctuate over time,
    indicating how widely prices move around their average.
    It's often calculated from the standard deviation or the variance between those returns.
    In most cases, the higher the volatility, the riskier the security.

    :param returns:
    :param annualized:
    :param trading_days:
    :return: volatility
    """
    if returns.empty:
        raise ValueError("Returns series is empty.")

    vol = returns.std()

    if annualized:
        vol *= np.sqrt(trading_days)

    return vol


def historical_VaR(returns: pd.Series, confidence_level:float=0.95) -> float:
    """
    It estimates how much a set of investments might lose (with a given probability),
    given normal market conditions, in a set time period such as a day.

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
    Conditional Value-at-Risk (CVaR) is defined as a coherent risk measure that quantifies
    the expected loss exceeding a specified value at a given confidence level.
    It is also known as Mean Shortfall or Tail Var

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
    The maximum drawdown, or “MDD”, is a metric that tracks
    the most significant potential percentage decline in the value of a portfolio over a given period.
    Conceptually, the maximum drawdown identifies the peak value and trough value of a portfolio or single investment,
    i.e. the volatility risk.

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
