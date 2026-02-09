import os
import pickle
import threading
from typing import Any, Dict

import numpy as np
import pandas as pd
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, f1_score
from sklearn.model_selection import train_test_split

# =============================================================================
# CONFIG
# =============================================================================

ARTIFACTS_DIR = os.getenv("ARTIFACTS_DIR", "/artifacts")
DATA_DIR = os.getenv("DATA_DIR", "/data")
RETRAIN_THRESHOLD = int(os.getenv("RETRAIN_THRESHOLD", "50"))

model = None
preprocessing_pipeline = None
load_error = None
retrain_lock = threading.Lock()

# =============================================================================
# FASTAPI APP
# =============================================================================

app = FastAPI(
    title="Student Depression Prediction API",
    version="1.0.0",
)


# =============================================================================
# SCHEMAS
# =============================================================================

class PredictRequest(BaseModel):
    features: Dict[str, Any]


class PredictResponse(BaseModel):
    prediction: int


class FeedbackRequest(BaseModel):
    features: Dict[str, Any]
    prediction: int
    actual: int


class FeedbackResponse(BaseModel):
    status: str
    total_feedbacks: int
    retrain_triggered: bool


# =============================================================================
# STARTUP
# =============================================================================

@app.on_event("startup")
async def load_artifacts():
    global model, preprocessing_pipeline, load_error

    model_path = os.path.join(ARTIFACTS_DIR, "model.pickle")
    pipeline_path = os.path.join(ARTIFACTS_DIR, "preprocessing_pipeline.pickle")

    try:
        with open(model_path, "rb") as f:
            model = pickle.load(f)

        with open(pipeline_path, "rb") as f:
            preprocessing_pipeline = pickle.load(f)

        load_error = None
        print("Artifacts loaded successfully")
        print(f"   - Model: {type(model).__name__}")
        print(f"   - Pipeline steps: {[s[0] for s in preprocessing_pipeline.steps]}")

    except Exception as e:
        load_error = str(e)
        model = None
        preprocessing_pipeline = None
        print(f"Failed to load artifacts: {load_error}")


# =============================================================================
# HELPERS
# =============================================================================

def retrain_model():
    """Retrain the model on ref_data + prod_data and update artifacts."""
    global model

    ref_path = os.path.join(DATA_DIR, "ref_data.csv")
    prod_path = os.path.join(DATA_DIR, "prod_data.csv")

    ref_df = pd.read_csv(ref_path)
    prod_df = pd.read_csv(prod_path)

    # Both files have PCA_1..PCA_n, target (and prod also has prediction)
    pca_cols = [c for c in ref_df.columns if c.startswith("PCA_")]

    X_ref = ref_df[pca_cols].values
    y_ref = ref_df["target"].values

    X_prod = prod_df[pca_cols].values
    y_prod = prod_df["target"].values

    X_all = np.concatenate([X_ref, X_prod])
    y_all = np.concatenate([y_ref, y_prod])

    X_train, X_test, y_train, y_test = train_test_split(
        X_all, y_all, test_size=0.2, random_state=42
    )

    # Train and compare models
    candidates = {
        "LogisticRegression": LogisticRegression(max_iter=1000),
        "RandomForest": RandomForestClassifier(n_estimators=100, random_state=42),
    }

    best_m = None
    best_acc = 0.0

    for name, m in candidates.items():
        m.fit(X_train, y_train)
        acc = accuracy_score(y_test, m.predict(X_test))
        print(f"   Retrain - {name}: accuracy={acc:.4f}")
        if acc > best_acc:
            best_acc = acc
            best_m = m

    # Save and hot-swap
    model_path = os.path.join(ARTIFACTS_DIR, "model.pickle")
    with open(model_path, "wb") as f:
        pickle.dump(best_m, f)

    model = best_m
    print(f"Model retrained and swapped (accuracy={best_acc:.4f})")


# =============================================================================
# ENDPOINTS
# =============================================================================

@app.get("/health")
async def health():
    return {
        "status": "ok" if model is not None else "degraded",
        "model_loaded": model is not None,
        "error": load_error,
    }


@app.post("/predict", response_model=PredictResponse)
async def predict(req: PredictRequest):
    if model is None or preprocessing_pipeline is None:
        raise HTTPException(status_code=503, detail="Model artifacts not loaded")

    try:
        df = pd.DataFrame([req.features])
        X_embedded = preprocessing_pipeline.transform(df)
        pred = int(model.predict(X_embedded)[0])
        return PredictResponse(prediction=pred)

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.post("/feedback", response_model=FeedbackResponse)
async def feedback(req: FeedbackRequest):
    if preprocessing_pipeline is None:
        raise HTTPException(status_code=503, detail="Pipeline not loaded")

    try:
        # Transform raw features to PCA vector
        df = pd.DataFrame([req.features])
        X_embedded = preprocessing_pipeline.transform(df)

        n_components = X_embedded.shape[1]
        pca_cols = [f"PCA_{i+1}" for i in range(n_components)]

        row = pd.DataFrame(X_embedded, columns=pca_cols)
        row["target"] = req.actual
        row["prediction"] = req.prediction

        # Append to prod_data.csv
        prod_path = os.path.join(DATA_DIR, "prod_data.csv")

        if os.path.exists(prod_path):
            row.to_csv(prod_path, mode="a", header=False, index=False)
        else:
            row.to_csv(prod_path, index=False)

        # Count total feedbacks
        total = len(pd.read_csv(prod_path))

        # Trigger retrain if multiple of k
        retrain_triggered = False
        if total % RETRAIN_THRESHOLD == 0 and total > 0:
            with retrain_lock:
                retrain_model()
            retrain_triggered = True

        return FeedbackResponse(
            status="ok",
            total_feedbacks=total,
            retrain_triggered=retrain_triggered,
        )

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.post("/retrain")
async def manual_retrain():
    """Manually trigger model retraining."""
    prod_path = os.path.join(DATA_DIR, "prod_data.csv")
    if not os.path.exists(prod_path):
        raise HTTPException(status_code=400, detail="No production data available for retraining")

    try:
        with retrain_lock:
            retrain_model()
        return {"status": "ok", "message": "Model retrained successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/feature-names")
async def get_feature_names():
    if preprocessing_pipeline is None:
        raise HTTPException(status_code=503, detail="Pipeline not loaded")

    preprocessor = preprocessing_pipeline.named_steps["preprocessor"]
    feature_names = []
    for name, transformer, columns in preprocessor.transformers_:
        feature_names.extend(columns)

    return {"feature_names": list(feature_names), "count": len(feature_names)}
