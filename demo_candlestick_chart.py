import yfinance as yf
import plotext as plt

ISIN = 'IE00B4L5Y983'

data = yf.Ticker(ISIN).history(start='2026-02-01')
dates = plt.datetimes_to_string(data.index)
data = data.reset_index(drop=True)

plt.date_form('d/m/Y')
plt.theme('dark')
plt.candlestick(dates, data)

ticker = yf.Ticker(ISIN)
plt.title(f"{ISIN} {ticker.info['longName']}")
plt.xlabel("Date")
plt.ylabel("Stock Price $")
plt.show()