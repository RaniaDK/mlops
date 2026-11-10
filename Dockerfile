
# 1. Image de base : Linux minimal avec Python 3.11
FROM python:3.11-slim

# 2. Définir le dossier de travail
WORKDIR /app

# 3. Copier et installer les dépendances
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 4. Copier le code et le modèle
COPY app.py .
COPY model/ model/

# 5. Charger le modèle depuis le dossier model par défaut
ENV MODEL_URI=model

# 6. Documenter le port utilisé par l'API
EXPOSE 8000

# 7. Démarrer l'API FastAPI
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
