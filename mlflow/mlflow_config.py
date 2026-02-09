"""
MLflow Configuration Module
Projet: MindPulse - Student Depression Prediction

Ce module fournit les fonctions utilitaires pour l'intégration MLflow.
"""

import mlflow
import mlflow.sklearn
from mlflow.tracking import MlflowClient
import os
from pathlib import Path
from datetime import datetime

# Configuration MLflow
MLFLOW_TRACKING_URI = os.getenv("MLFLOW_TRACKING_URI", "http://localhost:5000")
EXPERIMENT_NAME = "student-depression-prediction"
MODEL_NAME = "depression-classifier"


def setup_mlflow():
    """Configure MLflow avec le tracking URI et l'expérience"""
    mlflow.set_tracking_uri(MLFLOW_TRACKING_URI)
    
    # Créer ou récupérer l'expérience
    experiment = mlflow.get_experiment_by_name(EXPERIMENT_NAME)
    if experiment is None:
        experiment_id = mlflow.create_experiment(
            EXPERIMENT_NAME,
            artifact_location=f"mlflow-artifacts/{EXPERIMENT_NAME}"
        )
        print(f"✅ Expérience '{EXPERIMENT_NAME}' créée (ID: {experiment_id})")
    else:
        experiment_id = experiment.experiment_id
        print(f"📊 Expérience '{EXPERIMENT_NAME}' existante (ID: {experiment_id})")
    
    mlflow.set_experiment(EXPERIMENT_NAME)
    return experiment_id


def log_model_training(
    model,
    model_name: str,
    metrics: dict,
    params: dict = None,
    artifacts: dict = None,
    tags: dict = None,
    input_example=None,
    signature=None
):
    """
    Log un entraînement de modèle dans MLflow.
    
    Args:
        model: Le modèle entraîné
        model_name: Nom du modèle (ex: "Random Forest")
        metrics: Dict des métriques (accuracy, f1_score, etc.)
        params: Dict des hyperparamètres
        artifacts: Dict {nom: chemin} des artifacts à logger
        tags: Dict des tags additionnels
        input_example: Exemple d'input pour la signature du modèle
        signature: Signature MLflow du modèle
    
    Returns:
        run_id: L'ID du run MLflow
    """
    with mlflow.start_run(run_name=f"{model_name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}") as run:
        run_id = run.info.run_id
        
        # Log des tags
        mlflow.set_tag("model_type", model_name)
        mlflow.set_tag("project", "mindpulse")
        mlflow.set_tag("task", "binary_classification")
        if tags:
            for key, value in tags.items():
                mlflow.set_tag(key, value)
        
        # Log des paramètres
        if params:
            mlflow.log_params(params)
        
        # Log des métriques
        for metric_name, metric_value in metrics.items():
            mlflow.log_metric(metric_name, metric_value)
        
        # Log du modèle sklearn
        mlflow.sklearn.log_model(
            model,
            artifact_path="model",
            input_example=input_example,
            signature=signature
        )
        
        # Log des artifacts supplémentaires (fichiers pickle, etc.)
        if artifacts:
            for artifact_name, artifact_path in artifacts.items():
                if Path(artifact_path).exists():
                    mlflow.log_artifact(artifact_path, artifact_name)
        
        print(f"✅ Run MLflow enregistré: {run_id}")
        print(f"   📊 Métriques: {metrics}")
        
        return run_id


def compare_and_register_best_model(metrics: dict, model_name: str, run_id: str):
    """
    Compare les métriques avec le modèle en production et enregistre si meilleur.
    
    Args:
        metrics: Dict des métriques du nouveau modèle
        model_name: Nom du type de modèle
        run_id: ID du run MLflow
    
    Returns:
        registered: True si le modèle a été enregistré comme nouveau champion
    """
    client = MlflowClient()
    
    # Vérifier si un modèle existe déjà en production
    try:
        latest_versions = client.get_latest_versions(MODEL_NAME, stages=["Production"])
        
        if latest_versions:
            # Récupérer les métriques du modèle en production
            prod_run_id = latest_versions[0].run_id
            prod_run = client.get_run(prod_run_id)
            prod_accuracy = float(prod_run.data.metrics.get("accuracy", 0))
            
            new_accuracy = metrics.get("accuracy", 0)
            
            if new_accuracy > prod_accuracy:
                print(f"🎯 Nouveau modèle meilleur! ({new_accuracy:.4f} > {prod_accuracy:.4f})")
                _register_model_to_production(client, run_id)
                return True
            else:
                print(f"ℹ️ Modèle existant conservé ({prod_accuracy:.4f} >= {new_accuracy:.4f})")
                # Enregistrer quand même dans le registry mais pas en production
                _register_model_staging(client, run_id)
                return False
        else:
            # Pas de modèle en production, enregistrer celui-ci
            print("🆕 Premier modèle, enregistrement en production")
            _register_model_to_production(client, run_id)
            return True
            
    except Exception as e:
        # Le modèle n'existe pas encore dans le registry
        print(f"🆕 Création du modèle dans le registry: {MODEL_NAME}")
        _register_model_to_production(client, run_id)
        return True


def _register_model_to_production(client: MlflowClient, run_id: str):
    """Enregistre un modèle en production"""
    model_uri = f"runs:/{run_id}/model"
    
    # Enregistrer le modèle
    mv = mlflow.register_model(model_uri, MODEL_NAME)
    
    # Passer en production
    client.transition_model_version_stage(
        name=MODEL_NAME,
        version=mv.version,
        stage="Production",
        archive_existing_versions=True
    )
    
    print(f"✅ Modèle enregistré en production (version {mv.version})")


def _register_model_staging(client: MlflowClient, run_id: str):
    """Enregistre un modèle en staging"""
    model_uri = f"runs:/{run_id}/model"
    
    mv = mlflow.register_model(model_uri, MODEL_NAME)
    
    client.transition_model_version_stage(
        name=MODEL_NAME,
        version=mv.version,
        stage="Staging"
    )
    
    print(f"📦 Modèle enregistré en staging (version {mv.version})")


def load_production_model():
    """Charge le modèle en production depuis MLflow"""
    model_uri = f"models:/{MODEL_NAME}/Production"
    
    try:
        model = mlflow.sklearn.load_model(model_uri)
        print(f"✅ Modèle de production chargé: {MODEL_NAME}")
        return model
    except Exception as e:
        print(f"⚠️ Impossible de charger le modèle de production: {e}")
        return None


def get_model_info():
    """Récupère les informations sur le modèle en production"""
    client = MlflowClient()
    
    try:
        versions = client.get_latest_versions(MODEL_NAME, stages=["Production"])
        
        if versions:
            version = versions[0]
            run = client.get_run(version.run_id)
            
            return {
                "model_name": MODEL_NAME,
                "version": version.version,
                "stage": version.current_stage,
                "run_id": version.run_id,
                "metrics": run.data.metrics,
                "params": run.data.params,
                "tags": run.data.tags,
                "created_at": version.creation_timestamp
            }
        return None
    except Exception as e:
        print(f"⚠️ Erreur lors de la récupération des infos modèle: {e}")
        return None


def log_prediction_metrics(predictions_count: int, avg_confidence: float = None):
    """Log des métriques de prédiction pour le monitoring"""
    with mlflow.start_run(run_name=f"predictions_{datetime.now().strftime('%Y%m%d_%H%M%S')}"):
        mlflow.set_tag("type", "inference_metrics")
        mlflow.log_metric("predictions_count", predictions_count)
        if avg_confidence:
            mlflow.log_metric("avg_confidence", avg_confidence)
