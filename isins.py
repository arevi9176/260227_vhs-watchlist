"""
Die ISIN (International Securities Identification Number) ist ein weltweit einheitlicher, zwölf-
telliger alphanumerischer Code zur eindeutigen Identifizierung von Wertpapieren (Aktien, Anleihen, Fonds).
Sie dient der Standardisierung im internationalen Börsenhandel, besteht aus
 - Länderkennung
 - nationalem Code
 - Prüfziffer

Aufbau:
Ländercode (2 Stellen):  Repräsentiert das Land des Emittenten (z.B. "DE" für Deutschland, "US" für USA).
Basisnummer (9 Stellen): Identifiziert das Wertpapier spezifisch (oft basierend auf der nationalen Kennnummer).
Prüfziffer (1 Stelle):   Dient der Validierung.

Jedes Wertpapier hat eine eigene, unverwechselbare ISIN.
"""

DAX = {
    "adidas": "DE000A1EWWW0",
    "Airbus": "NL0000235190",
    "Allianz": "DE0008404005",
    "BASF": "DE000BASF111",
    "Bayer": "DE000BAY0017",
    "Beiersdorf": "DE0005200000",
    "BMW": "DE0005190003",
    "Brenntag": "DE000A1DAHH0",
    "Commerzbank": "DE000CBK1001",
    "Continental": "DE0005439004",
    "Daimler Truck": "DE000DTR0CK8",
    "Deutsche Bank": "DE0005140008",
    "Deutsche Börse": "DE0005810055",
    "Deutsche Telekom": "DE0005557508",
    "DHL Group": "DE0005552004",
    "E.ON": "DE000ENAG999",
    "Fresenius": "DE0005785604",
    "Fresenius Medical Care": "DE0005785802",
    "GEA": "DE0006602006",
    "Hannover Rück": "DE0008402215",
    "Heidelberg Materials": "DE0006047004",
    "Henkel vz.": "DE0006048432",
    "Infineon": "DE0006231004",
    "Mercedes-Benz Group": "DE0007100000",
    "Merck": "DE0006599905",
    "MTU Aero Engines": "DE000A0D9PT0",
    "Münchener Rück": "DE0008430026",
    "Porsche Automobil": "DE000PAH0038",
    "QIAGEN": "NL0015002SN0",
    "Rheinmetall": "DE0007030009",
    "RWE": "DE0007037129",
    "SAP": "DE0007164600",
    "Scout24": "DE000A12DM80",
    "Siemens": "DE0007236101",
    "Siemens Energy": "DE000ENER6Y0",
    "Siemens Healthineers": "DE000SHL1006",
    "Symrise": "DE000SYM9999",
    "Volkswagen (VW) vz.": "DE0007664039",
    "Vonovia": "DE000A1ML7J1",
    "Zalando": "DE000ZAL1111"
}
