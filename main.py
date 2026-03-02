import yfinance

def hole_yf_symbol(isin:str):
    search = yfinance.Search(isin, max_results=1)
    if search.quotes:
        return search.quotes[0]['symbol']
    return None


class PortfolioElement:

    def __init__(self, isin: str, stueckzahl: float, kurs_beobachtung:float, waehrung:str="EUR"):

        self.isin = isin
        self.stueckzahl = stueckzahl
        self.kurs_beobachtung = kurs_beobachtung
        self.waehrung = waehrung

        yf_symbol= hole_yf_symbol(isin)
        if yf_symbol is None:
            raise ValueError(f"Kein Yahoo Finance-Symbol für ISIN {isin} gefunden.")

        self.ticker = yfinance.Ticker(yf_symbol)
        ticker_waehrung = self.ticker.info.get("currency")
        if ticker_waehrung != self.waehrung:
            raise ValueError(f"ISIN: {isin} -> Angegebene Währung {waehrung} stimmt nicht mit der Währung des Tickers {ticker_waehrung} überein.")

        self.name = self.ticker.info["longName"]
        self.update()
  
    def update(self) -> None:
        self.kurs_aktuell = self.ticker.info["regularMarketPrice"]
        self.kurs_schluss = self.ticker.info["previousClose"]
        self.kurs_eroeffung = self.ticker.info["regularMarketOpen"]
        self.kurs_hoch = self.ticker.info["regularMarketDayHigh"]
        self.kurs_tief = self.ticker.info["regularMarketDayLow"]
        self.kurs_52wochen_hoch = self.ticker.info["fiftyTwoWeekHigh"]
        self.kurs_52wochen_tief = self.ticker.info["fiftyTwoWeekLow"]
        self.kurs_aenderung = self.ticker.info["regularMarketChange"]
        self.kurs_aenderung_prozent = self.ticker.info["regularMarketChangePercent"]

    def info(self) -> None:
        print(f"ISIN: {self.isin}")
        print(f"Name: {self.name}")
        print(f"Währung: {self.waehrung}")
        print(f"Stueckzahl: {self.stueckzahl}")
        print(f"Beobachtungskurs: {self.kurs_beobachtung}")
        print(f"Aktueller Kurs: {self.kurs_aktuell}")
        print(f"Kursänderung: {self.kurs_aenderung} ({self.kurs_aenderung_prozent:.2f}%)")
        print(f"Schlusskurs: {self.kurs_schluss}")
        print(f"Eröffnungskurs: {self.kurs_eroeffung}")
        print(f"Tageshoch: {self.kurs_hoch}")
        print(f"Tiefstkurs: {self.kurs_tief}")
        print(f"52 Wochen Hoch: {self.kurs_52wochen_hoch}")
        print(f"52 Wochen Tief: {self.kurs_52wochen_tief}")

if __name__ == "__main__":

    element = PortfolioElement(isin="DE0007030009", stueckzahl=10, kurs_beobachtung=150.0)
    element.info()