
import pandas as pd
import numpy as np

# Fixer la graine aléatoire pour obtenir les mêmes résultats
np.random.seed(42)

# Nombre de clients fictifs
n = 500

# Générer les données des clients
data = pd.DataFrame({
    "age": np.random.randint(18, 70, n),
    "salaire": np.random.randint(1200, 8000, n),
    "abonnement": np.random.choice(
        ["Basique", "Standard", "Premium"], n
    ),
    "anciennete": np.random.randint(0, 15, n),
    "consommation": np.random.randint(0, 100, n)
})

# Créer la variable cible : churn
data["churn"] = (
    (data["consommation"] < 30) &
    (data["anciennete"] < 2)
).astype(int)

# Enregistrer les données dans un fichier CSV
data.to_csv("churn_data.csv", index=False)

# Afficher les 5 premières lignes
print(data.head())

# Afficher le taux de churn
print(f"Taux de churn : {data['churn'].mean():.1%}")
