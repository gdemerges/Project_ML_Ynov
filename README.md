# MindPulse - Student Depression Prediction 🧠

Projet de mise en production et déploiement continu d'un modèle de Machine Learning pour la prédiction de la dépression chez les étudiants.

## 📋 Description

Solution complète de ML en production avec architecture microservices :
- 🧠 **Interface web moderne (Streamlit)** - Formulaire multi-étapes avec design glassmorphism
- 🔄 **API de serving (FastAPI)** - Prédiction + Feedback + Auto-retrain
- 📊 **Reporting (Evidently)** - Génération automatique de rapports HTML
- 🐳 **Conteneurisation optimisée (Docker)** - Images légères Python 3.11
- 🔄 **Réentraînement automatique** - Trigger toutes les 50 feedbacks
- ⚙️ **Orchestration (Airflow)** - Pipelines MLOps automatisés
- 🔬 **MLflow** - Tracking des expériences et Model Registry

## 📊 Dataset

**Student Depression and Lifestyle Data**
- **Source** : Données d'étudiants (100k enregistrements)
- **Features** : Age, Gender, Department, CGPA, Sleep_Duration, Study_Hours, Social_Media_Hours, Physical_Activity, Stress_Level
- **Target** : Depression (0/1)
- **Preprocessing** : StandardScaler + OneHotEncoder + PCA (95% variance)

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     prod_net (Docker bridge)                 │
│                                                              │
│  ┌──────────────┐      ┌──────────────┐    ┌──────────────┐│
│  │ serving-api  │ ───> │   webapp     │    │  reporting   ││
│  │   :8080      │      │   :8081      │    │  (run once)  ││
│  │              │      │              │    │              ││
│  │ • /predict   │      │ • Form UI    │    │ • HTML       ││
│  │ • /feedback  │      │ • Multi-step │    │   reports    ││
│  │ • /health    │      │ • Feedback   │    │              ││
│  └──────────────┘      └──────────────┘    └──────────────┘│
│         │                                           │        │
│         └───────────────────────────────────────────┘        │
│                volumes: data/, artifacts/, reports/          │
└─────────────────────────────────────────────────────────────┘
```

## 🚀 Démarrage rapide

### Option 1 : Tout démarrer d'un coup (recommandé)

```bash
# Script automatique
./start.sh

# Ou manuellement
docker compose up --build
```

**Services disponibles :**
- Webapp : http://localhost:8081
- API : http://localhost:8080
- Reporting : génère des fichiers dans `reports/`

### Option 2 : Services individuels (conforme au sujet)

```bash
# 1. API de serving (doit être lancé en premier)
docker compose -f serving/docker-compose.yml up

# 2. Application web
docker compose -f webapp/docker-compose.yml up

# 3. Reporting (génère les rapports puis s'arrête)
docker compose -f reporting/docker-compose.yml up
```

### Option 3 : Services MLOps additionnels

```bash
# MLflow Tracking Server (port 5000)
cd mlflow && ./start.sh

# Airflow Orchestration (port 8083)
cd airflow && ./start.sh
```

## 💻 Utilisation de l'application web

### Flow utilisateur

1. **Ouvrez** http://localhost:8081
2. **Remplissez le formulaire multi-étapes** :
   - Étape 1/4 : Informations démographiques (Genre, Âge, Département)
   - Étape 2/4 : Profil académique (CGPA, Heures d'étude)
   - Étape 3/4 : Habitudes de vie (Sommeil, Réseaux sociaux, Activité physique, Stress)
   - Étape 4/4 : Révision et soumission
3. **Obtenez votre prédiction** avec recommandations personnalisées
4. **Fournissez un feedback** (optionnel) pour améliorer le modèle
   - Affiche le nombre total de feedbacks
   - Indique si le ré-entraînement a été déclenché

### Features du formulaire

- ✅ **Navigation bidirectionnelle** (Précédent/Suivant)
- ✅ **Sauvegarde automatique** des données entre les étapes
- ✅ **Page de révision** avant soumission
- ✅ **Design moderne** : glassmorphism, gradient violet, animations
- ✅ **Responsive** : s'adapte à toutes les tailles d'écran

## 🔧 API Endpoints

### POST /predict
Effectue une prédiction sur un profil étudiant.

```bash
curl -X POST http://localhost:8080/predict \
  -H "Content-Type: application/json" \
  -d '{
    "features": {
      "Age": 22,
      "Gender": "Male",
      "Department": "Engineering",
      "CGPA": 3.2,
      "Sleep_Duration": 6.5,
      "Study_Hours": 5.0,
      "Social_Media_Hours": 4.0,
      "Physical_Activity": 90,
      "Stress_Level": 7
    }
  }'
```

**Réponse :**
```json
{
  "prediction": 1
}
```

### POST /feedback
Enregistre un feedback utilisateur et déclenche le ré-entraînement si seuil atteint.

```bash
curl -X POST http://localhost:8080/feedback \
  -H "Content-Type: application/json" \
  -d '{
    "features": { ... },
    "prediction": 1,
    "actual": 0
  }'
```

**Réponse :**
```json
{
  "status": "ok",
  "total_feedbacks": 45,
  "retrain_triggered": false
}
```

**Ré-entraînement automatique :**
- Trigger : tous les 50 feedbacks (configurable via `RETRAIN_THRESHOLD`)
- Processus : concatène `ref_data.csv` + `prod_data.csv`, compare Logistic Regression vs Random Forest, sauvegarde le meilleur modèle
- Hot-swap : le nouveau modèle est chargé sans redémarrage du conteneur

## 📊 Reporting avec Evidently

Le service `reporting` génère 3 rapports HTML :

```bash
docker compose -f reporting/docker-compose.yml up
```

**Rapports générés dans `reports/` :**
- `data_quality.html` - Qualité des données
- `data_drift.html` - Détection de drift
- `classification_performance.html` - Métriques (F1, Precision, Recall, Accuracy)

**Accès :** Ouvrez les fichiers HTML directement dans votre navigateur.

## 🛠️ Technologies & Versions

| Composant | Technologie | Version | Taille image |
|-----------|-------------|---------|--------------|
| Base | Python | 3.11-slim | ~150 MB |
| API | FastAPI | 0.115.0 | ~115 MB |
| Web | Streamlit | latest | ~120 MB |
| ML | scikit-learn | 1.8.0 | - |
| Reporting | Evidently | latest | ~180 MB |
| Orchestration | Airflow | 2.9.0 | ~1.2 GB |
| Tracking | MLflow | 2.12.1 | ~800 MB |

**Optimisations Docker :**
- `--no-cache-dir` : gain de ~200 MB par image
- Layers combinés : build plus rapide
- Utilisateur non-root : sécurité améliorée
- `.dockerignore` : exclusion des fichiers inutiles

## 📁 Structure du projet

```
Project_ML_Ynov/
├── docker-compose.yml          # 🆕 Compose racine (tout en un)
├── start.sh                    # 🆕 Script de démarrage automatique
├── DOCKER_GUIDE.md             # 🆕 Guide optimisations Docker
│
├── data/
│   ├── ref_data.csv            # Données de référence (PCA + target)
│   └── prod_data.csv           # Feedbacks collectés (généré auto)
│
├── artifacts/
│   ├── model.pickle                    # Modèle entraîné
│   └── preprocessing_pipeline.pickle   # Pipeline (scaler + PCA)
│
├── scripts/
│   ├── students_scripts.py     # Script d'entraînement PCA
│   ├── train_with_mlflow.py    # 🆕 Entraînement avec MLflow
│   └── requirements.txt        # 🆕 Dépendances training
│
├── serving/                    # 🔧 API FastAPI refaite
│   ├── api.py                  # • /predict, /feedback, /health
│   ├── Dockerfile              # • Auto-retrain trigger
│   ├── docker-compose.yml      # • Hot model swap
│   ├── requirements.txt        # • Python 3.11
│   └── .dockerignore           # 🆕
│
├── webapp/                     # 🎨 UI refaite (glassmorphism)
│   ├── app.py                  # • Formulaire multi-étapes
│   ├── Dockerfile              # • Navigation bidirectionnelle
│   ├── docker-compose.yml      # • Feedback intégré
│   ├── requirements.txt        # • Design moderne
│   └── .dockerignore           # 🆕
│
├── reporting/                  # 📊 Service Evidently
│   ├── project.py              # Génère 3 rapports HTML
│   ├── Dockerfile
│   ├── docker-compose.yml
│   ├── requirements.txt
│   └── .dockerignore           # 🆕
│
├── reports/                    # Rapports générés
│   ├── data_quality.html
│   ├── data_drift.html
│   └── classification_performance.html
│
├── mlflow/                     # 🔬 MLflow Tracking
│   ├── docker-compose.yml
│   ├── mlflow_config.py
│   ├── requirements.txt
│   └── README.md
│
└── airflow/                    # ⚙️ Orchestration MLOps
    ├── dags/
    │   ├── ml_retrain_pipeline.py          # DAG ré-entraînement
    │   └── evidently_reporting_pipeline.py # DAG reporting
    ├── docker-compose.yml
    ├── requirements.txt
    └── README.md
```

## 🔧 Commandes utiles

### Gestion des conteneurs

```bash
# Tout démarrer
docker compose up --build

# Arrêter
docker compose down

# Rebuild complet
docker compose up --build --force-recreate

# Voir les logs
docker compose logs -f serving-api
docker compose logs -f webapp

# Status des services
docker compose ps
```

### Debugging

```bash
# Health check API
curl http://localhost:8080/health

# Shell dans un conteneur
docker compose exec serving-api bash
docker compose exec webapp bash

# Voir les artifacts
ls -lh artifacts/

# Voir les feedbacks
cat data/prod_data.csv | wc -l
```

### Nettoyage

```bash
# Supprimer les conteneurs
docker compose down

# Supprimer images + volumes
docker compose down --rmi all --volumes

# Nettoyer tout Docker
docker system prune -a
```

## ⚙️ Configuration

### Variables d'environnement

**serving/api.py :**
```python
ARTIFACTS_DIR = "/artifacts"       # Emplacement des modèles
DATA_DIR = "/data"                 # Emplacement des données
RETRAIN_THRESHOLD = 50             # Nombre de feedbacks avant retrain
```

**Pour modifier le seuil de ré-entraînement :**
```yaml
# docker-compose.yml
environment:
  - RETRAIN_THRESHOLD=100  # Retrain tous les 100 feedbacks
```

## 📚 Documentation complète

- **[DOCKER_GUIDE.md](./DOCKER_GUIDE.md)** - Optimisations Docker détaillées
- **[MLOPS_GUIDE.md](./MLOPS_GUIDE.md)** - Architecture MLOps complète
- **[AIRFLOW_IMPLEMENTATION_SUMMARY.md](./AIRFLOW_IMPLEMENTATION_SUMMARY.md)** - Détails Airflow

## ⚠️ Troubleshooting

### Problème : "Cannot reach the API"
**Cause :** L'API n'est pas démarrée ou n'est pas healthy
**Solution :**
```bash
docker compose logs serving-api
curl http://localhost:8080/health
```

### Problème : "Model artifacts not loaded"
**Cause :** Version scikit-learn incompatible
**Solution :** Le projet utilise scikit-learn 1.8.0 avec Python 3.11

### Problème : Webapp ne démarre pas
**Cause :** Dépendance sur serving-api non satisfaite
**Solution :** Le healthcheck gère ça automatiquement avec le compose racine

### Problème : Permission denied sur volumes
**Cause :** UID mismatch
**Solution :**
```bash
sudo chown -R 1000:1000 data/ artifacts/ reports/
```

## ⚠️ Disclaimer

Cette application est à **but éducatif uniquement**. Elle ne remplace **en aucun cas** un diagnostic médical professionnel. Si vous pensez souffrir de dépression, consultez un professionnel de santé.

## 🆘 Ressources de soutien psychologique

En cas de détresse psychologique :

- **3114** - Numéro national de prévention du suicide
- **SOS Amitié** : 09 72 39 40 50 (24h/24, 7j/7)
- **Fil Santé Jeunes** : 0 800 235 236 (gratuit, anonyme)
- **Nightline** : Service d'écoute étudiant

## 👥 Équipe & Contexte

- **Membres** : Mama Assaïta Sakho, Parvin Sultana, Gabriel Faucon, Guillaume Demergès
- **Cours** : Concepts, fonctionnements et technologies de l'IA
- **Enseignant** : Haytham Elghazel
- **Formation** : M1 DataEng - Ynov Campus
- **Année universitaire** : 2025-2026

## 📝 License

Projet académique - Ynov 2025-2026

## 🔗 Liens utiles

- [Documentation Streamlit](https://docs.streamlit.io/)
- [Documentation FastAPI](https://fastapi.tiangolo.com/)
- [Documentation Docker](https://docs.docker.com/)
- [Documentation Evidently](https://docs.evidentlyai.com/)
- [Documentation MLflow](https://mlflow.org/docs/latest/index.html)
- [Documentation Airflow](https://airflow.apache.org/docs/)

---

**MindPulse** - Production ML Pipeline avec Auto-Retraining 🚀
