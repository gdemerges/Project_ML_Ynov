"""
DAG Airflow pour la génération automatique de rapports Evidently
Projet: MindPulse - Student Depression Prediction
"""

from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.bash import BashOperator
import pandas as pd
from pathlib import Path

# Configuration des chemins
DATA_PATH = Path("/opt/airflow/data")
REPORTS_PATH = Path("/opt/airflow/reports")


def check_data_availability(**context):
    """Vérifie la disponibilité des données pour le reporting"""
    ref_data_path = DATA_PATH / "ref_data.csv"
    prod_data_path = DATA_PATH / "prod_data.csv"

    ref_exists = ref_data_path.exists()
    prod_exists = prod_data_path.exists()

    print(f"📊 Données de référence: {'✅ Disponibles' if ref_exists else '❌ Manquantes'}")
    print(f"📊 Données de production: {'✅ Disponibles' if prod_exists else '❌ Manquantes'}")

    if not ref_exists:
        raise FileNotFoundError("Données de référence manquantes")

    if not prod_exists:
        print("⚠️ Aucune donnée de production - génération de données vides")
        pd.DataFrame().to_csv(prod_data_path, index=False)

    return ref_exists and prod_exists


def generate_data_quality_report(**context):
    """Génère un rapport de qualité des données avec Evidently"""
    from evidently.report import Report
    from evidently.metric_preset import DataQualityPreset

    ref_data_path = DATA_PATH / "ref_data.csv"
    prod_data_path = DATA_PATH / "prod_data.csv"

    ref_data = pd.read_csv(ref_data_path)

    # Vérifier si prod_data est vide
    prod_data = pd.read_csv(prod_data_path)
    if len(prod_data) == 0:
        print("⚠️ Pas de données de production - utilisation des données de référence")
        prod_data = ref_data.sample(min(100, len(ref_data)))

    # Créer le rapport
    report = Report(metrics=[DataQualityPreset()])
    report.run(reference_data=ref_data, current_data=prod_data)

    # Sauvegarder le rapport
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    report_path = REPORTS_PATH / f"data_quality_report_{timestamp}.html"
    REPORTS_PATH.mkdir(exist_ok=True)
    report.save_html(str(report_path))

    print(f"✅ Rapport de qualité généré: {report_path}")


def generate_data_drift_report(**context):
    """Génère un rapport de drift des données avec Evidently"""
    from evidently.report import Report
    from evidently.metric_preset import DataDriftPreset

    ref_data_path = DATA_PATH / "ref_data.csv"
    prod_data_path = DATA_PATH / "prod_data.csv"

    ref_data = pd.read_csv(ref_data_path)
    prod_data = pd.read_csv(prod_data_path)

    if len(prod_data) == 0:
        print("⚠️ Pas de données de production - saut du rapport de drift")
        return

    # Créer le rapport
    report = Report(metrics=[DataDriftPreset()])
    report.run(reference_data=ref_data, current_data=prod_data)

    # Sauvegarder le rapport
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    report_path = REPORTS_PATH / f"data_drift_report_{timestamp}.html"
    report.save_html(str(report_path))

    print(f"✅ Rapport de drift généré: {report_path}")


def generate_model_performance_report(**context):
    """Génère un rapport de performance du modèle"""
    from evidently.report import Report
    from evidently.metric_preset import ClassificationPreset

    ref_data_path = DATA_PATH / "ref_data.csv"
    prod_data_path = DATA_PATH / "prod_data.csv"

    ref_data = pd.read_csv(ref_data_path)
    prod_data = pd.read_csv(prod_data_path)

    if len(prod_data) == 0 or 'target' not in prod_data.columns or 'prediction' not in prod_data.columns:
        print("⚠️ Données insuffisantes pour le rapport de performance")
        return

    # Créer le rapport
    report = Report(metrics=[ClassificationPreset()])
    report.run(
        reference_data=ref_data,
        current_data=prod_data,
        column_mapping={'target': 'target', 'prediction': 'prediction'}
    )

    # Sauvegarder le rapport
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    report_path = REPORTS_PATH / f"model_performance_report_{timestamp}.html"
    report.save_html(str(report_path))

    print(f"✅ Rapport de performance généré: {report_path}")


def cleanup_old_reports(**context):
    """Nettoie les anciens rapports (garde les 10 plus récents)"""
    if not REPORTS_PATH.exists():
        return

    reports = sorted(REPORTS_PATH.glob("*.html"), key=lambda x: x.stat().st_mtime, reverse=True)

    if len(reports) > 10:
        for old_report in reports[10:]:
            old_report.unlink()
            print(f"🗑️ Rapport supprimé: {old_report.name}")

    print(f"✅ Nettoyage terminé - {len(reports[:10])} rapports conservés")


def send_report_summary(**context):
    """Envoie un résumé des rapports générés"""
    ti = context['task_instance']

    print("\n" + "="*60)
    print("📊 RAPPORTS EVIDENTLY GÉNÉRÉS")
    print("="*60)
    print(f"📅 Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"📁 Répertoire: {REPORTS_PATH}")
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
    'evidently_reporting_pipeline',
    default_args=default_args,
    description='Génération automatique de rapports Evidently pour le monitoring',
    schedule_interval='0 */6 * * *',  # Toutes les 6 heures
    start_date=datetime(2026, 2, 9),
    catchup=False,
    tags=['monitoring', 'evidently', 'mindpulse'],
) as dag:

    # Task 1: Vérifier la disponibilité des données
    check_data = PythonOperator(
        task_id='check_data_availability',
        python_callable=check_data_availability,
    )

    # Task 2: Générer le rapport de qualité
    quality_report = PythonOperator(
        task_id='generate_data_quality_report',
        python_callable=generate_data_quality_report,
    )

    # Task 3: Générer le rapport de drift
    drift_report = PythonOperator(
        task_id='generate_data_drift_report',
        python_callable=generate_data_drift_report,
    )

    # Task 4: Générer le rapport de performance
    performance_report = PythonOperator(
        task_id='generate_model_performance_report',
        python_callable=generate_model_performance_report,
    )

    # Task 5: Nettoyer les anciens rapports
    cleanup_reports = PythonOperator(
        task_id='cleanup_old_reports',
        python_callable=cleanup_old_reports,
    )

    # Task 6: Envoyer le résumé
    send_summary = PythonOperator(
        task_id='send_report_summary',
        python_callable=send_report_summary,
    )

    # Définir le workflow
    check_data >> [quality_report, drift_report, performance_report] >> cleanup_reports >> send_summary
