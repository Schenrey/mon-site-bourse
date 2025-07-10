import yfinance as yf
from ta.momentum import RSIIndicator
from ta.trend import EMAIndicator

def get_indicators(ticker):
    try:
        data = yf.download(ticker, period="7d", interval="1h", progress=False)
        if data.empty or 'Close' not in data:
            return None

        close = data["Close"].dropna()

        rsi = RSIIndicator(close).rsi().iloc[-1]
        ema5 = EMAIndicator(close, window=5).ema_indicator().iloc[-1]
        ema20 = EMAIndicator(close, window=20).ema_indicator().iloc[-1]
        last_price = close.iloc[-1]

        return {
            "RSI": rsi,
            "EMA5": ema5,
            "EMA20": ema20,
            "last": last_price
        }
    except Exception:
        return None

