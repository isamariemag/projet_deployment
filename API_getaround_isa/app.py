from fastapi import FastAPI
from pydantic import BaseModel
import joblib
import numpy as np
import pandas as pd
import uvicorn

# Charger le préprocesseur et le modèle ML
preprocessor = joblib.load('/app/preprocessor.pkl')
model = joblib.load('/app/modele_isa24_logistic_regression.pkl')

# Créer l'application FastAPI
app = FastAPI()

# Définir le format des données d'entrée
class InputData(BaseModel):
    engine_power: int
    automatic_car: bool
    has_getaround_connect: bool
    has_gps: bool
    fuel: str
    paint_color: str
    car_type: str

# Point de terminaison racine pour éviter l'erreur 404
@app.get("/")
async def root():
    return {"message": "Bienvenue sur l'API de prédiction ! Utilisez /predict pour faire des prédictions."}

# Créer le point de terminaison /predict
@app.post("/predict")
async def predict(data: InputData):
    # Extraire les caractéristiques de l'objet data
    input_data = {
        "engine_power": [data.engine_power],
        "automatic_car": [int(data.automatic_car)],  # Convertir en int (0 ou 1)
        "has_getaround_connect": [int(data.has_getaround_connect)],  # Convertir en int (0 ou 1)
        "has_gps": [int(data.has_gps)],  # Convertir en int (0 ou 1)
        "fuel": [data.fuel],
        "paint_color": [data.paint_color],
        "car_type": [data.car_type]
    }

    # Convertir les données d'entrée en DataFrame
    input_df = pd.DataFrame(input_data)

    # Transformer les données d'entrée avec le préprocesseur
    input_preprocessed = preprocessor.transform(input_df)

    # Faire des prédictions
    predictions = model.predict(input_preprocessed)

    # Retourner les prédictions sous forme JSON
    return {"prediction": predictions.tolist()}

# Lancer l'application si ce fichier est exécuté directement
if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
