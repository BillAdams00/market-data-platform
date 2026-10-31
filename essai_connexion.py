from marketdata.ingestion.base_donnees import connexion

with connexion() as conn:
    with conn.cursor() as curseur:
        curseur.execute("SELECT count(*) FROM observation;")
        print(curseur.fetchone())