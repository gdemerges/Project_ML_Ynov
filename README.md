# Project_ML_Ynov - Student Depression Prediction 🧠

Projet de mise en production et déploiement continu d'un modèle de Machine Learning pour la prédiction de la dépression chez les étudiants.

## 📋 Description

Ce projet implémente une solution complète de ML en production avec :
- ✅ **Interface web (Streamlit)** - Application de prédiction interactive
- 🔄 **API de serving (FastAPI)** - Endpoint de prédiction et feedback
- 📊 **Système de reporting (Evidently)** - Suivi des performances
- 🐳 **Conteneurisation (Docker)** - Déploiement simplifié
- 🔄 **Réentraînement automatique** - Amélioration continue

## 📊 Dataset

**Student Depression and Lifestyle 100k Data**
- **Source** : [Kaggle Dataset](https://www.kaggle.com/datasets/aldinwhyudii/student-depression-and-lifestyle-100k-data)
- **Taille** : 100,000 enregistrements
- **Type** : Données tabulaires
- **Variables** : Genre, Âge, Ville, CGPA, Durée de sommeil, Pression académique, Habitudes alimentaires, Stress financier, etc.
- **Target** : Depression (Yes/No)

## 🏗️ Structure du projet

```
Project_ML_Ynov/
├── docs/                          # Documentation du projet
│   └── Projet Mise en production et déploiement continu.pdf
├── data/                          # Données (ref_data.csv, prod_data.csv)
├── artifacts/                     # Modèles entraînés (pickle files)
├── scripts/                       # Scripts d'entraînement et notebooks
├── serving/                       # API FastAPI
│   ├── api.py
│   ├── Dockerfile
│   ├── docker-compose.yml
│   └── requirements.txt
├── webapp/                        # Application Streamlit ✅
│   ├── app.py
│   ├── Dockerfile
│   ├── docker-compose.yml
│   ├── requirements.txt
│   └── README.md
├── reporting/                     # Dashboard Evidently
│   ├── project.py
│   ├── Dockerfile
│   ├── docker-compose.yml
│   └── requirements.txt
├── WEBAPP_GUIDE.md               # Guide détaillé de l'application web
└── README.md                     # Ce fichier
```

## 🚀 Démarrage rapide

### Prérequis

- Docker Desktop installé
- Docker Compose installé

### 1. Démarrer l'API de serving

```bash
docker compose -f serving/docker-compose.yml up
```

L'API sera accessible sur : **http://localhost:8080**

### 2. Démarrer l'application web Streamlit

```bash
docker compose -f webapp/docker-compose.yml up
```

L'application sera accessible sur : **http://localhost:8081**

### 3. (Optionnel) Démarrer le reporting

```bash
docker compose -f reporting/docker-compose.yml up
```

Le dashboard sera accessible sur : **http://localhost:8082**

## 💻 Utilisation de l'application web

1. **Ouvrez votre navigateur** à `http://localhost:8081`
2. **Remplissez le formulaire** avec vos informations :
   - Informations démographiques (genre, âge, ville, profession)
   - Informations académiques (CGPA, heures d'étude)
   - Style de vie (sommeil, habitudes alimentaires)
   - Évaluation psychologique (stress, satisfaction)
3. **Cliquez sur "🔮 Prédire"**
4. **Consultez le résultat** :
   - ⚠️ Risque de dépression détecté
   - ✅ Pas de risque détecté
5. **(Optionnel) Fournissez un feedback** pour améliorer le modèle

## 📚 Documentation

- **Guide webapp complet** : [WEBAPP_GUIDE.md](./WEBAPP_GUIDE.md)
- **README webapp** : [webapp/README.md](./webapp/README.md)
- **Spécifications du projet** : [docs/Projet Mise en production et déploiement continu.pdf](./docs/)

## 🛠️ Technologies utilisées

### Backend & ML
- **Python 3.10** - Langage de programmation
- **scikit-learn** - Machine Learning
- **FastAPI** - Framework API
- **Evidently** - Monitoring et reporting

### Frontend
- **Streamlit** - Interface utilisateur interactive
- **Requests** - Communication HTTP

### Infrastructure
- **Docker** - Conteneurisation
- **Docker Compose** - Orchestration
- **uvicorn** - Serveur ASGI

## 🔧 Commandes utiles

### Reconstruire les images

```bash
# API
docker compose -f serving/docker-compose.yml up --build --force-recreate

# Webapp
docker compose -f webapp/docker-compose.yml up --build --force-recreate

# Reporting
docker compose -f reporting/docker-compose.yml up --build --force-recreate
```

### Arrêter les services

```bash
# Tout arrêter
docker compose -f serving/docker-compose.yml down
docker compose -f webapp/docker-compose.yml down
docker compose -f reporting/docker-compose.yml down

# Ou avec un seul script
docker stop webapp serving-api reporting
```

### Voir les logs

```bash
docker logs webapp -f
docker logs serving-api -f
```

## 🧪 Tests

Pour tester l'API manuellement :

```bash
curl -X POST http://localhost:8080/predict \
  -H "Content-Type: application/json" \
  -d '{
    "Gender": "Male",
    "Age": 20,
    "City": "Paris",
    "Profession": "Student",
    "CGPA": 3.5,
    "Sleep_Duration": 7.0,
    "Study_Hours": 4.0,
    "Dietary_Habits": "Healthy",
    "Academic_Pressure": 6,
    "Work_Pressure": 4,
    "Study_Satisfaction": 7,
    "Job_Satisfaction": 5,
    "Financial_Stress": 5,
    "Family_History": "No"
  }'
```

## ⚠️ Disclaimer

Cette application est à **but éducatif uniquement**. Elle ne remplace **en aucun cas** un diagnostic médical professionnel. Si vous pensez souffrir de dépression, consultez un professionnel de santé.

## 🆘 Ressources de soutien psychologique

En cas de détresse psychologique :

- **SOS Amitié** : 09 72 39 40 50 (24h/24, 7j/7)
- **Fil Santé Jeunes** : 0 800 235 236 (gratuit, anonyme)
- **Suicide Écoute** : 01 45 39 40 00 (24h/24, 7j/7)
- **3114** : Numéro national de prévention du suicide

## 👥 Équipe & Contexte

- **Cours** : Concepts, fonctionnements et technologies de l'IA
- **Enseignant** : Haytham Elghazel
- **Formation** : M1 DataEng - Ynov Campus
- **Année universitaire** : 2025-2026

### Répartition du travail

- **Webapp (Streamlit)** : Interface utilisateur de prédiction ✅
- **API (FastAPI)** : Endpoints de prédiction et feedback
- **Reporting (Evidently)** : Dashboard de monitoring
- **ML Pipeline** : Entraînement et réentraînement

## 📝 License

Projet académique - Ynov 2025-2026

## 🔗 Liens utiles

- [Documentation Streamlit](https://docs.streamlit.io/)
- [Documentation FastAPI](https://fastapi.tiangolo.com/)
- [Documentation Docker](https://docs.docker.com/)
- [Documentation Evidently](https://docs.evidentlyai.com/)
- [Dataset Kaggle](https://www.kaggle.com/datasets/aldinwhyudii/student-depression-and-lifestyle-100k-data)

---

**Note** : Ce projet fait partie d'un travail d'équipe. La partie webapp (Streamlit) a été implémentée. Les autres composants (API, reporting, ML pipeline) sont gérés par les autres membres de l'équipe.
