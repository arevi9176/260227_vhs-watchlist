import yfinance as yf
import plotext as plt

ISIN = 'EUNL.DE'

plt.date_form('d/m/Y')

data = yf.Ticker(ISIN).history(start='2025-12-01')
dates = plt.datetimes_to_string(data.index)
data = data.reset_index(drop=True)

plt.candlestick(dates, data)

ticker = yf.Ticker(ISIN)
plt.title(f"{ISIN} {ticker.info['longName']}")
plt.xlabel("Date")
plt.ylabel("Stock Price $")
plt.show()