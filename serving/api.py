import os
import pickle
from typing import Any, Dict

import pandas as pd
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel


# =============================================================================
# CONFIG
# =============================================================================

ARTIFACTS_DIR = os.getenv("ARTIFACTS_DIR", "/artifacts")

model = None
scaler = None
label_encoder = None
feature_names = None
load_error = None


# =============================================================================
# FASTAPI APP
# =============================================================================

app = FastAPI(
    title="Student Depression Prediction API",
    version="1.0.0"
)


# =============================================================================
# SCHEMAS
# =============================================================================

class PredictRequest(BaseModel):
    features: Dict[str, Any]


class PredictResponse(BaseModel):
    prediction: str


# =============================================================================
# STARTUP
# =============================================================================

@app.on_event("startup")
async def load_artifacts():
    global model, scaler, label_encoder, feature_names, load_error

    model_path = os.path.join(ARTIFACTS_DIR, "model.pkl")
    scaler_path = os.path.join(ARTIFACTS_DIR, "scaler.pkl")
    le_path = os.path.join(ARTIFACTS_DIR, "label_encoder.pkl")
    fn_path = os.path.join(ARTIFACTS_DIR, "feature_names.pkl")

    try:
        with open(model_path, "rb") as f:
            model = pickle.load(f)

        with open(scaler_path, "rb") as f:
            scaler = pickle.load(f)

        with open(le_path, "rb") as f:
            label_encoder = pickle.load(f)

        with open(fn_path, "rb") as f:
            feature_names = pickle.load(f)

        load_error = None

        print("Artifacts loaded successfully")
        print(f"   - Model: {type(model).__name__}")
        print(f"   - Features: {len(feature_names)}")

    except Exception as e:
        load_error = str(e)
        model = None
        scaler = None
        label_encoder = None
        feature_names = None
        print(f"Failed to load artifacts: {load_error}")


# =============================================================================
# ENDPOINTS
# =============================================================================

@app.get("/health")
async def health():
    return {
        "status": "ok" if model is not None else "degraded",
        "model_loaded": model is not None,
        "error": load_error
    }


@app.post("/predict", response_model=PredictResponse)
async def predict(req: PredictRequest):
    if model is None or scaler is None or label_encoder is None or feature_names is None:
        raise HTTPException(status_code=503, detail="Model artifacts not loaded")

    try:
        df = pd.DataFrame([req.features])

        # Missing features
        missing = [c for c in feature_names if c not in df.columns]
        if missing:
            raise HTTPException(
                status_code=400,
                detail=f"Missing feature(s): {missing}"
            )

        # Extra features (ignored)
        extra = [c for c in df.columns if c not in feature_names]
        if extra:
            print(f"Ignored extra features: {extra}")

        # Reorder columns
        df = df[feature_names]

        X_scaled = scaler.transform(df)
        pred_encoded = model.predict(X_scaled)[0]
        pred_label = label_encoder.inverse_transform([pred_encoded])[0]

        return PredictResponse(prediction=str(pred_label))

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.get("/feature-names")
async def get_feature_names():
    if feature_names is None:
        raise HTTPException(status_code=503, detail="Feature names not loaded")

    return {
        "feature_names": list(feature_names),
        "count": len(feature_names)
    }
