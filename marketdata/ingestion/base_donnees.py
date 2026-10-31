import os

import psycopg
from dotenv import load_dotenv

load_dotenv()


def connexion():
    """Ouvre une connexion à marketdb à partir des variables du .env."""
    return psycopg.connect(
        host=os.environ["PGHOST"],
        port=os.environ["PGPORT"],
        dbname=os.environ["PGDATABASE"],
        user=os.environ["PGUSER"],
        password=os.environ["PGPASSWORD"],
    )