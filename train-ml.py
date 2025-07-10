import yfinance as yf
import pandas as pd
import numpy as np
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Dropout
from tensorflow.keras.callbacks import EarlyStopping
import os

def get_data(ticker, period="5y"):
    df = yf.download(ticker, period=period)
    df.dropna(inplace=True)

    delta = df['Close'].diff()
    gain = delta.clip(lower=0)
    loss = -delta.clip(upper=0)
    avg_gain = gain.rolling(window=14).mean()
    avg_loss = loss.rolling(window=14).mean()
    rs = avg_gain / avg_loss
    df['RSI'] = 100 - (100 / (1 + rs))

    df['EMA20'] = df['Close'].ewm(span=20, adjust=False).mean()

    df['Future_Close'] = df['Close'].shift(-5)
    df['Target'] = (df['Future_Close'] > df['Close']).astype(int)

    df.dropna(inplace=True)
    return df

def create_sequences(data, features, target, seq_length=30):
    X, y = [], []
    for i in range(len(data) - seq_length):