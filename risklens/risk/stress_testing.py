import numpy as np
import pandas as pd


def stress_test_percentage_shock(current_value: float, shock: float)->dict:
    """
    Quick sanity check
    instant stress testing

    :param current_value:
    :param shock:
    :return:
    """
    if current_value <= 0:
        raise ValueError("current_value must be greater than zero.")
    if shock < -1:
        raise ValueError("shock cannot less than -100%.")

    stress_value = current_value * ( 1 + shock )
    loss = current_value - stress_value

    return {
        "current_value": current_value,
        "shock": shock,
        "stress_value": stress_value,
        "loss": loss,
    }

def historical_stress_test(current_value: float, returns:pd.Series)->dict:
    """
    realistic stress
    backtest risk

    :param current_value:
    :param returns:
    :return:
    """
    if current_value <= 0:
        raise ValueError("current_value must be greater than zero.")
    if returns.empty:
        raise ValueError("Returns series is empty.")

    clean_returns = returns.dropna()
    if clean_returns.empty:
        raise ValueError("Returns series contains only NaN values.")

    worst_return = clean_returns.mean()
    stressed_value = current_value * (1 + worst_return)
    loss = current_value - stressed_value

    return {
        "current_value": current_value,
        "worst_return": worst_return,
        "stressed_value": stressed_value,
        "loss": loss,
    }

def scenario_stress_test(current_value: float, scenario_name:str, shock:float)->dict:
    """
    institutional-style scenarios
    risk reporting

    :param current_value:
    :param scenario_name:
    :param shock:
    :return:
    """
    if not scenario_name:
        raise ValueError("scenario_name must not be empty.")

    result = stress_test_percentage_shock(current_value, shock)
    return {
        "scenario_name": scenario_name,
        **result,
    }

def monte_carlo_stress_test(
        current_value: float,
        returns:pd.Series,
        simulations:int=10_000,
        confidence_level:float=0.95,
        random_seed:int | None=None,
)->dict:
    """
    quant-grade risk
    institutional modeling

    :param current_value:
    :param returns:
    :param simulations:
    :return:
    """
    if returns.empty:
        raise ValueError("Returns series is empty.")
    if current_value <= 0:
        raise ValueError("current_value must be greater than zero.")
    if simulations <= 0:
        raise ValueError("simulations must be greater than zero.")
    if not 0<=confidence_level<=1:
        raise ValueError("confidence_level must be between 0 and 1.")

    clean_returns = returns.dropna()
    if clean_returns.empty:
        raise ValueError("Returns series contains only NaN values.")
    mean_returns = clean_returns.mean()
    volatility_returns = clean_returns.std()

    rng = np.random.default_rng(random_seed)

    simulated_returns = rng.normal(loc=mean_returns, scale=volatility_returns, size=simulations)
    simulated_value = current_value * (1 + simulated_returns)
    simulated_loss = current_value - simulated_value

    var_percentile = confidence_level * 100
    var_loss = np.percentile(simulated_loss, var_percentile)

    tail_losses = simulated_loss[simulated_loss > var_loss]
    cvar_loss = tail_losses.mean()

    worst_case_loss = simulated_loss.max()

    average_loss = simulated_loss.mean()

    return {
        "current_value": current_value,
        "simulations": simulations,
        "confidence_level": confidence_level,
        "mean_returns": mean_returns,
        "volatility": volatility_returns,
        "var_loss": var_loss,
        "cvar_loss": cvar_loss,
        "worst_case_loss": worst_case_loss,
        "average_loss": average_loss,
    }
