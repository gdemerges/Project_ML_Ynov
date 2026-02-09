#!/bin/bash
# Script de démarrage du serveur MLflow

echo "🚀 Démarrage du serveur MLflow..."
docker compose up -d

echo ""
echo "✅ MLflow Tracking Server démarré!"
echo "📊 Interface: http://localhost:5000"
echo ""
echo "Pour arrêter: docker compose down"
