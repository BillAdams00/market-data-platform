from datetime import date

from marketdata.ingestion import alphavantage, frankfurter

print(frankfurter.executer(date(2026, 10, 1), date(2026, 10, 31)), "taux de change")
print(alphavantage.executer("NVDA"), "cours")