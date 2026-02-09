#!/bin/bash

echo "🚀 Démarrage d'Airflow pour MindPulse Analytics"
echo "================================================"

# Vérifier si Docker est en cours d'exécution
if ! docker info > /dev/null 2>&1; then
    echo "❌ Erreur: Docker n'est pas en cours d'exécution"
    echo "   Veuillez démarrer Docker Desktop et réessayer"
    exit 1
fi

# Créer les dossiers nécessaires
echo "📁 Création des dossiers nécessaires..."
mkdir -p dags logs plugins config ../reports

# Définir les permissions (Linux/macOS)
if [[ "$OSTYPE" == "linux-gnu"* ]] || [[ "$OSTYPE" == "darwin"* ]]; then
    echo "🔒 Configuration des permissions..."
    echo "AIRFLOW_UID=$(id -u)" > .env
    echo "AIRFLOW_GID=0" >> .env
fi

# Initialiser la base de données Airflow
echo "🗄️ Initialisation de la base de données Airflow..."
docker compose up airflow-init

if [ $? -eq 0 ]; then
    echo "✅ Initialisation réussie"
else
    echo "❌ Erreur lors de l'initialisation"
    exit 1
fi

# Démarrer les services Airflow
echo "🎬 Démarrage des services Airflow..."
docker compose up -d

# Attendre que les services démarrent
echo "⏳ Attente du démarrage des services (30 secondes)..."
sleep 30

# Vérifier le statut des services
echo ""
echo "📊 Statut des services:"
docker compose ps

echo ""
echo "================================================"
echo "✅ Airflow est maintenant accessible!"
echo ""
echo "🌐 Interface Web: http://localhost:8083"
echo "👤 Username: admin"
echo "🔑 Password: admin"
echo ""
echo "📊 DAGs disponibles:"
echo "   - ml_retrain_pipeline: Réentraînement automatique"
echo "   - evidently_reporting_pipeline: Génération de rapports"
echo ""
echo "📝 Commandes utiles:"
echo "   docker compose logs -f           # Voir les logs"
echo "   docker compose down              # Arrêter Airflow"
echo "   docker compose restart           # Redémarrer Airflow"
echo "================================================"
