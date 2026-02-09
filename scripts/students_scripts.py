import pandas as pd
import numpy as np
import pickle
import os
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.decomposition import PCA
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from xgboost import XGBClassifier
from sklearn.metrics import accuracy_score, f1_score

# ==========================================
#  Setup Directories
# ==========================================
# Create necessary folders if they don't exist
# 'artifacts' will store the model and pipeline for the API 
# 'data' will store the reference data for reporting 
os.makedirs("data", exist_ok=True)
os.makedirs("artifacts", exist_ok=True)

# ==========================================
#  Load Dataset
# ==========================================
DATA_PATH = "data/Student Depression and Lifestyle.csv"

try:
    df = pd.read_csv(DATA_PATH)
    print(" Dataset Loaded Successfully.")
except FileNotFoundError:
    print(f" Error: File not found at {DATA_PATH}.")
    exit()

# ==========================================
#  Preprocessing Configuration
# ==========================================
target_col = 'Depression' 

# Separate Features (X) and Target (y)
X = df.drop(columns=[target_col])

# Convert Boolean Target (True/False) to Integer (1/0)
y = df[target_col].astype(int)

# Automatically identify numeric and categorical columns
numeric_features = X.select_dtypes(include=['int64', 'float64']).columns
categorical_features = X.select_dtypes(include=['object', 'category']).columns

print(f"  Numeric Features: {len(numeric_features)}")
print(f"  Categorical Features: {len(categorical_features)}")

# ==========================================
# Build Preprocessing Pipeline
# ==========================================
# Define how to handle different data types
preprocessor = ColumnTransformer(
    transformers=[
        # Scale numeric features to standard normal distribution
        ('num', StandardScaler(), numeric_features),
        
        # One-Hot Encode categorical features (handle_unknown='ignore' prevents crashes on new data)
        ('cat', OneHotEncoder(handle_unknown='ignore', sparse_output=False), categorical_features)
    ])

# Create the full pipeline: Preprocessor -> PCA
# PCA is used to create vector embeddings as per project requirements
embedding_pipeline = Pipeline(steps=[
    ('preprocessor', preprocessor),
    ('pca', PCA(n_components=0.95)) # Retain 95% variance
])

# ==========================================
#  Generate & Save Reference Data
# ==========================================
print(" Generating embeddings (PCA vectors)...")
X_embedded = embedding_pipeline.fit_transform(X)

# Create a DataFrame for the reference data 
# Naming columns PCA_1, PCA_2, etc.
pca_columns = [f"PCA_{i+1}" for i in range(X_embedded.shape[1])]
ref_data = pd.DataFrame(X_embedded, columns=pca_columns)
ref_data['target'] = y.values # Append target for Evidently AI reporting

# Save ref_data.csv
ref_data.to_csv("data/ref_data.csv", index=False)
print(f" ref_data.csv saved (Shape: {ref_data.shape})")

# ==========================================
#  Model Training & Comparison
# ==========================================
# Split data: 80% Training, 20% Testing
X_train, X_test, y_train, y_test = train_test_split(X_embedded, y, test_size=0.2, random_state=42)

# Define models to compare
models = {
    "Logistic Regression": LogisticRegression(),
    "Random Forest": RandomForestClassifier(n_estimators=100, random_state=42),
    "XGBoost": XGBClassifier(use_label_encoder=False, eval_metric='logloss')
}

best_model = None
best_score = 0
best_model_name = ""

print("\n --- Model Comparison Results ---")
for name, model in models.items():
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)
    
    # Calculate metrics
    acc = accuracy_score(y_test, y_pred)
    f1 = f1_score(y_test, y_pred, average='weighted')
    
    print(f"   🔹 {name}: Accuracy = {acc:.4f}, F1-Score = {f1:.4f}")
    
    # Track the best model
    if acc > best_score:
        best_score = acc
        best_model = model
        best_model_name = name

print(f"\n Winner Model: {best_model_name} with Accuracy: {best_score:.4f}")

# ==========================================
#  Save Artifacts for API
# ==========================================
# Save the best model
with open("artifacts/model.pickle", "wb") as f:
    pickle.dump(best_model, f)

# Save the preprocessing pipeline (Scaler + Encoder + PCA)
# The API will need this to transform new raw user data into vectors
with open("artifacts/preprocessing_pipeline.pickle", "wb") as f:
    pickle.dump(embedding_pipeline, f)

print(" All artifacts saved in 'artifacts/' folder.")
print("   - model.pickle")
print("   - preprocessing_pipeline.pickle")