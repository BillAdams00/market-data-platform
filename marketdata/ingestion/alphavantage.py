from datetime import date
from decimal import Decimal
import os

import requests
from dotenv import load_dotenv

load_dotenv()

SOURCE = "alphavantage"
CLE_META_DATA = "Meta Data"
CLE_SERIE_TEMPORELLE = "Time Series (Daily)"
CLE_SYMBOLE = "2. Symbol"
CLE_CLOTURE = "4. close"


def transformer(donnees: dict, champ: str = CLE_CLOTURE) -> list[tuple]:
    """Traduit une réponse Alpha Vantage en triplets (code_serie, date, valeur)."""
    code_serie = donnees[CLE_META_DATA][CLE_SYMBOLE]
    lignes = []
    for jour, cotations in donnees[CLE_SERIE_TEMPORELLE].items():
        lignes.append((
            code_serie,
            date.fromisoformat(jour),
           Decimal(cotations["1. open"]),
        ))
    return lignes



URL_BASE = "https://www.alphavantage.co/query"


def extraire(symbole: str, taille: str = "compact") -> dict:
    """Appelle Alpha Vantage et renvoie la réponse JSON telle quelle."""
    reponse = requests.get(
        URL_BASE,
        params={
            "function": "TIME_SERIES_DAILY",
            "symbol": symbole,
            "outputsize": taille,
            "apikey": os.environ["ALPHAVANTAGE_API_KEY"],
        },
        timeout=10,
    )
    reponse.raise_for_status()

    donnees = reponse.json()
    if CLE_SERIE_TEMPORELLE not in donnees:
        raise RuntimeError(
            f"Reponse Alpha Vantage inattendue, blocs recus : {list(donnees)}"
        )
    return donnees

from marketdata.ingestion import socle


def executer(symbole: str, champ: str = CLE_CLOTURE) -> int:
    """Chaîne complète pour un titre."""
    def produire():
        return transformer(extraire(symbole), champ)

    return socle.executer(SOURCE, produire)