import yfinance as yf
import pandas as pd
import numpy as np
from tensorflow.keras.models import load_model

MODEL_PATH = "models/AAPL_lstm_model.h5"
model = None
history = {}

def load_lstm_model():
    global model
    if model is None:
        model = load_model(MODEL_PATH)

def get_recent_data(ticker, features, seq_length=30):
    df = yf.download(ticker, period="2mo")
    df.dropna(inplace=True)

    delta = df['Close'].diff()
    gain = delta.clip(lower=0)
    loss = -delta.clip(upper=0)
    avg_gain = gain.rolling(window=14).mean()
    avg_loss = loss.rolling(window=14).mean()
    rs = avg_gain / avg_loss
    df['RSI'] = 100 - (100 / (1 + rs))
    df['EMA20'] = df['Close'].ewm(span=20, adjust=False).mean()
    df.dropna(inplace=True)

    recent = df[features].tail(seq_length)
    return recent

def predict_trend(ticker="AAPL"):
    load_lstm_model()
    features = ['Close', 'Volume', 'RSI', 'EMA20']
    seq_length = 30
    recent_data = get_recent_data(ticker, features, seq_length)

    if len(recent_data) < seq_length:
        return "Données insuffisantes"

    x_input = recent_data.values.reshape(1, seq_length, len(features))
    prob = model.predict(x_input)[0][0]

    if prob > 0.6:
        return f"Acheter ({prob:.2f})"
    elif prob < 0.4:
        return f"Vendre ({prob:.2f})"
    else:
        return f"Neutre ({prob:.2f})"

def get_price(tickers):
    prices = {}
    for ticker in tickers:
        stock = yf.Ticker(ticker)
        data = stock.history(period="1d", interval="1m")
        if not data.empty:
            prices[ticker] = data['Close'].iloc[-1]
        else:
            prices[ticker] = None
    return prices

def check_signals(tickers):
    alerts = []
    prices = get_price(tickers)

    for ticker in tickers:
        price = prices.get(ticker)
        if price is None:
            continue

        # Historique pour calcul variation sur 10 périodes
        if ticker not in history:
            history[ticker] = []
        history[ticker].append(price)
        if len(history[ticker]) > 10:
            old_price = history[ticker][-10]
            change = (price - old_price) / old_price * 100
            if change <= -3:
                alerts.append(f"Alerte ACHAT {ticker} : baisse de {change:.2f}%")
            elif change >= 5:
                alerts.append(f"Alerte VENTE {ticker} : hausse de {change:.2f}%")

        # Prédiction ML
        pred = predict_trend(ticker)
        alerts.append(f"{ticker} - Prédiction ML : {pred}")

    return alerts, prices
