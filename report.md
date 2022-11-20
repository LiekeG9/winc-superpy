Inleiding
=========
De opdracht "SuperPy" was een opdracht met veel uitdagingen. Bij sommige details kon ik in de eerste instantie geen oplossing vinden. Door te zoeken op het internet en voorbeelden testen in separate testprojecten is het uiteindelijk gelukt om deze problemen op de lossen en in te bouwen in het hoofdproject.

Technische info
===============
Generieke functies
------------------
De opdracht is in kleine stukjes functionaliteit opgehakt en daarmee per stukje in een testapplicatie (try-out) uitgeprobeerd. Steeds kleine stukjes code gaan samenvoegen in main.py, bij die aanpak niet gelet op generiek maken van code die meerdere keren gebruikt kon worden.

Halverwege het project heb ik een refactorslag uitgevoerd en zoveel mogelijk dubbele code ontdubbeld (lees: omgezet in generieke functies). Hierbij is gebruik gemaakt van parameters met als voordeel dat deze functies (zoals het aanmaken van een id; zie onderstaand voorbeeld) telkens op meerdere plekken hergebruikt konden worden. Hetzelfde geldt voor de functie waarmee de output wordt getoond in de vorm van tabellen. 

```python
def GetNewId(fId, fList):
    fNewId = fId
    for obj in fList:
        for key, value in obj.__dict__.items():
            if key == "id":
                if value > fNewId:
                    fNewId = value
    fNewId = fNewId + 1
    return fNewId
```

Bedragen in NL-formaat
----------------------
Het systeem rekende bedragen uit met floats, waarbij standaard punten als decimaal teken en komma's per duizendtallen worden gebruikt. Ik wilde bedragen liever in het NL-formaat weergeven. Veel voorbeelden gezien die gericht waren op niet Europese formaten. Uiteindelijk locale module gevonden om NL-formaat te realiseren.

```python 
def FormatMoney(fValue):
    locale.setlocale(locale.LC_ALL, "nl_NL")
    tmpMoneyStr = locale.currency(fValue, grouping=True)
    return tmpMoneyStr
```

Opdrachten vanuit CMD (Argparse)
--------------------------------
Gezocht naar voorbeelden waarbij gebruik werd gemaakt van commando's die gebruik maken van paramaters, zowel verplichte als optionele, en die de mogelijkheid hebben meerdere commando's af te handelen (zoals bij report inventory/revenue/profit).De oplossing werd geboden in de vorm van hoofd- en sub-parsers.

Een andere uitdaging was het uitlezen van de argumenten. 
Tenslotte de datumformat naar een generiekformat gewijzigd. 

```python
def main_parser():
    parser = argparse.ArgumentParser(description='Welcome to the SuperPy command line parser')
    subparsers = parser.add_subparsers(dest='main_command', help='main command')
    parser.add_argument('-a', '--advance-time', type=int)

    a_parser = subparsers.add_parser('buy', help='buy product and add to inventory')
    a_parser.add_argument('-n', '--product-name', type=str, required=True)
    a_parser.add_argument('-p', '--price', type=float, required=True)
    a_parser.add_argument('-e', '--expiration-date', type=str, required=True)
    a_parser.set_defaults(func=buy)

[...]
```

