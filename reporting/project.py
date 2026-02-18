import os

import pandas as pd
from evidently.pipeline.column_mapping import ColumnMapping
from evidently.report import Report
from evidently.metric_preset import (
    ClassificationPreset,
    DataDriftPreset,
    DataQualityPreset,
)

# =============================================================================
# CONFIG
# =============================================================================

DATA_DIR = os.getenv("DATA_DIR", "/data")
REPORT_DIR = os.getenv("REPORT_DIR", "/reports")

REF_DATA_PATH = os.path.join(DATA_DIR, "ref_data.csv")
PROD_DATA_PATH = os.path.join(DATA_DIR, "prod_data.csv")

os.makedirs(REPORT_DIR, exist_ok=True)


# =============================================================================
# LOAD DATA
# =============================================================================

def load_data():
    ref_data = pd.read_csv(REF_DATA_PATH)

    # ref_data has PCA_1..PCA_n + target
    # prod_data has PCA_1..PCA_n + target + prediction
    if os.path.exists(PROD_DATA_PATH):
        prod_data = pd.read_csv(PROD_DATA_PATH)
    else:
        print("⚠️  No production data found, using a sample of reference data.")
        prod_data = ref_data.sample(frac=0.1, random_state=42).copy()
        prod_data["prediction"] = prod_data["target"]

    # Ensure ref_data also has a prediction column for classification metrics
    if "prediction" not in ref_data.columns:
        ref_data["prediction"] = ref_data["target"]

    # Align types: target and prediction must be consistent (no mixed float/str)
    for df in (ref_data, prod_data):
        for col in ("target", "prediction"):
            if col in df.columns:
                numeric = pd.to_numeric(df[col], errors="coerce")
                # Only apply numeric conversion if no values were lost
                if numeric.notna().sum() == df[col].notna().sum():
                    df[col] = numeric
                else:
                    df[col] = df[col].astype(str)
    prod_data = prod_data.dropna(subset=["target", "prediction"])
    ref_data = ref_data.dropna(subset=["target", "prediction"])

    return ref_data, prod_data


def build_column_mapping(ref_data, prod_data):
    ref_pca = set(c for c in ref_data.columns if c.startswith("PCA_"))
    prod_pca = set(c for c in prod_data.columns if c.startswith("PCA_"))
    pca_cols = sorted(ref_pca & prod_pca)

    if ref_pca != prod_pca:
        print(f"⚠️  PCA column mismatch — using intersection: {pca_cols}")

    column_mapping = ColumnMapping()
    column_mapping.target = "target"
    column_mapping.prediction = "prediction"
    column_mapping.numerical_features = pca_cols

    return column_mapping


# =============================================================================
# REPORTS
# =============================================================================

def generate_reports(ref_data, prod_data, column_mapping):
    # --- Data Quality Report ---
    print("📊 Generating Data Quality report...")
    data_quality_report = Report(metrics=[DataQualityPreset()])
    data_quality_report.run(
        reference_data=ref_data,
        current_data=prod_data,
        column_mapping=column_mapping,
    )
    dq_path = os.path.join(REPORT_DIR, "data_quality.html")
    data_quality_report.save_html(dq_path)
    print(f"   ✅ Saved to {dq_path}")

    # --- Data Drift Report ---
    print("📊 Generating Data Drift report...")
    data_drift_report = Report(metrics=[DataDriftPreset()])
    data_drift_report.run(
        reference_data=ref_data,
        current_data=prod_data,
        column_mapping=column_mapping,
    )
    dd_path = os.path.join(REPORT_DIR, "data_drift.html")
    data_drift_report.save_html(dd_path)
    print(f"   ✅ Saved to {dd_path}")

    # --- Classification Performance Report ---
    print("📊 Generating Classification Performance report...")
    classification_report = Report(metrics=[ClassificationPreset()])
    classification_report.run(
        reference_data=ref_data,
        current_data=prod_data,
        column_mapping=column_mapping,
    )
    cp_path = os.path.join(REPORT_DIR, "classification_performance.html")
    classification_report.save_html(cp_path)
    print(f"   ✅ Saved to {cp_path}")


# =============================================================================
# MAIN
# =============================================================================

if __name__ == "__main__":
    print("🚀 Starting Evidently Reporting...")
    print("📂 Loading data...")
    ref_data, prod_data = load_data()

    print(f"   Reference data shape: {ref_data.shape}")
    print(f"   Production data shape: {prod_data.shape}")

    column_mapping = build_column_mapping(ref_data, prod_data)

    generate_reports(ref_data, prod_data, column_mapping)

    print("\n✅ All reports generated successfully!")
    print(f"   Reports saved in: {REPORT_DIR}/")
    print(f"   - data_quality.html")
    print(f"   - data_drift.html")
    print(f"   - classification_performance.html")
