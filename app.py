
# ===== 1. Importer les bibliothèques =====
import os
from typing import Literal

import mlflow
import mlflow.sklearn
import pandas as pd

from fastapi import FastAPI
from pydantic import BaseModel


# ===== 2. Créer l'application =====
app = FastAPI(title="API Churn")


# ===== 3. Lire la configuration dans les variables d'environnement =====
TRACKING_URI = os.getenv("MLFLOW_TRACKING_URI", "sqlite:///mlflow.db")
MODEL_URI = os.getenv("MODEL_URI", "models:/churn-model@champion")


# ===== 4. Charger le champion UNE SEULE FOIS, au démarrage =====
mlflow.set_tracking_uri(TRACKING_URI)

model = mlflow.sklearn.load_model(MODEL_URI)

print(f"Modèle chargé depuis : {MODEL_URI}")


# ===== 5. Décrire les données attendues =====
class Client(BaseModel):
    age: int
    salaire: float
    abonnement: Literal["Basique", "Standard", "Premium"]
    anciennete: float
    consommation: float


# ===== 6. Route /health =====
@app.get("/health")
def health():
    return {"status": "ok"}


# ===== 7. Route /predict =====
@app.post("/predict")
def predict(client: Client):

    # a) Transformer le client reçu en DataFrame
    ligne = pd.DataFrame([client.model_dump()])

    # b) Transformer abonnement en colonnes 0/1
    ligne = pd.get_dummies(ligne)

    # c) Garder les colonnes du modèle dans le bon ordre
    ligne = ligne.reindex(
        columns=model.feature_names_in_,
        fill_value=0
    )

    # d) Effectuer la prédiction
    # 1 = le client part, 0 = le client reste
    resultat = int(model.predict(ligne)[0])

    return {
        "churn": resultat,
        "message": "Le client va partir" if resultat == 1 else "Le client reste"
    }
