"""
Script d'entraînement avec intégration MLflow
Projet: MindPulse - Student Depression Prediction

Ce script entraîne les modèles et log tous les résultats dans MLflow.
"""

import pandas as pd
import numpy as np
import pickle
import os
import sys
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.decomposition import PCA
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from xgboost import XGBClassifier
from sklearn.metrics import (
    accuracy_score, f1_score, precision_score, recall_score,
    roc_auc_score, confusion_matrix, classification_report
)
import mlflow
import mlflow.sklearn
from mlflow.models.signature import infer_signature

# Ajouter le chemin du module mlflow_config
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'mlflow'))
from mlflow_config import (
    setup_mlflow, log_model_training, compare_and_register_best_model,
    MLFLOW_TRACKING_URI, EXPERIMENT_NAME
)

# ==========================================
#  Setup Directories
# ==========================================
os.makedirs("data", exist_ok=True)
os.makedirs("artifacts", exist_ok=True)

# ==========================================
#  Configuration MLflow
# ==========================================
print(f"🔗 Configuration MLflow: {MLFLOW_TRACKING_URI}")
setup_mlflow()

# ==========================================
#  Load Dataset
# ==========================================
DATA_PATH = "data/Student Depression and Lifestyle.csv"

try:
    df = pd.read_csv(DATA_PATH)
    print(f"✅ Dataset Loaded Successfully ({len(df)} rows)")
except FileNotFoundError:
    print(f"❌ Error: File not found at {DATA_PATH}")
    exit()

# ==========================================
#  Preprocessing Configuration
# ==========================================
target_col = 'Depression'

X = df.drop(columns=[target_col])
y = df[target_col].astype(int)

numeric_features = X.select_dtypes(include=['int64', 'float64']).columns
categorical_features = X.select_dtypes(include=['object', 'category']).columns

print(f"📊 Numeric Features: {len(numeric_features)}")
print(f"📊 Categorical Features: {len(categorical_features)}")

# ==========================================
# Build Preprocessing Pipeline
# ==========================================
preprocessor = ColumnTransformer(
    transformers=[
        ('num', StandardScaler(), numeric_features),
        ('cat', OneHotEncoder(handle_unknown='ignore', sparse_output=False), categorical_features)
    ])

PCA_COMPONENTS = 0.95  # Hyperparamètre à tracker

embedding_pipeline = Pipeline(steps=[
    ('preprocessor', preprocessor),
    ('pca', PCA(n_components=PCA_COMPONENTS))
])

# ==========================================
#  Generate & Save Reference Data
# ==========================================
print("🔄 Generating embeddings (PCA vectors)...")
X_embedded = embedding_pipeline.fit_transform(X)

pca_columns = [f"PCA_{i+1}" for i in range(X_embedded.shape[1])]
ref_data = pd.DataFrame(X_embedded, columns=pca_columns)
ref_data['target'] = y.values

ref_data.to_csv("data/ref_data.csv", index=False)
print(f"✅ ref_data.csv saved (Shape: {ref_data.shape})")

# ==========================================
#  Model Training & Comparison with MLflow
# ==========================================
X_train, X_test, y_train, y_test = train_test_split(
    X_embedded, y, test_size=0.2, random_state=42
)

# Modèles avec leurs hyperparamètres
models_config = {
    "Logistic_Regression": {
        "model": LogisticRegression(max_iter=1000, random_state=42),
        "params": {"max_iter": 1000, "solver": "lbfgs", "random_state": 42}
    },
    "Random_Forest": {
        "model": RandomForestClassifier(n_estimators=100, max_depth=10, random_state=42),
        "params": {"n_estimators": 100, "max_depth": 10, "random_state": 42}
    },
    "XGBoost": {
        "model": XGBClassifier(
            n_estimators=100, 
            max_depth=6, 
            learning_rate=0.1,
            use_label_encoder=False, 
            eval_metric='logloss',
            random_state=42
        ),
        "params": {
            "n_estimators": 100, 
            "max_depth": 6, 
            "learning_rate": 0.1,
            "eval_metric": "logloss"
        }
    }
}

best_model = None
best_score = 0
best_model_name = ""
best_run_id = None
all_results = []

print("\n📊 Model Comparison with MLflow Tracking")
print("=" * 60)

for name, config in models_config.items():
    model = config["model"]
    params = config["params"]
    
    # Entraînement
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)
    y_pred_proba = model.predict_proba(X_test)[:, 1] if hasattr(model, 'predict_proba') else None
    
    # Calcul des métriques
    metrics = {
        "accuracy": accuracy_score(y_test, y_pred),
        "f1_score": f1_score(y_test, y_pred, average='weighted'),
        "precision": precision_score(y_test, y_pred, average='weighted'),
        "recall": recall_score(y_test, y_pred, average='weighted'),
    }
    
    if y_pred_proba is not None:
        metrics["roc_auc"] = roc_auc_score(y_test, y_pred_proba)
    
    # Confusion matrix
    cm = confusion_matrix(y_test, y_pred)
    metrics["true_negatives"] = int(cm[0, 0])
    metrics["false_positives"] = int(cm[0, 1])
    metrics["false_negatives"] = int(cm[1, 0])
    metrics["true_positives"] = int(cm[1, 1])
    
    # Ajouter les params de preprocessing
    params["pca_components"] = PCA_COMPONENTS
    params["test_size"] = 0.2
    params["dataset_size"] = len(df)
    
    # Signature du modèle pour MLflow
    signature = infer_signature(X_train, y_pred)
    
    # Log dans MLflow
    run_id = log_model_training(
        model=model,
        model_name=name,
        metrics=metrics,
        params=params,
        tags={
            "training_type": "initial",
            "dataset": "Student Depression and Lifestyle"
        },
        input_example=X_train[:5],
        signature=signature
    )
    
    print(f"   🔹 {name}: Accuracy = {metrics['accuracy']:.4f}, F1 = {metrics['f1_score']:.4f}")
    
    # Stocker les résultats
    all_results.append({
        "name": name,
        "accuracy": metrics['accuracy'],
        "f1_score": metrics['f1_score'],
        "run_id": run_id
    })
    
    # Tracker le meilleur modèle
    if metrics['accuracy'] > best_score:
        best_score = metrics['accuracy']
        best_model = model
        best_model_name = name
        best_run_id = run_id
        best_metrics = metrics

print("=" * 60)
print(f"\n🏆 Winner: {best_model_name} with Accuracy: {best_score:.4f}")

# ==========================================
#  Register Best Model in MLflow Model Registry
# ==========================================
print("\n📦 Registering best model in MLflow Model Registry...")
compare_and_register_best_model(best_metrics, best_model_name, best_run_id)

# ==========================================
#  Save Artifacts for API (backward compatibility)
# ==========================================
with open("artifacts/model.pickle", "wb") as f:
    pickle.dump(best_model, f)

with open("artifacts/preprocessing_pipeline.pickle", "wb") as f:
    pickle.dump(embedding_pipeline, f)

print("\n✅ All artifacts saved:")
print("   - artifacts/model.pickle")
print("   - artifacts/preprocessing_pipeline.pickle")
print(f"   - MLflow Run ID: {best_run_id}")

# ==========================================
#  Summary
# ==========================================
print("\n" + "=" * 60)
print("📊 TRAINING SUMMARY")
print("=" * 60)
print(f"Dataset: {DATA_PATH}")
print(f"Samples: {len(df)}")
print(f"Features: {X_embedded.shape[1]} (after PCA)")
print(f"Best Model: {best_model_name}")
print(f"Accuracy: {best_score:.4f}")
print(f"F1 Score: {best_metrics['f1_score']:.4f}")
print(f"MLflow Experiment: {EXPERIMENT_NAME}")
print(f"MLflow UI: {MLFLOW_TRACKING_URI}")
print("=" * 60)
