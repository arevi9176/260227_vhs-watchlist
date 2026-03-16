import yfinance as yf
import plotext as plt

plt.date_form('d/m/Y')

data = yf.Ticker('GOOG').history(start='2026-03-01')
dates = plt.datetimes_to_string(data.index)
data = data.reset_index(drop=True)

plt.candlestick(dates, data)

plt.title("Google Stock Price CandleSticks")
plt.xlabel("Date")
plt.ylabel("Stock Price $")
plt.show()