"""
Configuration de PattyBoost.
"""

import os

# --- Fournisseur SMM ---
SMM_API_URL = os.environ.get("SMM_API_URL", "https://smmkings.com/api/v2")
SMM_API_KEY = os.environ.get("SMM_API_KEY", "COLLE_TA_CLE_API_ICI")

# --- Sécurité admin (CHANGE CE MOT DE PASSE dans Render, pas ici) ---
ADMIN_PASSWORD = os.environ.get("ADMIN_PASSWORD", "changeMoi123")

# --- WhatsApp de contact (format international sans le +) ---
WHATSAPP_NUMBER = os.environ.get("WHATSAPP_NUMBER", "243987167271")

# --- Base de données ---
SECRET_KEY = os.environ.get("SECRET_KEY", "dev-secret-change-en-prod")

# ---------------------------------------------------------------------
# CATALOGUE DYNAMIQUE : au lieu d'une liste figée, le site récupère TOUS
# les services Instagram / TikTok / Facebook directement depuis SMMKing
# à chaque rafraîchissement du cache (voir services_api.obtenir_catalogue).
# ---------------------------------------------------------------------

# Mots-clés utilisés pour ne garder que les catégories de ces réseaux
# (insensible à la casse). Ajoute des mots si tu veux élargir (ex: "YouTube").
PLATEFORMES_AUTORISEES = ["Instagram", "TikTok", "Facebook"]

# Marge appliquée automatiquement : prix de vente = prix d'achat x MARKUP
# 3.0 = tu factures 3 fois le prix que te facture SMMKing.
MARKUP = 3.0

# Durée (en secondes) pendant laquelle la liste de services est gardée en
# mémoire avant d'être re-téléchargée depuis SMMKing (évite de ralentir le site).
CACHE_DUREE_SECONDES = 1800  # 30 minutes

# Taux indicatif USD -> CDF pour affichage (à ajuster régulièrement, le taux bouge)
USD_TO_CDF = 2800
