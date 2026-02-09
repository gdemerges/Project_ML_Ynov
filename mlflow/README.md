# MLflow Integration - MindPulse Project 🚀

Guide complet pour l'intégration MLflow dans le projet de prédiction de dépression étudiante.

## 📋 Vue d'ensemble

MLflow est intégré pour:
- **Tracking des expériences** - Suivi des métriques, paramètres et artifacts
- **Model Registry** - Gestion des versions de modèles (Staging/Production)
- **Model Serving** - Déploiement simplifié des modèles
- **Comparaison des modèles** - Interface visuelle pour comparer les runs

## 🏗️ Architecture

```
mlflow/
├── docker-compose.yml       # Configuration Docker du serveur MLflow
├── mlflow_config.py         # Module de configuration et utilitaires
└── requirements.txt         # Dépendances Python
```

## 🚀 Démarrage rapide

### 1. Lancer le serveur MLflow

```bash
cd mlflow
docker compose up -d
```

Le serveur sera accessible sur: **http://localhost:5000**

### 2. Entraîner un modèle avec tracking

```bash
cd scripts
python train_with_mlflow.py
```

### 3. Visualiser les résultats

Ouvrez http://localhost:5000 pour accéder à l'interface MLflow.

## 📊 Fonctionnalités

### Tracking des expériences

Chaque entraînement log automatiquement:

| Type | Description |
|------|-------------|
| **Paramètres** | Hyperparamètres du modèle (n_estimators, max_depth, etc.) |
| **Métriques** | accuracy, f1_score, precision, recall, roc_auc |
| **Artifacts** | Modèle sérialisé, pipeline de preprocessing |
| **Tags** | Type de modèle, type d'entraînement, dataset |

### Model Registry

Les modèles sont automatiquement enregistrés avec les stages:

- **None** - Modèle juste enregistré
- **Staging** - Modèle en test
- **Production** - Modèle actif pour les prédictions
- **Archived** - Anciens modèles archivés

## 🔧 Configuration

### Variables d'environnement

```bash
# URI du serveur MLflow
export MLFLOW_TRACKING_URI=http://localhost:5000

# Nom de l'expérience
export MLFLOW_EXPERIMENT_NAME=student-depression-prediction
```

### Configuration Docker

Le fichier `docker-compose.yml` configure:
- SQLite pour le backend store (production: PostgreSQL recommandé)
- Volume persistant pour les artifacts
- Port 5000 exposé

## 📁 Structure des Runs

```
experiment/
├── run_1/
│   ├── metrics/
│   │   ├── accuracy
│   │   ├── f1_score
│   │   └── ...
│   ├── params/
│   │   ├── n_estimators
│   │   └── ...
│   ├── artifacts/
│   │   └── model/
│   └── tags/
└── run_2/
    └── ...
```

## 🔄 Intégration Airflow

Le DAG `ml_retrain_pipeline.py` intègre MLflow pour:

1. **Tracking automatique** - Chaque ré-entraînement crée un nouveau run
2. **Comparaison** - Compare avec le modèle en production
3. **Promotion automatique** - Passe en production si meilleur

### Variables Airflow requises

```python
MLFLOW_TRACKING_URI = "http://mlflow-server:5000"
```

## 📝 Utilisation du module `mlflow_config.py`

### Setup initial

```python
from mlflow_config import setup_mlflow

experiment_id = setup_mlflow()
```

### Logger un entraînement

```python
from mlflow_config import log_model_training

run_id = log_model_training(
    model=trained_model,
    model_name="Random_Forest",
    metrics={"accuracy": 0.95, "f1_score": 0.94},
    params={"n_estimators": 100, "max_depth": 10},
    tags={"training_type": "initial"}
)
```

### Enregistrer le meilleur modèle

```python
from mlflow_config import compare_and_register_best_model

registered = compare_and_register_best_model(
    metrics={"accuracy": 0.95},
    model_name="Random_Forest",
    run_id=run_id
)
```

### Charger le modèle de production

```python
from mlflow_config import load_production_model

model = load_production_model()
predictions = model.predict(X_new)
```

## 🌐 API MLflow

### Endpoints utiles

| Endpoint | Description |
|----------|-------------|
| `GET /api/2.0/mlflow/experiments/list` | Liste des expériences |
| `GET /api/2.0/mlflow/runs/search` | Recherche de runs |
| `GET /api/2.0/mlflow/registered-models/list` | Modèles enregistrés |

### Exemple avec Python

```python
import mlflow
from mlflow.tracking import MlflowClient

client = MlflowClient("http://localhost:5000")

# Lister les expériences
experiments = client.search_experiments()

# Lister les runs d'une expérience
runs = client.search_runs(experiment_ids=["1"])

# Obtenir le modèle en production
versions = client.get_latest_versions("depression-classifier", stages=["Production"])
```

## 🐳 Docker Compose complet

Pour intégrer MLflow avec les autres services:

```yaml
# Dans le docker-compose principal
services:
  mlflow-server:
    image: ghcr.io/mlflow/mlflow:v2.12.1
    ports:
      - "5000:5000"
    volumes:
      - mlflow_data:/mlflow
    command: mlflow server --host 0.0.0.0 --port 5000
    networks:
      - app-network

  webapp:
    # ... configuration existante
    environment:
      - MLFLOW_TRACKING_URI=http://mlflow-server:5000
    depends_on:
      - mlflow-server
```

## 📈 Bonnes pratiques

1. **Nommage cohérent** - Utilisez des noms de runs descriptifs
2. **Tags informatifs** - Ajoutez des tags pour le filtrage
3. **Versioning des données** - Loggez la taille du dataset
4. **Comparaison systématique** - Comparez toujours avec la production
5. **Archivage** - Archivez les anciens modèles régulièrement

## 🔍 Troubleshooting

### Le serveur ne démarre pas

```bash
# Vérifier les logs
docker compose logs mlflow-server

# Recréer le conteneur
docker compose down -v
docker compose up -d
```

### Connexion refusée

```bash
# Vérifier que le serveur est accessible
curl http://localhost:5000/health
```

### Erreur de permission

```bash
# Donner les permissions sur le volume
chmod -R 777 ./mlflow_data
```

## 📚 Ressources

- [Documentation MLflow](https://mlflow.org/docs/latest/index.html)
- [MLflow Model Registry](https://mlflow.org/docs/latest/model-registry.html)
- [MLflow Tracking](https://mlflow.org/docs/latest/tracking.html)
