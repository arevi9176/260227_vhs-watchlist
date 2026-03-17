import yfinance

def hole_wechselkurs(waehrung):
    """Gibt den aktuellen Wechselkurs von der angegebenen Währung zu EUR zurück."""
    ticker_symbol = f"{waehrung}EUR=X"
    ticker = yfinance.Ticker(ticker_symbol)
    
    # Abruf des aktuellsten Preises (Last Price)
    wechselkurs = ticker.fast_info['last_price']
    return wechselkurs


class PortfolioElement:
    """Repräsentiert ein Element im Portfolio, z.B. eine Aktie oder einen Fonds.
       Der Beobachtungskurs muss in EUR angegeben werden.
    """

    def __init__(self, isin: str, stueckzahl: float, kurs_beobachtung:float):

        self.isin = isin
        self.stueckzahl = stueckzahl
        self.kurs_beobachtung = kurs_beobachtung
   
        try:
            self.ticker = yfinance.Ticker(isin)
        except Exception as e:
            raise ValueError(f"Fehler beim Abrufen des Tickers für ISIN {isin}: {e}")
        
        ticker_waehrung = self.ticker.info.get("currency")
        self.waehrung = ticker_waehrung
        if self.waehrung == "EUR":
            self.wecheselkurs = 1.0
        else:
            self.wecheselkurs = hole_wechselkurs(self.waehrung)

        self.name = self.ticker.info["longName"]
        self.update()
  
    def update(self) -> None:
        self.kurs_aktuell = self.ticker.info["regularMarketPrice"] * self.wecheselkurs
        self.kurs_schluss = self.ticker.info["previousClose"] * self.wecheselkurs
        self.kurs_eroeffung = self.ticker.info["regularMarketOpen"] * self.wecheselkurs
        self.kurs_hoch = self.ticker.info["regularMarketDayHigh"] * self.wecheselkurs
        self.kurs_tief = self.ticker.info["regularMarketDayLow"] * self.wecheselkurs
        self.kurs_52wochen_hoch = self.ticker.info["fiftyTwoWeekHigh"] * self.wecheselkurs
        self.kurs_52wochen_tief = self.ticker.info["fiftyTwoWeekLow"] * self.wecheselkurs

        # Beobachtungswert: Gesamtwert der im Besitz befindlichen Wertpapiere zum Beobachtungskurs
        self.wert_beobachtung = self.stueckzahl * self.kurs_beobachtung

        # Aktueller Wert: Gesamtwert der im Besitz befindlichen Wertpapiere zum aktuellen Kurs
        self.wert_aktuell = self.stueckzahl * self.kurs_aktuell

        # Tageswertentwicklung: Differenz zwischen aktuellem Kurs und Schlusskurs
        self.wertenwicklung_tag = self.ticker.info["regularMarketChange"]
        self.wertenwicklung_tag_prozent = self.ticker.info["regularMarketChangePercent"]

        # Gesamtwertentwicklung: Differenz zwischen aktuellem Wert und Beobachtungswert
        self.wertenwicklung_gesamt = self.wert_aktuell - self.wert_beobachtung
        self.wertenwicklung_gesamt_prozent = self.wertenwicklung_gesamt / self.wert_beobachtung * 100


    def info(self) -> None:
        print(f"              ISIN: {self.isin}")
        print(f"              Name: {self.name}")
        print(f"           Währung: {self.waehrung}")
        print(f"        Stueckzahl: {self.stueckzahl}")
        print(f"  Beobachtungskurs: {self.kurs_beobachtung}")
        print(f"       Schlusskurs: {self.kurs_schluss}")
        print(f"    Aktueller Kurs: {self.kurs_aktuell}")
        print(f"      Kursänderung: {self.wertenwicklung_tag:.2f} ({self.wertenwicklung_tag_prozent:.2f}%)")
        print(f"    Eröffnungskurs: {self.kurs_eroeffung}")
        print(f"         Tageshoch: {self.kurs_hoch}")
        print(f"         Tagestief: {self.kurs_tief}")
        print(f"    52 Wochen Hoch: {self.kurs_52wochen_hoch}")
        print(f"    52 Wochen Tief: {self.kurs_52wochen_tief}")
        print(f"Gesamtkursänderung: {self.wertenwicklung_gesamt:.2f} ({self.wertenwicklung_gesamt_prozent:.2f}%)")


if __name__ == "__main__":

    pe1 = PortfolioElement("DE000A1EWWW0", 20, 140.0)      # adidas
    pe2 = PortfolioElement("DE000BASF111", 20, 55.0)       # BASF

    pe1.info()
