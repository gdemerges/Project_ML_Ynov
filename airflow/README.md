# Airflow - Orchestration MLOps Pipeline

Ce dossier contient l'infrastructure Airflow pour l'orchestration automatique des pipelines MLOps du projet MindPulse.

## 📋 Vue d'ensemble

Airflow est utilisé pour automatiser :
- 🔄 **Réentraînement automatique** du modèle ML
- 📊 **Génération de rapports Evidently** (monitoring)
- 🔍 **Détection de drift** des données
- 📈 **Suivi de performance** du modèle

## 🏗️ Structure

```
airflow/
├── dags/                                # DAGs Airflow
│   ├── ml_retrain_pipeline.py         # Pipeline de réentraînement
│   └── evidently_reporting_pipeline.py # Pipeline de reporting
├── logs/                                # Logs d'exécution
├── plugins/                             # Plugins personnalisés
├── config/                              # Configuration Airflow
├── docker-compose.yml                   # Orchestration Docker
├── requirements.txt                     # Dépendances Python
└── README.md                           # Ce fichier
```

## 🚀 Démarrage rapide

### 1. Définir l'UID utilisateur (Linux/macOS)

```bash
echo "AIRFLOW_UID=$(id -u)" > .env
```

### 2. Initialiser Airflow

```bash
docker compose up airflow-init
```

### 3. Démarrer les services Airflow

```bash
docker compose up -d
```

### 4. Accéder à l'interface web

Ouvrez votre navigateur à : **http://localhost:8083**

**Identifiants par défaut :**
- Username: `admin`
- Password: `admin`

## 📊 DAGs disponibles

### 1. `ml_retrain_pipeline` - Réentraînement automatique

**Déclenchement :** Quotidien (schedule: `@daily`)

**Workflow :**
1. ✅ Vérifier les données de production (seuil: 1000 lignes)
2. 🔍 Détecter le drift des données
3. 💾 Sauvegarder le modèle actuel
4. 🔗 Fusionner ref_data + prod_data
5. 🤖 Entraîner le nouveau modèle (comparaison: LR, RF, XGBoost)
6. 📦 Archiver les données de production
7. 📧 Notifier le succès

**Conditions de réentraînement :**
- Nombre de lignes dans `prod_data.csv` ≥ 1000
- OU drift détecté (> 30% de colonnes avec drift)

**Activation manuelle :**
```bash
# Via l'interface web Airflow ou via CLI :
docker exec -it airflow-webserver airflow dags trigger ml_retrain_pipeline
```

### 2. `evidently_reporting_pipeline` - Génération de rapports

**Déclenchement :** Toutes les 6 heures (schedule: `0 */6 * * *`)

**Workflow :**
1. ✅ Vérifier la disponibilité des données
2. 📊 Générer rapport de qualité des données
3. 📉 Générer rapport de drift
4. 📈 Générer rapport de performance du modèle
5. 🗑️ Nettoyer les anciens rapports (garde les 10 plus récents)
6. 📧 Envoyer le résumé

**Rapports générés :**
- `data_quality_report_YYYYMMDD_HHMMSS.html`
- `data_drift_report_YYYYMMDD_HHMMSS.html`
- `model_performance_report_YYYYMMDD_HHMMSS.html`

**Emplacement :** `/opt/airflow/reports` (dans le conteneur)

## 🔧 Configuration

### Modifier les seuils de réentraînement

Éditez `dags/ml_retrain_pipeline.py` :

```python
# Seuil pour déclencher le réentraînement
RETRAIN_THRESHOLD = 1000  # Modifier cette valeur
```

### Modifier la fréquence d'exécution

Éditez le paramètre `schedule_interval` dans les DAGs :

```python
# Exécution quotidienne
schedule_interval='@daily'

# Exécution toutes les heures
schedule_interval='@hourly'

# Exécution personnalisée (cron)
schedule_interval='0 */6 * * *'  # Toutes les 6 heures
```

## 📝 Commandes utiles

### Voir les logs en temps réel

```bash
# Logs du webserver
docker logs -f airflow-webserver

# Logs du scheduler
docker logs -f airflow-scheduler
```

### Arrêter Airflow

```bash
docker compose down
```

### Redémarrer Airflow

```bash
docker compose down && docker compose up -d
```

### Reconstruire les images

```bash
docker compose down
docker compose up --build -d
```

### Lister les DAGs

```bash
docker exec -it airflow-webserver airflow dags list
```

### Tester un DAG manuellement

```bash
# Déclencher le réentraînement
docker exec -it airflow-webserver airflow dags trigger ml_retrain_pipeline

# Déclencher le reporting
docker exec -it airflow-webserver airflow dags trigger evidently_reporting_pipeline
```

### Activer/Désactiver un DAG

```bash
# Activer
docker exec -it airflow-webserver airflow dags unpause ml_retrain_pipeline

# Désactiver
docker exec -it airflow-webserver airflow dags pause ml_retrain_pipeline
```

## 🐛 Debugging

### Vérifier le statut des services

```bash
docker compose ps
```

### Accéder au shell du conteneur

```bash
docker exec -it airflow-webserver bash
```

### Vérifier les erreurs dans les logs

```bash
# Logs du scheduler (où les DAGs s'exécutent)
docker logs airflow-scheduler | grep ERROR

# Logs du webserver
docker logs airflow-webserver | grep ERROR
```

### Tester une tâche spécifique

```bash
docker exec -it airflow-webserver airflow tasks test ml_retrain_pipeline check_production_data 2026-02-09
```

## 📚 Ressources

- [Documentation Airflow](https://airflow.apache.org/docs/)
- [Documentation Evidently](https://docs.evidentlyai.com/)
- [DAG Writing Best Practices](https://airflow.apache.org/docs/apache-airflow/stable/best-practices.html)

## ⚙️ Variables d'environnement

Variables configurables dans `docker-compose.yml` :

- `AIRFLOW__CORE__EXECUTOR`: Type d'executor (LocalExecutor par défaut)
- `AIRFLOW__DATABASE__SQL_ALCHEMY_CONN`: Connexion à la base de données
- `AIRFLOW__WEBSERVER__SECRET_KEY`: Clé secrète pour le webserver

## 🔒 Sécurité

**⚠️ Important :** Les identifiants par défaut (`admin`/`admin`) doivent être changés en production !

Pour changer le mot de passe :

```bash
docker exec -it airflow-webserver airflow users create \
  --username YOUR_USERNAME \
  --firstname YOUR_FIRSTNAME \
  --lastname YOUR_LASTNAME \
  --role Admin \
  --email YOUR_EMAIL \
  --password YOUR_PASSWORD
```

## 📞 Support

En cas de problème :
1. Consultez les logs : `docker logs airflow-scheduler`
2. Vérifiez l'interface web Airflow : http://localhost:8083
3. Consultez la documentation du projet

---

**MindPulse Analytics** • M1 DataEng • Ynov Campus • 2025-2026
