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


@app.route("/test-api")
def test_api():
    try:
        solde = services_api.solde_compte()
        return f"Connexion réussie ! Résultat : {solde}"
    except Exception as e:
        return f"Erreur : {e}"


@app.route("/")
def index():
    return render_template("index.html", services=SERVICES, usd_to_cdf=USD_TO_CDF)


@app.route("/commander", methods=["GET", "POST"])
def commander():
    service_nom = request.args.get("service") or request.form.get("service")
    service = trouver_service(service_nom)
    if not service:
        flash("Service introuvable.")
        return redirect(url_for("index"))

    if request.method == "POST":
        quantite = int(request.form["quantite"])
        if quantite < service["min"] or quantite > service["max"]:
            flash(f"Quantité doit être entre {service['min']} et {service['max']}.")
            return render_template("commander.html", service=service, usd_to_cdf=USD_TO_CDF)

        prix_cdf = prix_vente_cdf(service, quantite)

        order = Order(
            client_nom=request.form.get("nom", ""),
            client_whatsapp=request.form.get("whatsapp", ""),
            service_nom=service["nom"],
            service_id_provider=service["service_id_provider"],
            lien_cible=request.form["lien"],
            quantite=quantite,
            prix_vente_cdf=prix_cdf,
            statut="en_attente_paiement",
        ).save()

        message = (
            f"Bonjour, je viens de commander sur PattyBoost :\n"
            f"Commande #{order.id} - {service['nom']} x{quantite}\n"
            f"Lien : {order.lien_cible}\n"
            f"Montant : {prix_cdf} CDF\n"
            f"Je vous envoie la preuve de paiement Mobile Money ici."
        )
        lien_whatsapp = (
            f"https://wa.me/{WHATSAPP_NUMBER}?text={urllib.parse.quote(message)}"
        )
        return render_template(
            "confirmation.html", order=order, lien_whatsapp=lien_whatsapp
        )

    return render_template("commander.html", service=service, usd_to_cdf=USD_TO_CDF)


@app.route("/suivi")
def suivi():
    ref = request.args.get("ref", "")
    order = Order.get(int(ref)) if ref.isdigit() else None
    return render_template("suivi.html", order=order)


def admin_requis(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        if not session.get("admin"):
            return redirect(url_for("admin_login"))
        return f(*args, **kwargs)
    return wrapper


@app.route("/admin/login", methods=["GET", "POST"])
def admin_login():
    if request.method == "POST":
        if request.form.get("mot_de_passe") == ADMIN_PASSWORD:
            session["admin"] = True
            return redirect(url_for("admin_dashboard"))
        flash("Mot de passe incorrect.")
    return render_template("admin_login.html")


@app.route("/admin/logout")
def admin_logout():
    session.pop("admin", None)
    return redirect(url_for("admin_login"))


@app.route("/admin")
@admin_requis
def admin_dashboard():
    commandes = Order.all_desc()
    return render_template("admin_dashboard.html", commandes=commandes)


@app.route("/admin/valider/<int:order_id>", methods=["POST"])
@admin_requis
def admin_valider(order_id):
    order = Order.get(order_id)
    if not order:
        return redirect(url_for("admin_dashboard"))

    order.statut = "paiement_recu"
    order.save()

    try:
        order_id_provider = services_api.passer_commande(
            order.service_id_provider, order.lien_cible, order.quantite
        )
        order.order_id_provider = order_id_provider
        order.statut = "envoyee_au_fournisseur"
        order.save()
        flash(f"Commande #{order.id} envoyée au fournisseur (ref {order_id_provider}).")
    except Exception as e:
        flash(f"Erreur envoi fournisseur : {e}. Vérifie config.py (clé API).")

    return redirect(url_for("admin_dashboard"))


@app.route("/admin/verifier/<int:order_id>", methods=["POST"])
@admin_requis
def admin_verifier_statut(order_id):
    order = Order.get(order_id)
    if order and order.order_id_provider:
        try:
            data = services_api.statut_commande(order.order_id_provider)
            statut_fournisseur = data.get("status", "").lower()
            if statut_fournisseur == "completed":
                order.statut = "terminee"
            elif statut_fournisseur in ("in progress", "processing"):
                order.statut = "en_cours"
            order.save()
            flash(f"Statut fournisseur : {data.get('status')}")
        except Exception as e:
            flash(f"Erreur vérification : {e}")
    return redirect(url_for("admin_dashboard"))


if __name__ == "__main__":
    app.run(debug=True)
