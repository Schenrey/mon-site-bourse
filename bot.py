import schedule
import time
from strategy import check_signals
from alert import send_email
from tickers import TICKERS



def job():
    alert = check_signals("AAPL")
    if alert:
        print(alert)
        send_email(alert)

schedule.every(1).minutes.do(job)

if __name__ == "__main__":
    while True:
        schedule.run_pending()
        time.sleep(1)
