"""
DAG Airflow pour le réentraînement automatique du modèle ML
Projet: MindPulse - Student Depression Prediction
"""

from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.bash import BashOperator
from airflow.sensors.filesystem import FileSensor
import pandas as pd
import pickle
import os
from pathlib import Path

# Configuration des chemins
DATA_PATH = Path("/opt/airflow/data")
ARTIFACTS_PATH = Path("/opt/airflow/artifacts")
SCRIPTS_PATH = Path("/opt/airflow/scripts")

# Seuil pour déclencher le réentraînement
RETRAIN_THRESHOLD = 1000  # Nombre de nouvelles données de production


def check_production_data(**context):
    """Vérifie si assez de données de production ont été collectées"""
    prod_data_path = DATA_PATH / "prod_data.csv"

    if not prod_data_path.exists():
        print("❌ Aucune donnée de production trouvée")
        return False

    prod_data = pd.read_csv(prod_data_path)
    n_rows = len(prod_data)

    print(f"📊 Données de production: {n_rows} lignes")

    if n_rows >= RETRAIN_THRESHOLD:
        print(f"✅ Seuil atteint ({n_rows} >= {RETRAIN_THRESHOLD}), réentraînement nécessaire")
        context['task_instance'].xcom_push(key='should_retrain', value=True)
        return True
    else:
        print(f"⏳ Seuil non atteint ({n_rows} < {RETRAIN_THRESHOLD})")
        context['task_instance'].xcom_push(key='should_retrain', value=False)
        return False


def check_model_drift(**context):
    """Détecte le drift des données entre ref_data et prod_data"""
    from evidently.test_suite import TestSuite
    from evidently.tests import TestColumnDrift, TestShareOfDriftedColumns

    ref_data_path = DATA_PATH / "ref_data.csv"
    prod_data_path = DATA_PATH / "prod_data.csv"

    if not ref_data_path.exists() or not prod_data_path.exists():
        print("⚠️ Données manquantes pour la détection de drift")
        return False

    ref_data = pd.read_csv(ref_data_path)
    prod_data = pd.read_csv(prod_data_path)

    # Créer le test suite Evidently
    test_suite = TestSuite(tests=[
        TestShareOfDriftedColumns(lt=0.3),  # Moins de 30% de colonnes avec drift
    ])

    test_suite.run(reference_data=ref_data, current_data=prod_data)
    results = test_suite.as_dict()

    # Vérifier si des tests ont échoué (drift détecté)
    drift_detected = any(test['status'] == 'FAIL' for test in results['tests'])

    if drift_detected:
        print("⚠️ DRIFT DÉTECTÉ - Réentraînement recommandé")
        context['task_instance'].xcom_push(key='drift_detected', value=True)
        return True
    else:
        print("✅ Pas de drift significatif détecté")
        context['task_instance'].xcom_push(key='drift_detected', value=False)
        return False


def backup_current_model(**context):
    """Sauvegarde le modèle actuel avant réentraînement"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    model_path = ARTIFACTS_PATH / "model.pickle"
    pipeline_path = ARTIFACTS_PATH / "preprocessing_pipeline.pickle"

    if model_path.exists():
        backup_model = ARTIFACTS_PATH / f"model_backup_{timestamp}.pickle"
        os.system(f"cp {model_path} {backup_model}")
        print(f"✅ Modèle sauvegardé: {backup_model}")

    if pipeline_path.exists():
        backup_pipeline = ARTIFACTS_PATH / f"preprocessing_pipeline_backup_{timestamp}.pickle"
        os.system(f"cp {pipeline_path} {backup_pipeline}")
        print(f"✅ Pipeline sauvegardé: {backup_pipeline}")


def merge_production_data(**context):
    """Fusionne les données de référence et de production"""
    ref_data_path = DATA_PATH / "ref_data.csv"
    prod_data_path = DATA_PATH / "prod_data.csv"
    merged_path = DATA_PATH / "merged_training_data.csv"

    ref_data = pd.read_csv(ref_data_path)
    prod_data = pd.read_csv(prod_data_path)

    # Fusionner les datasets
    merged_data = pd.concat([ref_data, prod_data], ignore_index=True)

    # Supprimer les doublons
    merged_data = merged_data.drop_duplicates()

    merged_data.to_csv(merged_path, index=False)
    print(f"✅ Données fusionnées: {len(merged_data)} lignes")
    print(f"   - Référence: {len(ref_data)} lignes")
    print(f"   - Production: {len(prod_data)} lignes")


def train_new_model(**context):
    """Entraîne un nouveau modèle sur les données fusionnées"""
    from sklearn.model_selection import train_test_split
    from sklearn.preprocessing import StandardScaler, OneHotEncoder
    from sklearn.compose import ColumnTransformer
    from sklearn.pipeline import Pipeline
    from sklearn.decomposition import PCA
    from sklearn.linear_model import LogisticRegression
    from sklearn.ensemble import RandomForestClassifier
    from xgboost import XGBClassifier
    from sklearn.metrics import accuracy_score, f1_score

    merged_path = DATA_PATH / "merged_training_data.csv"
    data = pd.read_csv(merged_path)

    # Séparer features et target
    X = data.drop(columns=['target'])
    y = data['target']

    # Identifier les colonnes numériques et catégorielles
    numeric_features = X.select_dtypes(include=['int64', 'float64']).columns.tolist()
    categorical_features = X.select_dtypes(include=['object', 'category']).columns.tolist()

    # Pipeline de preprocessing
    preprocessor = ColumnTransformer(
        transformers=[
            ('num', StandardScaler(), numeric_features),
            ('cat', OneHotEncoder(handle_unknown='ignore', sparse_output=False), categorical_features)
        ])

    embedding_pipeline = Pipeline(steps=[
        ('preprocessor', preprocessor),
        ('pca', PCA(n_components=0.95))
    ])

    # Transformer les données
    X_embedded = embedding_pipeline.fit_transform(X)

    # Split train/test
    X_train, X_test, y_train, y_test = train_test_split(
        X_embedded, y, test_size=0.2, random_state=42
    )

    # Entraîner plusieurs modèles
    models = {
        "Logistic Regression": LogisticRegression(max_iter=1000),
        "Random Forest": RandomForestClassifier(n_estimators=100, random_state=42),
        "XGBoost": XGBClassifier(use_label_encoder=False, eval_metric='logloss')
    }

    best_model = None
    best_score = 0
    best_model_name = ""

    print("\n🔄 Comparaison des modèles:")
    for name, model in models.items():
        model.fit(X_train, y_train)
        y_pred = model.predict(X_test)

        acc = accuracy_score(y_test, y_pred)
        f1 = f1_score(y_test, y_pred, average='weighted')

        print(f"   {name}: Accuracy={acc:.4f}, F1-Score={f1:.4f}")

        if acc > best_score:
            best_score = acc
            best_model = model
            best_model_name = name

    print(f"\n🏆 Meilleur modèle: {best_model_name} (Accuracy: {best_score:.4f})")

    # Sauvegarder le meilleur modèle
    with open(ARTIFACTS_PATH / "model.pickle", "wb") as f:
        pickle.dump(best_model, f)

    with open(ARTIFACTS_PATH / "preprocessing_pipeline.pickle", "wb") as f:
        pickle.dump(embedding_pipeline, f)

    print("✅ Nouveau modèle entraîné et sauvegardé")

    # Pousser les métriques dans XCom
    context['task_instance'].xcom_push(key='model_name', value=best_model_name)
    context['task_instance'].xcom_push(key='accuracy', value=best_score)
    context['task_instance'].xcom_push(key='f1_score', value=f1)


def archive_production_data(**context):
    """Archive les données de production après réentraînement"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    prod_data_path = DATA_PATH / "prod_data.csv"
    archive_path = DATA_PATH / f"prod_data_archived_{timestamp}.csv"

    if prod_data_path.exists():
        os.system(f"mv {prod_data_path} {archive_path}")
        print(f"✅ Données de production archivées: {archive_path}")

        # Créer un nouveau fichier prod_data.csv vide
        pd.DataFrame().to_csv(prod_data_path, index=False)
        print("✅ Nouveau fichier prod_data.csv créé")


def notify_retrain_success(**context):
    """Notifie le succès du réentraînement"""
    ti = context['task_instance']
    model_name = ti.xcom_pull(task_ids='train_new_model', key='model_name')
    accuracy = ti.xcom_pull(task_ids='train_new_model', key='accuracy')

    print("\n" + "="*60)
    print("🎉 RÉENTRAÎNEMENT TERMINÉ AVEC SUCCÈS")
    print("="*60)
    print(f"📊 Modèle: {model_name}")
    print(f"📈 Accuracy: {accuracy:.4f}")
    print(f"📅 Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("="*60 + "\n")


# Configuration du DAG
default_args = {
    'owner': 'mindpulse',
    'depends_on_past': False,
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

with DAG(
    'ml_retrain_pipeline',
    default_args=default_args,
    description='Pipeline automatique de réentraînement du modèle ML',
    schedule_interval='@daily',  # Exécution quotidienne
    start_date=datetime(2026, 2, 9),
    catchup=False,
    tags=['ml', 'retraining', 'mindpulse'],
) as dag:

    # Task 1: Vérifier les données de production
    check_prod_data = PythonOperator(
        task_id='check_production_data',
        python_callable=check_production_data,
    )

    # Task 2: Détecter le drift
    detect_drift = PythonOperator(
        task_id='detect_drift',
        python_callable=check_model_drift,
    )

    # Task 3: Sauvegarder le modèle actuel
    backup_model = PythonOperator(
        task_id='backup_current_model',
        python_callable=backup_current_model,
    )

    # Task 4: Fusionner les données
    merge_data = PythonOperator(
        task_id='merge_production_data',
        python_callable=merge_production_data,
    )

    # Task 5: Entraîner le nouveau modèle
    train_model = PythonOperator(
        task_id='train_new_model',
        python_callable=train_new_model,
    )

    # Task 6: Archiver les données de production
    archive_data = PythonOperator(
        task_id='archive_production_data',
        python_callable=archive_production_data,
    )

    # Task 7: Notification de succès
    notify_success = PythonOperator(
        task_id='notify_retrain_success',
        python_callable=notify_retrain_success,
    )

    # Définir le workflow
    [check_prod_data, detect_drift] >> backup_model >> merge_data >> train_model >> archive_data >> notify_success
