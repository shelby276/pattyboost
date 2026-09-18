"""
Configuration de PattyBoost.
Remplis les valeurs API_URL / API_KEY une fois ton compte fournisseur SMM créé.
"""

import os

SMM_API_URL = os.environ.get("SMM_API_URL", "https://smmkings.com/api/v2")
SMM_API_KEY = os.environ.get("SMM_API_KEY", "COLLE_TA_CLE_API_ICI")

ADMIN_PASSWORD = os.environ.get("ADMIN_PASSWORD", "changeMoi123")

WHATSAPP_NUMBER = os.environ.get("WHATSAPP_NUMBER", "243987167271")

SQLALCHEMY_DATABASE_URI = "sqlite:///pattyboost.db"
SECRET_KEY = os.environ.get("SECRET_KEY", "dev-secret-change-en-prod")

SERVICES = [
    {
        "nom": "Abonnés Instagram",
        "plateforme": "Instagram",
        "service_id_provider": 1,
        "prix_achat_usd1000": 1.20,
        "prix_vente_usd1000": 3.00,
        "min": 100,
        "max": 10000,
    },
    {
        "nom": "Likes Instagram",
        "plateforme": "Instagram",
        "service_id_provider": 2,
        "prix_achat_usd1000": 0.40,
        "prix_vente_usd1000": 1.20,
        "min": 50,
        "max": 20000,
    },
    {
        "nom": "Vues Instagram/TikTok",
        "plateforme": "TikTok",
        "service_id_provider": 3,
        "prix_achat_usd1000": 0.08,
        "prix_vente_usd1000": 0.40,
        "min": 100,
        "max": 1000000,
    },
    {
        "nom": "Abonnés TikTok",
        "plateforme": "TikTok",
        "service_id_provider": 4,
        "prix_achat_usd1000": 1.50,
        "prix_vente_usd1000": 3.50,
        "min": 100,
        "max": 10000,
    },
    {
        "nom": "Likes Facebook (page)",
        "plateforme": "Facebook",
        "service_id_provider": 5,
        "prix_achat_usd1000": 1.00,
        "prix_vente_usd1000": 2.80,
        "min": 100,
        "max": 5000,
    },
    {
        "nom": "Abonnés Facebook",
        "plateforme": "Facebook",
        "service_id_provider": 6,
        "prix_achat_usd1000": 1.80,
        "prix_vente_usd1000": 4.00,
        "min": 100,
        "max": 5000,
    },
]

USD_TO_CDF = 2800
