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


class Order:
    def __init__(self, **kwargs):
        self.id = kwargs.get("id")
        self.client_nom = kwargs.get("client_nom", "")
        self.client_whatsapp = kwargs.get("client_whatsapp", "")
        self.service_nom = kwargs.get("service_nom", "")
        self.service_id_provider = kwargs.get("service_id_provider")
        self.lien_cible = kwargs.get("lien_cible", "")
        self.quantite = kwargs.get("quantite", 0)
        self.prix_vente_cdf = kwargs.get("prix_vente_cdf", 0)
        self.reference_paiement = kwargs.get("reference_paiement")
        self.statut = kwargs.get("statut", "en_attente_paiement")
        self.order_id_provider = kwargs.get("order_id_provider")
        self.date_creation = kwargs.get("date_creation") or datetime.utcnow().isoformat()

    def save(self):
        conn = get_conn()
        if self.id is None:
            cur = conn.execute("""
                INSERT INTO orders
                (client_nom, client_whatsapp, service_nom, service_id_provider,
                 lien_cible, quantite, prix_vente_cdf, reference_paiement,
                 statut, order_id_provider, date_creation)
                VALUES (?,?,?,?,?,?,?,?,?,?,?)
            """, (self.client_nom, self.client_whatsapp, self.service_nom,
                  self.service_id_provider, self.lien_cible, self.quantite,
                  self.prix_vente_cdf, self.reference_paiement, self.statut,
                  self.order_id_provider, self.date_creation))
            self.id = cur.lastrowid
        else:
            conn.execute("""
                UPDATE orders SET client_nom=?, client_whatsapp=?, service_nom=?,
                    service_id_provider=?, lien_cible=?, quantite=?, prix_vente_cdf=?,
                    reference_paiement=?, statut=?, order_id_provider=?
                WHERE id=?
            """, (self.client_nom, self.client_whatsapp, self.service_nom,
                  self.service_id_provider, self.lien_cible, self.quantite,
                  self.prix_vente_cdf, self.reference_paiement, self.statut,
                  self.order_id_provider, self.id))
        conn.commit()
        conn.close()
        return self

    @staticmethod
    def get(order_id):
        conn = get_conn()
        row = conn.execute("SELECT * FROM orders WHERE id=?", (order_id,)).fetchone()
        conn.close()
        return Order(**dict(row)) if row else None

    @staticmethod
    def all_desc():
        conn = get_conn()
        rows = conn.execute("SELECT * FROM orders ORDER BY id DESC").fetchall()
        conn.close()
        return [Order(**dict(r)) for r in rows]

    def date_affichee(self):
        try:
            return datetime.fromisoformat(self.date_creation).strftime("%d/%m/%Y %H:%M")
        except Exception:
            return self.date_creation
