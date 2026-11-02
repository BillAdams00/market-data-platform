from datetime import date
from decimal import Decimal
import requests
from marketdata.ingestion.base_donnees import connexion
from marketdata.ingestion import socle             
 

URL_BASE = "https://api.frankfurter.dev/v1"



def extraire(debut: date, fin: date, devise_cible: str) -> dict:
    """Appelle Frankfurter et renvoie la réponse JSON telle quelle."""
    url = f"{URL_BASE}/{debut}..{fin}"
    reponse = requests.get(
        url,
        params={"base": "EUR", "symbols": devise_cible},
        timeout=10,
    )
    reponse.raise_for_status()
    return reponse.json(parse_float=Decimal)

def transformer(donnees: dict, devise_cible: str) -> list[tuple]:
    """Traduit une réponse Frankfurter en triplets (code_serie, date, valeur)."""
    code_serie = donnees["base"] + devise_cible
    lignes = []
    for dat,  cotation in donnees["rates"].items():
        lignes.append((
            code_serie,
            date.fromisoformat(dat),
            Decimal(str(cotation[devise_cible])),
        ))
    return lignes

# frankfurter.py

SOURCE = "frankfurter"


def executer(debut: date, fin: date, devise_cible: str = "USD") -> int:
    def produire():
        return transformer(extraire(debut, fin, devise_cible), devise_cible)

    return socle.executer(SOURCE, produire)