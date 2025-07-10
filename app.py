import os
from flask import Flask, render_template
from flask_socketio import SocketIO
from strategy import check_signals
from alert import send_email
import threading
import time

app = Flask(__name__)
socketio = SocketIO(app)

TICKERS = ["AAPL", "TSLA", "BTC-USD", "ETH-USD"]  # Ajoute tes 200 tickers ici

def background_thread():
    while True:
        alerts, prices = check_signals(TICKERS)
        if alerts:
            for alert in alerts:
                socketio.emit('new_alert', {'message': alert})
                print(alert)
                send_email(alert)
        time.sleep(60)

@app.route("/")
def home():
    _, prices = check_signals(TICKERS)
    return render_template("home.html", prices=prices)

if __name__ == "__main__":
    thread = threading.Thread(target=background_thread)
    thread.daemon = True
    thread.start()

    port = int(os.environ.get("PORT", 5000))
    socketio.run(app, host="0.0.0.0", port=port)
