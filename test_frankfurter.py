from datetime import date
from decimal import Decimal

from marketdata.ingestion.frankfurter import transformer


REPONSE = {
    "amount": 1.0,
    "base": "EUR",
    "start_date": "2026-10-15",
    "end_date": "2026-10-20",
    "rates": {
        "2026-10-15": {"USD": 1.1208},
        "2026-10-16": {"USD": 1.1253},
        "2026-10-19": {"USD": 1.1225},
        "2026-10-20": {"USD": 1.1215},
    },
}


REPONSE_DEUX_DEVISES = {
    "amount": 1.0,
    "base": "EUR",
    "rates": {
        "2026-10-20": {"USD": 1.1215, "GBP": 0.8712},
    },
}
def test_une_ligne_par_date():
    lignes = transformer(REPONSE, "USD")
    assert len(lignes) == 4
    
def test_format_pivot():
    lignes = transformer(REPONSE, "USD")
    assert lignes[0] == ("EURUSD", date(2026, 10, 15), Decimal("1.1208"))


def test_types_convertis():
    code, jour, valeur = transformer(REPONSE, "USD")[0]
    assert isinstance(jour, date)
    assert isinstance(valeur, Decimal)


def test_devise_demandee():
    lignes = transformer(REPONSE_DEUX_DEVISES, "GBP")
    assert lignes[0] == ("EURGBP", date(2026, 10, 20), Decimal("0.8712"))