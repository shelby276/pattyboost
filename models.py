import sqlite3
from datetime import datetime

DB_PATH = "pattyboost.db"


def get_conn():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_conn()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS orders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            client_nom TEXT,
            client_whatsapp TEXT,
            service_nom TEXT,
            service_id_provider INTEGER,
            lien_cible TEXT,
            quantite INTEGER,
            prix_vente_cdf REAL,
            reference_paiement TEXT,
            statut TEXT DEFAULT 'en_attente_paiement',
            order_id_provider TEXT,
            date_creation TEXT
        )
    """)
    conn.commit()
    conn.close()

