import yfinance

class PortfolioElement:
    """Repräsentiert ein Element im Portfolio, z.B. eine Aktie oder einen Fonds."""

    def __init__(self, isin: str, stueckzahl: float, kurs_beobachtung:float, waehrung:str="EUR"):

        self.isin = isin
        self.stueckzahl = stueckzahl
        self.kurs_beobachtung = kurs_beobachtung
        self.waehrung = waehrung

        try:
            self.ticker = yfinance.Ticker(isin)
        except Exception as e:
            raise ValueError(f"Fehler beim Abrufen des Tickers für ISIN {isin}: {e}")
        
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
        print(f"            ISIN: {self.isin}")
        print(f"            Name: {self.name}")
        print(f"         Währung: {self.waehrung}")
        print(f"      Stueckzahl: {self.stueckzahl}")
        print(f"Beobachtungskurs: {self.kurs_beobachtung}")
        print(f"  Aktueller Kurs: {self.kurs_aktuell}")
        print(f"    Kursänderung: {self.wertenwicklung_tag:.2f} ({self.wertenwicklung_tag_prozent:.2f}%)")
        print(f"     Schlusskurs: {self.kurs_schluss}")
        print(f"  Eröffnungskurs: {self.kurs_eroeffung}")
        print(f"       Tageshoch: {self.kurs_hoch}")
        print(f"       Tagestief: {self.kurs_tief}")
        print(f"  52 Wochen Hoch: {self.kurs_52wochen_hoch}")
        print(f"  52 Wochen Tief: {self.kurs_52wochen_tief}")


class PortfolioManager:
    """Verwaltet das Portfolio, z.B. durch Hinzufügen von Elementen und Berechnung von Kennzahlen."""

    def __init__(self, name: str) -> None:
        self.name = name
        self.elements = []

    def add(self, element: PortfolioElement) -> None:
        self.elements.append(element)

    def update(self) -> None:
        self.portfolio_wert_beobachtung = 0
        self.portfolio_wert_aktuell = 0
        self.portfolio_wertenwicklung_gesamt = 0
        self.portfolio_wertenwicklung_gesamt_prozent = 0
        self.portfolio_wertenwicklung_tag = 0
        self.portfolio_wertenwicklung_tag_prozent = 0

        for element in self.elements:
            element.update()
            self.portfolio_wert_beobachtung += element.wert_beobachtung
            self.portfolio_wert_aktuell += element.wert_aktuell
            self.portfolio_wertenwicklung_tag += (element.wertenwicklung_tag  * element.stueckzahl)

        self.portfolio_wertenwicklung_tag_prozent = self.portfolio_wertenwicklung_tag / self.portfolio_wert_aktuell * 100
        self.portfolio_wertenwicklung_gesamt = self.portfolio_wert_aktuell - self.portfolio_wert_beobachtung
        self.portfolio_wertenwicklung_gesamt_prozent = self.portfolio_wertenwicklung_gesamt / self.portfolio_wert_beobachtung * 100

    def info(self) -> None:
        self.update()
        print(f"\nPortfolio: {self.name}:\n")
        print("Name                        Anzahl  Beobachtungskurs   Aktueller Kurs   WE-Tag (%)   WE-Gesamt (%)")
        print("                           Währung  Beobachtungswert   Aktueller Wert   WE-Tag abs   WE-Gesamt abs")
        for el in self.elements:
            print(f"{el.name:25}{' '*4}{el.stueckzahl:5.1f}{' '*12}{el.kurs_beobachtung:6.2f}{' '*9}{el.kurs_aktuell:8.2f}{' '*7}{el.wertenwicklung_tag_prozent:6.2f}{' '*7}{el.wertenwicklung_gesamt_prozent:8.2f}")
            print(f"{' '*29}[{el.waehrung:3}]{' '*10}{el.wert_beobachtung:8.2f}{' '*9}{el.wert_aktuell:8.2f}{' '*7}{el.wertenwicklung_tag:6.2f}{' '*7}{el.wertenwicklung_gesamt:8.2f}")

        print()
        print(f"Portfolio Gesamtwert Beobachtung: {self.portfolio_wert_beobachtung:.2f} {el.waehrung}")
        print(f"    Portfolio Gesamtwert Aktuell: {self.portfolio_wert_aktuell:.2f} {el.waehrung}")
        print(f"Portfolio Wertentwicklung Gesamt: {self.portfolio_wertenwicklung_gesamt:.2f} {el.waehrung} ({self.portfolio_wertenwicklung_gesamt_prozent:.2f}%)")
        print(f"   Portfolio Wertentwicklung Tag: {self.portfolio_wertenwicklung_tag:.2f} {el.waehrung} ({self.portfolio_wertenwicklung_tag_prozent:.2f}%)")

if __name__ == "__main__":


    pe1 = PortfolioElement("DE000A1EWWW0", 20, 140.0)      # adidas
    pe2 = PortfolioElement("DE000BASF111", 20, 55.0)       # BASF
    pe3 = PortfolioElement("DE0007164600", 32, 180.0)      # SAP
    pe4 = PortfolioElement("DE000CBK1001", 100, 25.0)      # Commerzbank

    pe1.info()
