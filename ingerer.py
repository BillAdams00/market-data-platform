from datetime import date

from marketdata.ingestion import frankfurter

nombre = frankfurter.executer(date(2026, 10, 1), date(2026, 10, 31))
print(f"{nombre} observations traitées")