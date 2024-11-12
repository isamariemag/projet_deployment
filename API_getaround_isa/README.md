# API Getaround Deployment Project ISA

## Histoire et contexte du projet
GetAround est l'Airbnb pour les voitures. Vous pouvez louer des voitures à n'importe qui pour quelques heures à quelques jours. Fondée en 2009, cette société a connu une croissance rapide. En 2019, ils comptent plus de 5 millions d'utilisateurs et environ 20 000 voitures disponibles dans le monde.  

PROBLEMATIQUE: En faisant partie de l'équipe de data science, l'objectif sera de travailler sur l'optimisation des prix de location de voiture en se basant sur la data collecté. 

## Introduction
Ce projet consiste à déployer une API permettant de prédire le prix de location des voitures sur la plateforme Getaround à l'aide du machine learning supervisé. Un modèle d'entraînement a été exporté dans une API afin de faire des prédictions sur les prix. L'API est en ligne et a été déployer sur le serveur Heroku. 

## Lien vers l'API (avec HEROKU)
Vous pouvez accéder à l'API en utilisant le lien suivant :
[API Getaround - Documentation](https://api3isa-6632e09d7c30.herokuapp.com/docs#/default/predict_predict_post)

## Lien vers l'API (en LOCAL)
(http://127.0.0.1:8000/docs#/default/predict_predict_post)

## Lien de la vidéo de l'API (enregistrement de prédictions)
(https://www.loom.com/share/0f8359e8f6b9456681d93493475a8c6b?sid=91f2c6fe-8791-4f6c-9e47-ec101c102a4d)

## Dossier
- **API_getaround_isa** : Contient l'implémentation de l'API FastAPI pour la prédiction de prix de location.

## Instructions pour l'utilisation
- Pour accéder à l'API, visitez le lien fourni du "/docs#/" et utilisez `/predict` pour effectuer des prédictions.
- Pour tester l'API, aller dans "Request body" puis faire une requête au format JSON :
({
  "engine_power": 256,
  "automatic_car": false,
  "has_getaround_connect": true,
  "has_gps": true,
  "fuel": "diesel",
  "paint_color": "black",
  "car_type": "coupe"
})


