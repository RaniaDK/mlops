# ===== 1. Importer les bibliothèques =====
from typing import Literal
import mlflow
import mlflow.sklearn
import pandas as pd
from fastapi import FastAPI
from pydantic import BaseModel

# ===== 2. Créer l'application =====
app = FastAPI(title="API Churn")

# ===== 3. Charger le modèle champion au démarrage =====
mlflow.set_tracking_uri("sqlite:///mlflow.db")
model = mlflow.sklearn.load_model("models:/churn-model@champion")

# ===== 4. Décrire les données reçues =====
class Client(BaseModel):
    age: int
    salaire: float
    abonnement: Literal["Basique", "Standard", "Premium"]
    anciennete: float
    consommation: float

# ===== 5. Route /health =====
@app.get("/health")
def health():
    return {"status": "ok"}

# ===== 6. Route /predict =====
@app.post("/predict")
def predict(client: Client):

    # a) Transformer le client en tableau
    ligne = pd.DataFrame([client.model_dump()])

    # b) Transformer l'abonnement en colonnes numériques
    ligne = pd.get_dummies(ligne)

    # c) Garder les variables attendues par le modèle
    ligne = ligne.reindex(
        columns=model.feature_names_in_,
        fill_value=0
    )

    # d) Effectuer la prédiction
    resultat = int(model.predict(ligne)[0])

    return {
        "churn": resultat,
        "message": "Le client va partir" if resultat == 1 else "Le client reste"
    }