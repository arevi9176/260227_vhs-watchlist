import yfinance
import json
from rich.console import Console
from rich.table import Table
from rich import box


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
        """Initialisiert ein Portfolio-Element mit der angegebenen ISIN, Stückzahl und Beobachtungskurs."""
        self.isin = isin
        self.stueckzahl = stueckzahl
        self.kurs_beobachtung = kurs_beobachtung
   
        self.ticker = yfinance.Ticker(isin)

        try:
            self.waehrung = self.ticker.info["currency"]
        except Exception as e:
            raise ValueError(f"Fehler beim Abrufen der Währung für ISIN {isin}: {e}")
   
        self.name = self.ticker.info["longName"]
        self.update()
  
    def update(self) -> None:
        """Aktualisiert die Werte des Portfolio-Elements, z.B. durch Abrufen der aktuellen Kurse und Berechnung der Wertentwicklung."""
        self.wecheselkurs = hole_wechselkurs(self.waehrung)
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
        """Gibt eine Übersicht über das Portfolio-Element aus"""
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


class PortfolioManager:
    """Verwaltet das Portfolio, z.B. durch Hinzufügen von Elementen und Berechnung von Kennzahlen."""

    def __init__(self, name: str) -> None:
        self.name = name
        self.elements = []

    def add(self, element: PortfolioElement) -> None:
        """Fügt ein Portfolio-Element zum Portfolio hinzu."""
        self.elements.append(element)

    def load_from_json(self, filename: str) -> None:
        """Einlesen der Daten aus der JSON-Datei"""
        with open(filename, 'r') as f:
            data = json.load(f)
        # Iteration über die Daten und Hinzufügen von Portfolio-Elementen zum Portfolio-Manager
        for name, details in data.items():
            self.add(PortfolioElement(details["isin"], details["stueckzahl"], details["kurs_beobachtung"]))

    def save(self, filename: str) -> None:
        """Speichern der Daten in einer JSON-Datei"""
        data = {}
        for element in self.elements:
            data[element.isin] = {
                "name": element.name,
                "stueckzahl": element.stueckzahl,
                "kurs_beobachtung": element.kurs_beobachtung
            }
        with open(filename, 'w') as f:
            json.dump(data, f, indent=4)

    def update(self) -> None:
        """Aktualisiert die Werte aller Portfolio-Elemente und berechnet die Gesamtwerte für das Portfolio."""
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
        """Gibt eine Übersicht über das Portfolio aus, z.B. in Form einer Tabelle."""
        self.update()
        table = Table(title=self.name, box=box.HEAVY_EDGE)
        table.add_column("Name", justify="left", style="cyan", no_wrap=True)
        table.add_column("ISIN", justify="left", style="white")
        table.add_column("Anzahl", justify="right", style="magenta")
        table.add_column("Währung", justify="right", style="green")
        table.add_column("BK", justify="right", style="yellow")
        table.add_column("BW", justify="right", style="yellow")
        table.add_column("AK", justify="right", style="yellow")
        table.add_column("AW", justify="right", style="yellow")
        table.add_column("WE-Tag", justify="right")
        table.add_column("WE-Tag %", justify="right")
        table.add_column("WE-Gesamt", justify="right")
        table.add_column("WE-Gesamt %", justify="right")
        for el in self.elements:
            we_tag_color = "red" if el.wertenwicklung_tag < 0 else "green"
            we_tag_prz_color = "red" if el.wertenwicklung_tag_prozent < 0 else "green"
            we_gesamt_color = "red" if el.wertenwicklung_gesamt < 0 else "green"
            we_gesamt_prz_color = "red" if el.wertenwicklung_gesamt_prozent < 0 else "green"
            table.add_row(
                el.name, el.isin,
                f"{el.stueckzahl:.1f}", el.waehrung, f"{el.kurs_beobachtung:.2f}", f"{el.wert_beobachtung:.2f}",
                f"{el.kurs_aktuell:.2f}", f"{el.wert_aktuell:.2f}",
                f"[{we_tag_color}]{el.wertenwicklung_tag:.2f}[/{we_tag_color}]",
                f"[{we_tag_prz_color}]{el.wertenwicklung_tag_prozent:.1f}%[/{we_tag_prz_color}]",
                f"[{we_gesamt_color}]{el.wertenwicklung_gesamt:.2f}[/{we_gesamt_color}]",
                f"[{we_gesamt_prz_color}]{el.wertenwicklung_gesamt_prozent:.2f}%[/{we_gesamt_prz_color}]"
            )
        console = Console()
        console.print(table)
        print(f"Portfolio Beobachtungsgesamtwert [EUR]: {self.portfolio_wert_beobachtung:10.2f}")
        print(f"  Portfolio aktueller Gesamtwert [EUR]: {self.portfolio_wert_aktuell:10.2f}")
        print(f" Portfolio Gesamtwertentwicklung [EUR]: {self.portfolio_wertenwicklung_gesamt:10.2f} ({self.portfolio_wertenwicklung_gesamt_prozent:.2f}%)")
        print(f"  Portfolio Tageswertentwicklung [EUR]: {self.portfolio_wertenwicklung_tag:10.2f} ({self.portfolio_wertenwicklung_tag_prozent:.2f}%)")
        print()

    def ask_ai(self, zeithorizont_in_jahren:int=10, risikoprofil:str="gering") -> None:
        """Fragt die KI nach einer Einschätzung zum Portfolio, z.B. in Bezug auf die aktuelle Marktsituation oder mögliche Anlagestrategien."""
        sys_msg = (
            "Du bist ein Experte für Aktien, ETF's und Anlagestrategien.\n"
            "Bewerte das folgende Aktien/ETF Portfolio in Bezug auf Chancen und Risiken für einen Vermögensaufbau.\n"
            f"Zeithorizont: {zeithorizont_in_jahren} Jahre.\n"
            f"Risikoprofil: {risikoprofil}.\n"
        )
        msg = ["Das Portfolio besteht aus folgenden Elementen:"]
        for element in self.elements:
            msg.append(
                f"- {element.name} (ISIN: {element.isin}, "
                f"Portfolioanteil: {element.wert_aktuell / self.portfolio_wert_aktuell * 100:.1f} %, "
                f"Kaufkurs: {element.kurs_beobachtung:.1f} EUR, "
                f"Aktueller Kurs: {element.kurs_aktuell:.1f} EUR)"
            )

        print(sys_msg)
        print("\n".join(msg))

        import json

        with open("secrets.json") as f:
            secrets = json.load(f)
            
        GOOGLE_API_KEY = secrets.get("GOOGLE_API_KEY")

        from langchain_google_genai import ChatGoogleGenerativeAI

        llm = ChatGoogleGenerativeAI(
            model="gemini-2.5-flash",
            api_key=GOOGLE_API_KEY,
        )

        from langchain_core.messages import SystemMessage, HumanMessage
        system_msg = SystemMessage(sys_msg)
        human_msg = HumanMessage("\n".join(msg))

        messages = [system_msg, human_msg]
        response = llm.invoke(messages)

        from rich.console import Console
        from rich.markdown import Markdown

        console = Console()
        md = Markdown(response.content)
        console.print(md)

if __name__ == "__main__":

    portfolio = PortfolioManager("Mein Portfolio")
    portfolio.load_from_json("portfolio.json")
    portfolio.info()
    portfolio.ask_ai(zeithorizont_in_jahren=15, risikoprofil="mittel")