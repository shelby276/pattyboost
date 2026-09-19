        @app.route("/test-api")
def test_api():
    try:
        solde = services_api.solde_compte()
        return f"Connexion réussie ! Résultat : {solde}"
    except Exception as e:
        return f"Erreur : {e}"


@app.route("/liste-services")
def liste_services():
    try:
        services = services_api.lister_services_fournisseur()
        return {"services": services}
    except Exception as e:
        return f"Erreur : {e}"


@app.route("/")
def index():
