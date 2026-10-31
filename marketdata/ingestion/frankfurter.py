from datetime import date
from decimal import Decimal
import requests
from marketdata.ingestion.base_donnees import connexion

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




SQL_SERIE = "SELECT id FROM serie WHERE source = %s AND code = %s"

SQL_UPSERT = """
    INSERT INTO observation (serie_id, date_observation, valeur)
    VALUES (%s, %s, %s)
    ON CONFLICT (serie_id, date_observation) DO UPDATE
      SET valeur = EXCLUDED.valeur,
          date_ingestion = now()
      WHERE observation.valeur IS DISTINCT FROM EXCLUDED.valeur
"""


def charger(lignes: list[tuple], source: str) -> int:
    """Insère ou met à jour les observations. Renvoie le nombre de lignes traitées."""
    with connexion() as conn:
        with conn.cursor() as curseur:
            identifiants = {}
            a_charger = []

            for code, jour, valeur in lignes:
                if code not in identifiants:
                    curseur.execute(SQL_SERIE, (source, code))
                    resultat = curseur.fetchone()
                    if resultat is None :
                        raise ValueError(f"Série inconnue en base : {source} / {code}")
                    identifiants[code] = resultat[0]

                a_charger.append((identifiants[code], jour, valeur ))

            curseur.executemany(SQL_UPSERT, a_charger)
            return len(a_charger)


SQL_JOURNAL_OUVRIR = """
    INSERT INTO ingestion_log (source, statut)
    VALUES (%s, 'en_cours')
    RETURNING id
"""

SQL_JOURNAL_FERMER = """
    UPDATE ingestion_log
       SET fin = now(), statut = %s, lignes_traitees = %s, message = %s
     WHERE id = %s
"""


def _ouvrir_journal(source: str) -> int:
    with connexion() as conn:
        with conn.cursor() as curseur:
            curseur.execute(SQL_JOURNAL_OUVRIR, (source,))
            return curseur.fetchone()[0]


def _fermer_journal(id_log: int, statut: str, lignes_traitees, message) -> None:
    with connexion() as conn:
        with conn.cursor() as curseur:
            curseur.execute(
                SQL_JOURNAL_FERMER, (statut, lignes_traitees, message, id_log)
            )


def executer(debut: date, fin: date, devise_cible: str = "USD") -> int:
    """Chaîne complète : extraction, traduction, chargement, journalisation."""
    source = "frankfurter"
    id_log = _ouvrir_journal(source)
    try:
        donnees = extraire(debut, fin, devise_cible)
        lignes  = transformer(donnees, devise_cible)
        nombre  = charger(lignes, source)
    except Exception as erreur:
        _fermer_journal(id_log, "echec", None, str(erreur))
        raise
    _fermer_journal(id_log, "succes", nombre, None)
    return nombre