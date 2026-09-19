"""
Wrapper pour l'API du fournisseur SMM (format standard utilisé par la
majorité des panels : SMMKing, JustAnotherPanel, Peakerr, SMMflow, etc.)

Documentation à vérifier chez ton fournisseur une fois inscrit — le format
ci-dessous est le plus courant (API v2 "type SMM panel").
"""

import requests
from config import SMM_API_URL, SMM_API_KEY


def lister_services_fournisseur():
    """Récupère la liste des services disponibles chez le fournisseur.
    Utile pour retrouver les vrais service_id_provider à mettre dans config.py"""
    payload = {"key": SMM_API_KEY, "action": "services"}
    r = requests.post(SMM_API_URL, data=payload, timeout=15)
    r.raise_for_status()
    return r.json()


def passer_commande(service_id_provider: int, lien: str, quantite: int):
    """Envoie la commande au fournisseur. Retourne l'order_id fournisseur."""
    payload = {
        "key": SMM_API_KEY,
        "action": "add",
        "service": service_id_provider,
        "link": lien,
        "quantity": quantite,
    }
    r = requests.post(SMM_API_URL, data=payload, timeout=15)
    r.raise_for_status()
    data = r.json()
    if "order" in data:
        return str(data["order"])
    raise RuntimeError(f"Réponse inattendue du fournisseur : {data}")


def statut_commande(order_id_provider: str):
    """Vérifie le statut d'une commande chez le fournisseur."""
    payload = {
        "key": SMM_API_KEY,
        "action": "status",
        "order": order_id_provider,
    }
    r = requests.post(SMM_API_URL, data=payload, timeout=15)
    r.raise_for_status()
    return r.json()


def solde_compte():
    """Vérifie ton solde disponible chez le fournisseur."""
    payload = {"key": SMM_API_KEY, "action": "balance"}
    r = requests.post(SMM_API_URL, data=payload, timeout=15)
    r.raise_for_status()
    return r.json()
