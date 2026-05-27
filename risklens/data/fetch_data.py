import yfinance as yf
import pandas as pd

def fetch_prices(tickers: list[str], start_date: str, end_date: str) -> pd.DataFrame:
    data = yf.download(tickers, start_date, end_date, auto_adjust=True)["Close"]

    if isinstance(data, pd.Series):
        data = data.to_frame(name=tickers[0])

    return data.dropna(how="all")

