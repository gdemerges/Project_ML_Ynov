# Guide Docker - MindPulse Platform

## Démarrage rapide

```bash
# Tout démarrer d'un coup
./start.sh

# Ou manuellement
docker compose up --build
```

## Architecture des conteneurs

```
┌─────────────────────────────────────────────────────────────┐
│                     prod_net (bridge)                        │
│                                                              │
│  ┌──────────────┐      ┌──────────────┐    ┌──────────────┐│
│  │ serving-api  │ ───> │   webapp     │    │  reporting   ││
│  │   :8080      │      │   :8081      │    │  (run once)  ││
│  └──────────────┘      └──────────────┘    └──────────────┘│
│         │                                           │        │
│         └───────────────────────────────────────────┘        │
│                volumes: data/, artifacts/, reports/          │
└─────────────────────────────────────────────────────────────┘
```

## Services

| Service | Port | Description | Healthcheck |
|---------|------|-------------|-------------|
| `serving-api` | 8080 | FastAPI - Prédiction + Feedback + Auto-retrain | `/health` |
| `webapp` | 8081 | Streamlit - Interface utilisateur | - |
| `reporting` | - | Evidently - Génère des rapports HTML | - |

## Volumes partagés

```
./data/
├── ref_data.csv          # Données de référence (PCA + target)
└── prod_data.csv         # Feedbacks collectés (créé automatiquement)

./artifacts/
├── model.pickle                    # Modèle entraîné
└── preprocessing_pipeline.pickle   # Pipeline preprocessing (scaler + PCA)

./reports/
├── data_quality.html              # Rapport qualité des données
├── data_drift.html                # Rapport de drift
└── classification_performance.html # Métriques de classification
```

## Optimisations Docker

### 1. Images légères (`python:3.10-slim`)
- Base Alpine trop minimale (problèmes avec scikit-learn)
- `slim` = bon compromis (taille réduite, compatibilité max)

### 2. Cache optimization
```dockerfile
RUN pip3 install --no-cache-dir -r requirements.txt
```
- `--no-cache-dir` : ne garde pas les fichiers temporaires de pip
- **Gain : ~200MB par image**

### 3. Layer optimization
```dockerfile
# ❌ Mauvais (2 layers)
RUN pip3 install --upgrade pip
RUN pip3 install -r requirements.txt

# ✅ Bon (1 layer)
RUN pip3 install --no-cache-dir --upgrade pip && \
    pip3 install --no-cache-dir -r requirements.txt
```

### 4. Security (non-root user)
```dockerfile
RUN useradd -m -u 1000 appuser
USER appuser
```
- Les processus tournent en tant qu'utilisateur non-privilégié
- Bonne pratique de sécurité

### 5. `.dockerignore`
Exclut les fichiers inutiles :
```
__pycache__/
*.pyc
.git/
.env
docker-compose.yml
```
- Accélère le build
- Réduit la taille des images

### 6. Healthcheck + depends_on
```yaml
healthcheck:
  test: ["CMD", "python", "-c", "import urllib.request; ..."]
  interval: 10s

depends_on:
  serving-api:
    condition: service_healthy
```
- Le webapp attend que l'API soit prête
- Pas d'erreur "connection refused" au démarrage

## Comparaison des tailles d'images

| Optimisation | Taille typique |
|--------------|----------------|
| `python:3.10` (full) | ~900 MB |
| `python:3.10-slim` | ~150 MB |
| + `--no-cache-dir` | ~120 MB |
| + `.dockerignore` | ~115 MB |

**Gain total : ~785 MB par image (87% de réduction)**

## Commandes utiles

```bash
# Tout arrêter
docker compose down

# Rebuild complet
docker compose up --build --force-recreate

# Voir les logs d'un service
docker compose logs serving-api
docker compose logs -f webapp  # mode follow

# Nettoyer les images inutilisées
docker system prune -a

# Voir la taille des images
docker images | grep mindpulse

# Shell dans un conteneur
docker compose exec serving-api bash
```

## Services additionnels (optionnels)

Les services MLflow et Airflow ont leurs propres docker-compose :

```bash
# MLflow (tracking)
cd mlflow && ./start.sh
# → http://localhost:5000

# Airflow (orchestration)
cd airflow && ./start.sh
# → http://localhost:8083
```

## Troubleshooting

### Problème : "cannot import name ColumnMapping"
**Cause** : Version d'Evidently incompatible
**Solution** : Le script utilise maintenant `evidently.pipeline.column_mapping`

### Problème : webapp ne démarre pas (connection refused)
**Cause** : L'API n'est pas encore prête
**Solution** : Le healthcheck gère ça automatiquement maintenant

### Problème : Model artifacts not found
**Cause** : Pas de modèle entraîné
**Solution** :
```bash
python scripts/students_scripts.py
```

### Problème : Permission denied sur volumes
**Cause** : UID mismatch entre host et container
**Solution** :
```bash
sudo chown -R 1000:1000 data/ artifacts/ reports/
```

## Architecture de déploiement

Pour un déploiement production, considérer :

1. **Registry Docker** : pousser les images sur Docker Hub / AWS ECR
2. **Orchestration** : passer à Kubernetes (ou Docker Swarm)
3. **Secrets** : utiliser Docker secrets / Kubernetes secrets
4. **Monitoring** : ajouter Prometheus + Grafana
5. **Reverse proxy** : Nginx / Traefik devant les services
6. **HTTPS** : certificats Let's Encrypt

## Alternatives

### Option 1 : Docker Compose racine (actuel)
✅ Simple, conforme au sujet
✅ Un seul réseau partagé
❌ Pas de scaling automatique

### Option 2 : Kubernetes
✅ Production-grade
✅ Auto-scaling, self-healing
❌ Plus complexe, overkill pour le projet

### Option 3 : Un seul container monolithique
❌ Anti-pattern microservices
❌ Pas de séparation des responsabilités
❌ Interdit par le sujet (conteneurisation des processus)
