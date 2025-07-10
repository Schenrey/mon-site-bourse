import pandas as pd
import numpy as np
import yfinance as yf
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report

def compute_features(df):
    close = df['Close']

    # RSI
    delta = close.diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
    rs = gain / loss
    rsi = 100 - (100 / (1 + rs))

    # EMA
    ema5 = close.ewm(span=5, adjust=False).mean()
    ema20 = close.ewm(span=20, adjust=False).mean()

    # MACD
    ema_fast = close.ewm(span=12, adjust=False).mean()
    ema_slow = close.ewm(span=26, adjust=False).mean()
    macd = ema_fast - ema_slow
    signal = macd.ewm(span=9, adjust=False).mean()

    # Momentum (différence prix sur 5 jours)
    momentum = close.diff(5)

    features = pd.DataFrame({
        'RSI': rsi,
        'EMA5': ema5,
        'EMA20': ema20,
        'MACD': macd,
        'Signal': signal,
        'Momentum': momentum
    })

    return features

def prepare_data(ticker):
    stock = yf.Ticker(ticker)
    df = stock.history(period="1y", interval="1d")

    features = compute_features(df)

    # Label : +1 si prix 5 jours plus haut que prix actuel, -1 sinon
    df['Future_Close'] = df['Close'].shift(-5)
    df['Target'] = np.where(df['Future_Close'] > df['Close'], 1, -1)

    dataset = features.copy()
    dataset['Target'] = df['Target']

    dataset = dataset.dropna()

    return dataset

def train_model(ticker):
    dataset = prepare_data(ticker)
    X = dataset.drop(columns=['Target'])
    y = dataset['Target']

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, shuffle=False)

    clf = RandomForestClassifier(n_estimators=100, random_state=42)
    clf.fit(X_train, y_train)

    y_pred = clf.predict(X_test)

    print(f"Rapport classification pour {ticker}:")
    print(classification_report(y_test, y_pred))

    return clf

def predict_next_move(model, recent_data):
    # recent_data = DataFrame avec mêmes features, dernière ligne pour prédiction
    pred = model.predict(recent_data)
    return pred[0]

if __name__ == "__main__":
    ticker = "AAPL"
    model = train_model(ticker)

    # Exemple pour prédire avec les dernières données
    stock = yf.Ticker(ticker)
    df = stock.history(period="30d", interval="1d")
    features = compute_features(df).dropna()
    last_row = features.iloc[[-1]]

    pred = predict_next_move(model, last_row)
    print("Prédiction prochain mouvement:", "HAUSSE" if pred == 1 else "BAISSE")
