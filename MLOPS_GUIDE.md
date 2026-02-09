# Guide MLOps - MindPulse Analytics

Ce guide décrit l'architecture MLOps complète du projet et le flux de données automatisé.

## 📊 Vue d'ensemble de l'architecture

```
┌─────────────────────────────────────────────────────────────────────┐
│                         UTILISATEUR                                  │
└───────────────────────────┬─────────────────────────────────────────┘
                            │
                            ▼
                  ┌─────────────────────┐
                  │  Streamlit WebApp   │  Port 8081
                  │  (Interface User)   │
                  └──────────┬──────────┘
                            │ HTTP POST /predict
                            ▼
                  ┌─────────────────────┐
                  │   FastAPI Serving   │  Port 8080
                  │  (Modèle ML + API)  │
                  └──────────┬──────────┘
                            │
              ┌─────────────┼─────────────┐
              │             │             │
              ▼             ▼             ▼
      ┌──────────┐   ┌──────────┐   ┌──────────┐
      │ Prédire  │   │ Feedback │   │  Stocker │
      │  avec    │   │   Loop   │   │  dans    │
      │  Modèle  │   │          │   │prod_data │
      └──────────┘   └──────────┘   └────┬─────┘
                                          │
                                          ▼
                            ┌──────────────────────────┐
                            │   Apache Airflow         │  Port 8083
                            │  (Orchestration MLOps)   │
                            └──────────┬───────────────┘
                                      │
                ┌─────────────────────┼─────────────────────┐
                │                     │                     │
                ▼                     ▼                     ▼
      ┌──────────────────┐  ┌──────────────────┐  ┌──────────────────┐
      │ DAG: Retrain     │  │ DAG: Reporting   │  │ DAG: Monitoring  │
      │ (Quotidien)      │  │ (Toutes les 6h)  │  │ (Continu)        │
      └────────┬─────────┘  └────────┬─────────┘  └────────┬─────────┘
               │                     │                     │
               ▼                     ▼                     ▼
      ┌──────────────────┐  ┌──────────────────┐  ┌──────────────────┐
      │ Nouveau Modèle   │  │ Rapports HTML    │  │ Alertes + Logs   │
      │ dans artifacts/  │  │ dans reports/    │  │                  │
      └──────────────────┘  └──────────────────┘  └──────────────────┘
```

## 🔄 Flux de données détaillé

### 1. Phase de prédiction (Runtime)

```
1. Utilisateur remplit le formulaire Streamlit
   ↓
2. Webapp envoie POST à /predict avec les features
   ↓
3. FastAPI charge le modèle (artifacts/model.pickle)
   ↓
4. Preprocessing avec pipeline (artifacts/preprocessing_pipeline.pickle)
   ↓
5. Prédiction ML (0: Pas de dépression, 1: Dépression)
   ↓
6. Réponse JSON retournée à Streamlit
   ↓
7. Affichage du résultat à l'utilisateur
```

### 2. Phase de feedback (Continuous Learning)

```
1. Utilisateur fournit le vrai résultat (actual)
   ↓
2. Webapp envoie POST à /feedback
   ↓
3. FastAPI sauvegarde dans data/prod_data.csv
   ↓
4. Ajout de: features + prediction + actual + timestamp
   ↓
5. Données accumulées pour réentraînement futur
```

### 3. Phase de monitoring (Toutes les 6 heures)

```
Airflow DAG: evidently_reporting_pipeline
↓
1. Lire ref_data.csv (données d'entraînement)
   ↓
2. Lire prod_data.csv (données de production)
   ↓
3. Comparer avec Evidently AI
   ├── Data Quality Report (valeurs manquantes, outliers)
   ├── Data Drift Report (distribution des features)
   └── Model Performance Report (accuracy, F1, précision)
   ↓
4. Générer rapports HTML dans reports/
   ↓
5. Nettoyer les anciens rapports (garde les 10 plus récents)
```

### 4. Phase de réentraînement (Quotidien)

```
Airflow DAG: ml_retrain_pipeline
↓
1. CHECK: prod_data.csv >= 1000 lignes ?
   ├── OUI → Continue
   └── NON → Skip (pas assez de données)
   ↓
2. CHECK: Drift détecté avec Evidently ?
   ├── OUI → Continue (drift > 30%)
   └── NON → Continue quand même si step 1 = OUI
   ↓
3. BACKUP: Sauvegarder modèle actuel
   - artifacts/model_backup_YYYYMMDD_HHMMSS.pickle
   - artifacts/preprocessing_pipeline_backup_YYYYMMDD_HHMMSS.pickle
   ↓
4. MERGE: Fusionner ref_data + prod_data
   - Créer merged_training_data.csv
   - Supprimer les doublons
   ↓
5. TRAIN: Entraîner 3 modèles
   - Logistic Regression
   - Random Forest
   - XGBoost
   ↓
6. SELECT: Garder le meilleur (accuracy)
   ↓
7. SAVE: Remplacer model.pickle
   ↓
8. ARCHIVE: Déplacer prod_data.csv
   - prod_data_archived_YYYYMMDD_HHMMSS.csv
   - Créer nouveau prod_data.csv vide
   ↓
9. NOTIFY: Logger le succès avec métriques
```

## 🎯 Triggers de réentraînement

Le réentraînement est déclenché automatiquement si **AU MOINS UNE** des conditions suivantes est remplie :

1. **Seuil de données** : `prod_data.csv` contient ≥ 1000 lignes
2. **Drift détecté** : Plus de 30% des features ont drifté
3. **Performance dégradée** : Accuracy < seuil défini (configurable)
4. **Déclenchement manuel** : Via l'interface Airflow

## 📁 Structure des fichiers de données

```
data/
├── student_lifestyle_100k.csv          # Dataset original Kaggle
├── ref_data.csv                        # Données d'entraînement (PCA)
├── prod_data.csv                       # Données de production (accumulées)
├── merged_training_data.csv            # Fusion ref + prod (temporaire)
└── prod_data_archived_YYYYMMDD.csv    # Archives des réentraînements

artifacts/
├── model.pickle                        # Modèle actuel en production
├── preprocessing_pipeline.pickle       # Pipeline de preprocessing
├── model_backup_YYYYMMDD.pickle       # Backups des modèles
└── preprocessing_pipeline_backup_*.pkl # Backups des pipelines

reports/
├── data_quality_report_*.html          # Rapports de qualité
├── data_drift_report_*.html            # Rapports de drift
└── model_performance_report_*.html     # Rapports de performance
```

## 🔧 Configuration des DAGs Airflow

### ml_retrain_pipeline.py

**Paramètres configurables :**

```python
# Seuil minimum de données pour déclencher le réentraînement
RETRAIN_THRESHOLD = 1000  # lignes dans prod_data.csv

# Seuil de drift acceptable
DRIFT_THRESHOLD = 0.3  # 30% max de colonnes avec drift

# Schedule
schedule_interval='@daily'  # Exécution quotidienne à minuit
```

**Modifier le schedule :**
```python
schedule_interval='@hourly'           # Toutes les heures
schedule_interval='0 */6 * * *'       # Toutes les 6 heures
schedule_interval='0 2 * * *'         # Tous les jours à 2h du matin
schedule_interval='0 0 * * 0'         # Tous les dimanches à minuit
```

### evidently_reporting_pipeline.py

**Paramètres configurables :**

```python
# Nombre de rapports à conserver
MAX_REPORTS = 10  # Garde les 10 plus récents

# Schedule
schedule_interval='0 */6 * * *'  # Toutes les 6 heures
```

## 🚀 Guide de déploiement complet

### 1. Démarrage initial

```bash
# 1. Entraîner le modèle initial
cd scripts
jupyter notebook students.ipynb
# Exécuter toutes les cellules → génère artifacts/ et data/ref_data.csv

# 2. Démarrer l'API de serving
cd ../serving
docker compose up -d

# 3. Démarrer la webapp Streamlit
cd ../webapp
docker compose up -d

# 4. Démarrer Airflow
cd ../airflow
./start.sh
```

### 2. Vérification du système

```bash
# Vérifier que tous les services sont up
docker ps

# Devrait montrer :
# - serving-api (port 8080)
# - webapp (port 8081)
# - airflow-webserver (port 8083)
# - airflow-scheduler
# - postgres (Airflow DB)
```

### 3. Test du flux complet

```bash
# 1. Aller sur la webapp
open http://localhost:8081

# 2. Faire une prédiction
# Remplir le formulaire → Cliquer "Run Analysis"

# 3. Fournir un feedback
# Indiquer le vrai résultat → Cliquer "Submit feedback"

# 4. Vérifier que les données sont sauvegardées
cat data/prod_data.csv

# 5. Aller sur Airflow
open http://localhost:8083
# Username: admin, Password: admin

# 6. Activer les DAGs
# Cliquer sur les toggles pour activer les 2 DAGs

# 7. Déclencher manuellement le réentraînement
# Dans Airflow UI → ml_retrain_pipeline → Trigger DAG
```

## 📊 Monitoring et observabilité

### Logs Airflow

```bash
# Logs du scheduler (exécution des DAGs)
docker logs -f airflow-scheduler

# Logs du webserver
docker logs -f airflow-webserver

# Logs d'un DAG spécifique
# Via l'interface Airflow → DAG → Graph View → Task → Log
```

### Métriques à surveiller

1. **Volume de données**
   - Nombre de lignes dans `prod_data.csv`
   - Taux de feedback (predictions avec actual)

2. **Performance du modèle**
   - Accuracy en production (via rapports Evidently)
   - F1-Score
   - Precision / Recall

3. **Drift des données**
   - % de features avec drift significatif
   - Distribution des features (histogrammes)

4. **Santé du pipeline**
   - Succès/Échec des DAG runs
   - Durée d'exécution des tâches
   - Erreurs dans les logs

## 🔐 Sécurité et bonnes pratiques

### En production

1. **Changer les credentials Airflow**
```bash
docker exec -it airflow-webserver airflow users create \
  --username YOUR_USER \
  --password YOUR_SECURE_PASSWORD \
  --firstname YOUR_NAME \
  --lastname YOUR_LASTNAME \
  --role Admin \
  --email YOUR_EMAIL
```

2. **Configurer la persistance des volumes**
```yaml
# Dans docker-compose.yml
volumes:
  - ./data:/opt/airflow/data:rw
  - ./artifacts:/opt/airflow/artifacts:rw
  - ./reports:/opt/airflow/reports:rw
```

3. **Activer les notifications**
- Email en cas d'échec des DAGs
- Slack webhooks pour alertes
- Grafana pour monitoring temps réel

4. **Backup régulier**
```bash
# Backup des modèles
cp -r artifacts/ backups/artifacts_$(date +%Y%m%d)/

# Backup de la BDD Airflow
docker exec postgres pg_dump -U airflow airflow > backup_airflow_$(date +%Y%m%d).sql
```

## 🐛 Troubleshooting

### Problème : DAG ne s'exécute pas

**Solution :**
```bash
# 1. Vérifier que le scheduler est actif
docker logs airflow-scheduler

# 2. Vérifier les erreurs dans le DAG
docker exec -it airflow-scheduler airflow dags list-import-errors

# 3. Tester le DAG manuellement
docker exec -it airflow-scheduler airflow dags test ml_retrain_pipeline 2026-02-09
```

### Problème : Réentraînement ne se déclenche pas

**Solution :**
```bash
# 1. Vérifier le nombre de lignes dans prod_data.csv
wc -l data/prod_data.csv

# 2. Ajuster le seuil dans le DAG
# Éditer airflow/dags/ml_retrain_pipeline.py
RETRAIN_THRESHOLD = 10  # Abaisser le seuil pour tester

# 3. Déclencher manuellement
# Via Airflow UI → Trigger DAG
```

### Problème : Modèle ne se charge pas après réentraînement

**Solution :**
```bash
# 1. Vérifier que le fichier existe
ls -lh artifacts/model.pickle

# 2. Restaurer le backup si nécessaire
cp artifacts/model_backup_YYYYMMDD_HHMMSS.pickle artifacts/model.pickle

# 3. Redémarrer l'API
docker restart serving-api
```

## 📚 Ressources

- [Documentation Airflow](https://airflow.apache.org/docs/)
- [Documentation Evidently AI](https://docs.evidentlyai.com/)
- [MLOps Best Practices](https://ml-ops.org/)
- [Continuous Training in ML](https://martinfowler.com/articles/cd4ml.html)

---

**MindPulse Analytics** • MLOps Pipeline • M1 DataEng • Ynov 2025-2026
