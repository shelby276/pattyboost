"""
Wrapper pour l'API du fournisseur SMM (SMMKing, format standard "API v2
type SMM panel" utilisé par la majorité des panels).
"""

import time
import requests
from config import (
    SMM_API_URL, SMM_API_KEY, PLATEFORMES_AUTORISEES, MARKUP,
    CACHE_DUREE_SECONDES,
)


def lister_services_fournisseur():
    """Récupère la liste BRUTE de tous les services du fournisseur."""
    payload = {"key": SMM_API_KEY, "action": "services"}
    r = requests.post(SMM_API_URL, data=payload, timeout=20)
    r.raise_for_status()
    return r.json()


def passer_commande(service_id_provider, lien: str, quantite: int):
    """Envoie la commande au fournisseur. Retourne l'order_id fournisseur."""
    payload = {
        "key": SMM_API_KEY,
        "action": "add",
        "service": service_id_provider,
        "link": lien,
        "quantity": quantite,
    }
    r = requests.post(SMM_API_URL, data=payload, timeout=20)
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
    r = requests.post(SMM_API_URL, data=payload, timeout=20)
    r.raise_for_status()
    return r.json()


def solde_compte():
    """Vérifie ton solde disponible chez le fournisseur."""
    payload = {"key": SMM_API_KEY, "action": "balance"}
    r = requests.post(SMM_API_URL, data=payload, timeout=20)
    r.raise_for_status()
    return r.json()


# ---------------------------------------------------------------------
# Catalogue dynamique : filtre + calcule les prix de vente, avec cache
# en mémoire pour ne pas re-télécharger des milliers de services à
# chaque visite du site.
# ---------------------------------------------------------------------
_cache = {"data": None, "timestamp": 0}


def obtenir_catalogue(forcer_rafraichissement: bool = False):
    """Retourne la liste filtrée (Instagram/TikTok/Facebook) des services,
    avec le prix de vente déjà calculé (prix_achat x MARKUP)."""
    maintenant = time.time()
    cache_perime = (maintenant - _cache["timestamp"]) > CACHE_DUREE_SECONDES

    if _cache["data"] is None or cache_perime or forcer_rafraichissement:
        tous = lister_services_fournisseur()
        filtres = []
        for s in tous:
            categorie = s.get("category", "") or ""
            correspond = any(
                mot.lower() in categorie.lower() for mot in PLATEFORMES_AUTORISEES
            )
            if not correspond:
                continue
            try:
                prix_achat = float(s["rate"])
                mini = int(float(s["min"]))
                maxi = int(float(s["max"]))
                service_id = s["service"]
                nom = s["name"]
            except (KeyError, ValueError, TypeError):
                continue

            filtres.append({
                "id": service_id,
                "nom": nom,
                "categorie": categorie,
                "min": mini,
                "max": maxi,
                "prix_achat_usd1000": prix_achat,
                "prix_vente_usd1000": round(prix_achat * MARKUP, 4),
            })

        filtres.sort(key=lambda s: (s["categorie"], s["prix_vente_usd1000"]))
        _cache["data"] = filtres
        _cache["timestamp"] = maintenant

    return _cache["data"]


def trouver_service_par_id(service_id):
    """Cherche un service par son ID dans le catalogue en cache."""
    service_id = str(service_id)
    for s in obtenir_catalogue():
        if str(s["id"]) == service_id:
            return s
    return None
