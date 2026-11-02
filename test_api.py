import requests

URL = "http://localhost:8000"

# ===== 1. Vérifier que l'API fonctionne =====
print("GET /health ->", requests.get(URL + "/health").json())

# ===== 2. Tester avec un client à faible consommation =====
client = {
    "age": 35,
    "salaire": 2500,
    "abonnement": "Standard",
    "anciennete": 1,
    "consommation": 10
}

r = requests.post(URL + "/predict", json=client)
print("POST /predict (client 1) ->", r.status_code, r.json())

# ===== 3. Tester avec un client fidèle =====
client2 = {
    "age": 50,
    "salaire": 4000,
    "abonnement": "Premium",
    "anciennete": 10,
    "consommation": 80
}

r = requests.post(URL + "/predict", json=client2)
print("POST /predict (client 2) ->", r.status_code, r.json())

# ===== 4. Tester une erreur de validation =====
mauvais = dict(client, age="abc")

r = requests.post(URL + "/predict", json=mauvais)

print("POST /predict (age='abc') ->", r.status_code)
print("Message :", r.json()["detail"][0]["msg"])