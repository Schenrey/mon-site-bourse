import yfinance as yf
import pandas as pd

def get_prices(tickers):
    # Téléchargement en batch, interval 1m, période 1 jour
    data = yf.download(tickers=tickers, period="1d", interval="1m", group_by='ticker', progress=False)

    prices = {}
    for ticker in tickers:
        try:
            # Pour tickers multiples, yfinance retourne un DataFrame multiindexé
            if len(tickers) > 1:
                df = data[ticker]
            else:
                df = data
            if not df.empty:
                prices[ticker] = df['Close'].iloc[-1]
            else:
                prices[ticker] = None
        except Exception:
            prices[ticker] = None
    return prices
