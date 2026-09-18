"""
Configuration de PattyBoost.
Remplis les valeurs API_URL / API_KEY une fois ton compte fournisseur SMM créé.
"""

import os

# --- Fournisseur SMM (à remplir après inscription, voir README.md) ---
SMM_API_URL = os.environ.get("SMM_API_URL", "https://provider.example.com/api/v2")
SMM_API_KEY = os.environ.get("SMM_API_KEY", "COLLE_TA_CLE_API_ICI")

# --- Sécurité admin (CHANGE CE MOT DE PASSE avant mise en ligne) ---
ADMIN_PASSWORD = os.environ.get("ADMIN_PASSWORD", "changeMoi123")

# --- WhatsApp de contact (format international sans le +) ---
WHATSAPP_NUMBER = os.environ.get("WHATSAPP_NUMBER", "243987167271")

# --- Base de données ---
SQLALCHEMY_DATABASE_URI = "sqlite:///pattyboost.db"
SECRET_KEY = os.environ.get("SECRET_KEY", "dev-secret-change-en-prod")

# ---------------------------------------------------------------------
# CATALOGUE DE SERVICES avec prix suggérés (marge ~50-70%).
# "service_id_provider" = l'ID du service chez TON fournisseur SMM
# (tu le trouves via l'action "services" de leur API, voir README.md)
# prix_achat_usd1000 = ce que TE facture le fournisseur pour 1000 unités
# prix_vente_usd1000 = ce que TU factures au client pour 1000 unités
# ---------------------------------------------------------------------
SERVICES = [
    {
        "nom": "Abonnés Instagram",
        "plateforme": "Instagram",
