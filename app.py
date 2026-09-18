from flask import Flask, render_template, request, redirect, url_for, session, flash
from functools import wraps
import urllib.parse

from config import (
    SECRET_KEY, SERVICES, USD_TO_CDF,
    WHATSAPP_NUMBER, ADMIN_PASSWORD,
)
from models import init_db, Order
import services_api

app = Flask(__name__)
app.config["SECRET_KEY"] = SECRET_KEY

init_db()


def prix_vente_cdf(service, quantite):
    prix_usd = (service["prix_vente_usd1000"] / 1000) * quantite
    return round(prix_usd * USD_TO_CDF)


def trouver_service(nom):
    return next((s for s in SERVICES if s["nom"] == nom), None)


# ---------------------------------------------------------------- PUBLIC ----

@app.route("/")
def index():
    return render_template("index.html", services=SERVICES, usd_to_cdf=USD_TO_CDF)

