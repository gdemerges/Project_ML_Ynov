import streamlit as st
import requests

# ---------------------------------------------------------------------------
# Translations
# ---------------------------------------------------------------------------
TRANSLATIONS = {
    "it": {
        "page_title": "NeuroMood - Strumento di Supporto alla Diagnosi",
        "hero_subtitle": "Strumento di supporto alla diagnosi — Valutazione del rischio di depressione",
        "step_counter": "Fase {current} di {total}",
        "form_steps": [
            {"title": "Informazioni del Paziente", "fields": ["name", "gender", "age", "department"]},
            {"title": "Percorso Accademico",        "fields": ["cgpa", "study"]},
            {"title": "Stile di Vita del Paziente", "fields": ["sleep", "social", "physical", "stress"]},
        ],
        "name_label":     "Nome del paziente",
        "gender_label":   "Sesso del paziente",
        "gender_options": ["Uomo", "Donna"],
        "age_label":      "Quanti anni ha il paziente?",
        "dept_label":     "In quale dipartimento studia il paziente?",
        "dept_options":   ["Scienze", "Ingegneria", "Medicina", "Arte", "Economia"],
        "cgpa_label":     "Qual è la sua media generale (/20)?",
        "study_label":    "Quante ore al giorno studia?",
        "sleep_label":    "Quante ore dorme il paziente per notte?",
        "social_label":   "Tempo trascorso sui social media (ore/giorno)?",
        "physical_label": "Attività fisica settimanale del paziente (min/settimana)?",
        "stress_label":   "Livello di stress percepito dal paziente (1-10)?",
        "btn_prev":    "⬅️ Precedente",
        "btn_next":    "Successivo ➡️",
        "btn_analyze": "🔮 Avvia Analisi",
        "review_title":        "✅ Riepilogo del Paziente",
        "review_patient_info": "👤 Informazioni del Paziente",
        "review_academic":     "📚 Percorso Accademico",
        "review_lifestyle":    "💪 Stile di Vita",
        "lbl_name":          "Nome :",
        "lbl_gender":        "Sesso :",
        "lbl_age":           "Età :",
        "lbl_age_unit":      "anni",
        "lbl_dept":          "Dipartimento :",
        "lbl_cgpa":          "Media generale :",
        "lbl_study":         "Ore di studio / giorno :",
        "lbl_study_unit":    "h",
        "lbl_sleep":         "Sonno :",
        "lbl_sleep_unit":    "h / notte",
        "lbl_social":        "Social media :",
        "lbl_social_unit":   "h / giorno",
        "lbl_physical":      "Attività fisica :",
        "lbl_physical_unit": "min / settimana",
        "lbl_stress":        "Stress :",
        "lbl_stress_unit":   "/ 10",
        "lbl_not_filled":    "Non compilato",
        "spinner_text":       "🔄 Analisi del profilo del paziente...",
        "result_risk_icon":   "⚠️",
        "result_risk_title":  "Rischio di Depressione Rilevato",
        "result_risk_desc":   "Il modello indica un potenziale rischio di depressione per questo paziente. Si raccomanda una valutazione clinica approfondita.",
        "result_ok_icon":     "✅",
        "result_ok_title":    "Nessun Rischio Significativo",
        "result_ok_desc":     "Il modello non indica un rischio significativo di depressione per questo paziente. Il paziente sembra mantenere un buon equilibrio di vita.",
        "prescriptions_title": "📋 Prescrizioni Raccomandate",
        "prescriptions_intro": "Ecco le raccomandazioni da trasmettere al paziente per migliorare il suo benessere:",
        "prescriptions": [
            "**🎬 Fare una maratona de Il Signore degli Anelli** — Terapia cinematografica immersiva (durata: 11h34 versione lunga)",
            "**🍰 Mangiare pasticcini** — Aumento del tasso di serotonina per via gustativa",
            "**🥾 Fare escursioni** — Silvoterapia e riconnessione con la natura",
            "**🤘 Fare pogo** — Liberazione di endorfine tramite espressione corporea intensa",
            "**✊ Distruggere il capitalismo** — Trattamento di fondo per eliminare la causa strutturale del malessere",
        ],
        "feedback_title":    "📊 Riscontro Clinico",
        "feedback_desc":     "La tua diagnosi clinica permette di migliorare la precisione del modello.",
        "feedback_question": "Il paziente presenta effettivamente sintomi di depressione?",
        "feedback_options":  ["No", "Sì"],
        "btn_send_feedback": "Invia la Diagnosi",
        "feedback_success":  "✅ Diagnosi registrata (totale: {total})",
        "feedback_retrain":  "🔄 Riaddestramento del modello avviato!",
        "btn_new_patient":   "🔄 Nuovo Paziente",
        "btn_download_csv":  "📥 Scarica CSV pazienti",
        "csv_no_data":       "Nessun paziente nella cronologia.",
        "footer_subtitle":   "Strumento di Supporto alla Diagnosi",
        "info_note": "<strong>ℹ️ Nota :</strong> Questo strumento di supporto alla diagnosi si basa su un modello di Machine Learning. Non sostituisce il giudizio clinico del medico. I dati vengono elaborati localmente.",
        "lang_picker_label": "Lingua",
        "flag": "🇮🇹",
        "error_api":         "❌ Errore API: {status} - {text}",
        "error_connection":  "❌ Impossibile raggiungere l'API. Assicurarsi che il contenitore di servizio sia in esecuzione.\n\nDettaglio: {error}",
        "error_unexpected":  "❌ Errore imprevisto ({type}): {error}",
        "error_feedback":    "❌ Errore: {status}",
    },
    "fr": {
        "page_title": "NeuroMood - Outil d'Aide au Diagnostic",
        "hero_subtitle": "Outil d'aide au diagnostic — Évaluation du risque de dépression",
        "step_counter": "Étape {current} sur {total}",
        "form_steps": [
            {"title": "Informations du Patient",  "fields": ["name", "gender", "age", "department"]},
            {"title": "Parcours Académique",       "fields": ["cgpa", "study"]},
            {"title": "Mode de Vie du Patient",    "fields": ["sleep", "social", "physical", "stress"]},
        ],
        "name_label":     "Nom du patient",
        "gender_label":   "Genre du patient",
        "gender_options": ["Homme", "Femme"],
        "age_label":      "Quel âge a le patient ?",
        "dept_label":     "Dans quel département étudie le patient ?",
        "dept_options":   ["Science", "Ingénierie", "Médecine", "Arts", "Affaires"],
        "cgpa_label":     "Quelle est sa moyenne générale (/20) ?",
        "study_label":    "Combien d'heures par jour étudie-t-il/elle ?",
        "sleep_label":    "Combien d'heures dort le patient par nuit ?",
        "social_label":   "Temps passé sur les réseaux sociaux (h/jour) ?",
        "physical_label": "Activité physique hebdomadaire du patient (min/semaine) ?",
        "stress_label":   "Niveau de stress ressenti par le patient (1-10) ?",
        "btn_prev":    "⬅️ Précédent",
        "btn_next":    "Suivant ➡️",
        "btn_analyze": "🔮 Lancer l'Analyse",
        "review_title":        "✅ Récapitulatif du Patient",
        "review_patient_info": "👤 Informations du Patient",
        "review_academic":     "📚 Parcours Académique",
        "review_lifestyle":    "💪 Mode de Vie",
        "lbl_name":          "Nom :",
        "lbl_gender":        "Genre :",
        "lbl_age":           "Âge :",
        "lbl_age_unit":      "ans",
        "lbl_dept":          "Département :",
        "lbl_cgpa":          "Moyenne générale :",
        "lbl_study":         "Heures d'étude / jour :",
        "lbl_study_unit":    "h",
        "lbl_sleep":         "Sommeil :",
        "lbl_sleep_unit":    "h / nuit",
        "lbl_social":        "Réseaux sociaux :",
        "lbl_social_unit":   "h / jour",
        "lbl_physical":      "Activité physique :",
        "lbl_physical_unit": "min / semaine",
        "lbl_stress":        "Stress :",
        "lbl_stress_unit":   "/ 10",
        "lbl_not_filled":    "Non renseigné",
        "spinner_text":       "🔄 Analyse du profil du patient...",
        "result_risk_icon":   "⚠️",
        "result_risk_title":  "Risque de Dépression Détecté",
        "result_risk_desc":   "Le modèle indique un risque potentiel de dépression pour ce patient. Une évaluation clinique approfondie est recommandée.",
        "result_ok_icon":     "✅",
        "result_ok_title":    "Pas de Risque Significatif",
        "result_ok_desc":     "Le modèle n'indique pas de risque significatif de dépression pour ce patient. Le patient semble maintenir un bon équilibre de vie.",
        "prescriptions_title": "📋 Prescriptions Recommandées",
        "prescriptions_intro": "Voici les recommandations à transmettre au patient pour améliorer son bien-être :",
        "prescriptions": [
            "**🎬 Faire un marathon Le Seigneur des Anneaux** — Thérapie cinématographique immersive (durée : 11h34 version longue)",
            "**🍰 Manger des pâtisseries** — Augmentation du taux de sérotonine par voie gustative",
            "**🥾 Randonner** — Sylvothérapie et reconnexion avec la nature",
            "**🤘 Pogoter** — Libération d'endorphines par expression corporelle intensive",
            "**✊ Détruire le capitalisme** — Traitement de fond pour éradiquer la cause structurelle du mal-être",
        ],
        "feedback_title":    "📊 Retour Clinique",
        "feedback_desc":     "Votre diagnostic clinique permet d'améliorer la précision du modèle.",
        "feedback_question": "Le patient présente-t-il effectivement des symptômes de dépression ?",
        "feedback_options":  ["Non", "Oui"],
        "btn_send_feedback": "Envoyer le Diagnostic",
        "feedback_success":  "✅ Diagnostic enregistré (total: {total})",
        "feedback_retrain":  "🔄 Ré-entraînement du modèle déclenché !",
        "btn_new_patient":   "🔄 Nouveau Patient",
        "btn_download_csv":  "📥 Télécharger CSV patients",
        "csv_no_data":       "Aucun patient dans l'historique.",
        "footer_subtitle":   "Outil d'Aide au Diagnostic",
        "info_note": "<strong>ℹ️ Note :</strong> Cet outil d'aide au diagnostic repose sur un modèle de Machine Learning. Il ne se substitue pas au jugement clinique du praticien. Les données sont traitées localement.",
        "lang_picker_label": "Langue",
        "flag": "🇫🇷",
        "error_api":         "❌ Erreur API: {status} - {text}",
        "error_connection":  "❌ Impossible de joindre l'API. Veuillez vous assurer que le conteneur de service est en cours d'exécution.\n\nDétail: {error}",
        "error_unexpected":  "❌ Erreur inattendue ({type}): {error}",
        "error_feedback":    "❌ Erreur: {status}",
    },
}

GENDER_MAPS = {
    "it": {"Uomo": "Male",  "Donna": "Female"},
    "fr": {"Homme": "Male", "Femme": "Female"},
}
DEPT_MAPS = {
    "it": {"Scienze": "Science", "Ingegneria": "Engineering", "Medicina": "Medical", "Arte": "Arts", "Economia": "Business"},
    "fr": {"Science": "Science", "Ingénierie": "Engineering", "Médecine": "Medical", "Arts": "Arts", "Affaires": "Business"},
}

# ---------------------------------------------------------------------------
# Config
# ---------------------------------------------------------------------------
st.set_page_config(
    page_title="NeuroMood",
    page_icon="🩺",
    layout="centered",
    initial_sidebar_state="collapsed",
)

API_URL      = "http://serving-api:8080/predict"
FEEDBACK_URL = "http://serving-api:8080/feedback"

# ---------------------------------------------------------------------------
# CSS moderne - Glassmorphism + Gradients
# ---------------------------------------------------------------------------
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

    /* --- Global --- */
    .stApp {
        background: linear-gradient(160deg, #0f2027 0%, #203a43 40%, #2c5364 100%);
        font-family: 'Inter', sans-serif;
    }

    /* Hide Streamlit branding */
    #MainMenu, footer, header {visibility: hidden;}
    .block-container {
        padding: 0.5rem 1rem 2rem;
        position: relative;
        z-index: 1;
        max-width: 740px;
    }

    /* ---- Top-right topbar ---- */
    .topbar-row {
        display: flex;
        justify-content: flex-end;
        align-items: center;
        gap: 10px;
        padding: 4px 0 8px;
    }

    /* Profile circle */
    .profile-circle {
        width: 44px;
        height: 44px;
        border-radius: 50%;
        background: linear-gradient(145deg, #26c6da 0%, #00838f 55%, #006064 100%);
        display: flex;
        align-items: flex-end;
        justify-content: center;
        border: 2.5px solid rgba(77,208,225,0.55);
        box-shadow: 0 4px 16px rgba(0,0,0,0.4), 0 0 0 4px rgba(77,208,225,0.10);
        overflow: hidden;
        cursor: default;
        flex-shrink: 0;
        transition: box-shadow 0.25s, border-color 0.25s;
    }
    .profile-circle:hover {
        border-color: rgba(77,208,225,0.9);
        box-shadow: 0 6px 22px rgba(0,0,0,0.45), 0 0 0 5px rgba(77,208,225,0.18);
    }
    .profile-circle svg { width: 80%; height: 80%; }

    /* Language selectbox */
    .lang-select .stSelectbox > div > div {
        background: rgba(255,255,255,0.07) !important;
        border: 1px solid rgba(224,247,250,0.18) !important;
        border-radius: 14px !important;
        color: #e0f7fa !important;
        padding: 0.1rem 0.4rem !important;
        font-size: 0.88rem !important;
        backdrop-filter: blur(12px);
        box-shadow: 0 2px 12px rgba(0,0,0,0.15) !important;
        transition: border-color 0.2s;
        min-height: 40px !important;
    }
    .lang-select .stSelectbox > div > div:hover {
        border-color: rgba(77,208,225,0.45) !important;
    }
    .lang-select .stSelectbox [data-baseweb="select"] span,
    .lang-select .stSelectbox [data-baseweb="select"] div {
        color: #e0f7fa !important;
        font-size: 0.88rem !important;
        font-weight: 500 !important;
    }
    /* Dropdown list */
    [data-baseweb="popover"] ul {
        background: #e0f7fa !important;
        border: 1px solid rgba(15,32,39,0.2) !important;
        border-radius: 12px !important;
    }
    /* Items non-sélectionnés */
    [data-baseweb="popover"] li {
        color: #0f2027 !important;
        background: transparent !important;
    }
    [data-baseweb="popover"] li:hover {
        background: rgba(77,208,225,0.25) !important;
        color: #0f2027 !important;
    }
    /* Item sélectionné */
    [data-baseweb="popover"] li[aria-selected="true"] {
        background: rgba(77,208,225,0.35) !important;
        color: #0f2027 !important;
        font-weight: 600 !important;
    }
    [data-baseweb="popover"] li[aria-selected="true"]:hover {
        background: rgba(77,208,225,0.45) !important;
        color: #0f2027 !important;
    }

    /* --- Header --- */
    .hero {
        text-align: center;
        padding: 2rem 0 3rem;
    }
    .hero-icon {
        font-size: 4rem;
        margin-bottom: 1rem;
        animation: float 3s ease-in-out infinite;
    }
    @keyframes float {
        0%, 100% { transform: translateY(0px); }
        50% { transform: translateY(-10px); }
    }
    .hero-title {
        font-size: 2.5rem;
        font-weight: 700;
        color: #e0f7fa;
        margin-bottom: 0.5rem;
        text-shadow: 0 2px 20px rgba(0,0,0,0.3);
        letter-spacing: -0.5px;
    }
    .hero-subtitle {
        font-size: 1.05rem;
        color: rgba(224,247,250,0.75);
        font-weight: 400;
    }

    /* --- Glass Card --- */
    .glass-card {
        background: rgba(255, 255, 255, 0.08);
        backdrop-filter: blur(25px);
        -webkit-backdrop-filter: blur(25px);
        border-radius: 20px;
        padding: 2.5rem;
        border: 1px solid rgba(255, 255, 255, 0.15);
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.2);
        margin-bottom: 2rem;
        position: relative;
        overflow: hidden;
    }

    /* --- Section Title Card (standalone header) --- */
    .section-title-card {
        background: rgba(255, 255, 255, 0.08);
        backdrop-filter: blur(25px);
        -webkit-backdrop-filter: blur(25px);
        border-radius: 16px;
        padding: 1rem 1.5rem;
        border: 1px solid rgba(255, 255, 255, 0.15);
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.2);
        margin-bottom: 1rem;
    }

    /* --- Section Titles --- */
    .section-title {
        font-size: 1.3rem;
        font-weight: 600;
        color: #e0f7fa;
        margin: 0;
        display: flex;
        align-items: center;
        gap: 0.5rem;
        padding-bottom: 0.5rem;
        border-bottom: 1px solid rgba(224,247,250,0.15);
    }

    /* --- ALL Form Inputs - universal fix --- */
    .stNumberInput label, .stSelectbox label, .stSlider label, .stTextInput label {
        color: #e0f7fa !important;
        font-weight: 500 !important;
        font-size: 0.95rem !important;
    }

    .stTextInput > div > div,
    .stTextInput [data-baseweb="input"],
    .stTextInput [data-baseweb="base-input"] {
        background: rgba(255,255,255,0.08) !important;
        border: 1px solid rgba(224,247,250,0.25) !important;
        border-radius: 10px !important;
    }
    .stTextInput > div > div:focus-within,
    .stTextInput [data-baseweb="input"]:focus-within {
        border-color: #4dd0e1 !important;
        box-shadow: 0 0 0 2px rgba(77,208,225,0.2) !important;
    }
    .stTextInput input,
    .stTextInput [data-baseweb="base-input"] input {
        background: transparent !important;
        border: none !important;
        color: #e0f7fa !important;
        -webkit-text-fill-color: #e0f7fa !important;
        font-weight: 500 !important;
        caret-color: #4dd0e1 !important;
    }
    .stTextInput input:-webkit-autofill,
    .stTextInput input:-webkit-autofill:hover,
    .stTextInput input:-webkit-autofill:focus {
        -webkit-box-shadow: 0 0 0 1000px rgba(15,32,39,0.9) inset !important;
        -webkit-text-fill-color: #e0f7fa !important;
        caret-color: #4dd0e1 !important;
    }

    .stNumberInput input {
        background: rgba(255,255,255,0.1) !important;
        border: 1px solid rgba(224,247,250,0.25) !important;
        border-radius: 10px !important;
        color: #ffffff !important;
        font-weight: 500 !important;
        caret-color: #4dd0e1 !important;
    }
    .stNumberInput input:focus {
        border-color: #4dd0e1 !important;
        box-shadow: 0 0 0 2px rgba(77,208,225,0.2) !important;
    }

    .stNumberInput button {
        color: #e0f7fa !important;
        border-color: rgba(224,247,250,0.25) !important;
        background: rgba(255,255,255,0.08) !important;
    }
    .stNumberInput button:hover {
        background: rgba(77,208,225,0.2) !important;
        border-color: #4dd0e1 !important;
    }

    .stSelectbox > div > div {
        background: rgba(255,255,255,0.1) !important;
        border: 1px solid rgba(224,247,250,0.25) !important;
        border-radius: 10px !important;
        color: #ffffff !important;
    }
    .stSelectbox [data-baseweb="select"] span {
        color: #ffffff !important;
    }

    .stSlider [data-baseweb="slider"] > div > div {
        background: rgba(224,247,250,0.2) !important;
    }
    .stSlider [data-baseweb="slider"] > div > div > div {
        background: linear-gradient(90deg, #26c6da, #4dd0e1) !important;
    }
    .stSlider [data-baseweb="slider"] [role="slider"] {
        background: #e0f7fa !important;
        border-color: #4dd0e1 !important;
        box-shadow: 0 2px 8px rgba(77,208,225,0.4) !important;
    }
    .stSlider [data-testid="stTickBarMin"],
    .stSlider [data-testid="stTickBarMax"],
    .stSlider > div > div > div > div > div {
        color: rgba(224,247,250,0.8) !important;
    }

    /* --- Buttons --- */
    .stButton > button,
    .stFormSubmitButton > button {
        width: 100%;
        background: linear-gradient(135deg, #e0f7fa 0%, #b2ebf2 100%) !important;
        color: #0f2027 !important;
        border: none !important;
        border-radius: 12px !important;
        padding: 0.85rem 2rem !important;
        font-size: 1rem !important;
        font-weight: 600 !important;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
        box-shadow: 0 4px 15px rgba(0,0,0,0.2) !important;
        letter-spacing: 0.2px;
    }
    .stButton > button:hover,
    .stFormSubmitButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 24px rgba(77,208,225,0.3) !important;
        background: linear-gradient(135deg, #b2ebf2 0%, #80deea 100%) !important;
    }
    .stButton > button:active,
    .stFormSubmitButton > button:active {
        transform: translateY(0px);
    }

    /* --- Top bar: language selector --- */
    .lang-select { display: flex; align-items: center; }
    .lang-select .stSelectbox > div > div {
        background: rgba(255,255,255,0.07) !important;
        border: 1px solid rgba(224,247,250,0.18) !important;
        border-radius: 14px !important;
        color: #e0f7fa !important;
        padding: 0.15rem 0.4rem !important;
        font-size: 0.88rem !important;
        backdrop-filter: blur(12px);
        -webkit-backdrop-filter: blur(12px);
        box-shadow: 0 2px 12px rgba(0,0,0,0.15) !important;
        transition: border-color 0.2s, box-shadow 0.2s;
    }
    .lang-select .stSelectbox > div > div:hover {
        border-color: rgba(77,208,225,0.45) !important;
        box-shadow: 0 2px 16px rgba(77,208,225,0.12) !important;
    }
    .lang-select .stSelectbox [data-baseweb="select"] span,
    .lang-select .stSelectbox [data-baseweb="select"] div {
        color: #e0f7fa !important;
        font-size: 0.88rem !important;
        font-weight: 500 !important;
    }
    /* Dropdown list */
    [data-baseweb="popover"] ul { background: #e0f7fa !important; border: 1px solid rgba(15,32,39,0.2) !important; border-radius: 12px !important; }
    [data-baseweb="popover"] li { color: #0f2027 !important; }
    [data-baseweb="popover"] li:hover { background: rgba(77,208,225,0.25) !important; color: #0f2027 !important; }

    /* --- Top bar: profile avatar --- */
    .profile-circle {
        width: 46px;
        height: 46px;
        border-radius: 50%;
        background: linear-gradient(145deg, #26c6da 0%, #00838f 60%, #006064 100%);
        display: flex;
        align-items: flex-end;
        justify-content: center;
        border: 2.5px solid rgba(77,208,225,0.55);
        box-shadow: 0 4px 16px rgba(0,0,0,0.35), 0 0 0 4px rgba(77,208,225,0.10);
        overflow: hidden;
        cursor: default;
        margin-left: auto;
        transition: box-shadow 0.25s, border-color 0.25s;
    }
    .profile-circle:hover {
        border-color: rgba(77,208,225,0.85);
        box-shadow: 0 6px 22px rgba(0,0,0,0.4), 0 0 0 5px rgba(77,208,225,0.18);
    }
    .profile-circle svg { width: 80%; height: 80%; }

    /* --- Result Cards --- */
    .result-card {
        backdrop-filter: blur(20px);
        border-radius: 20px;
        padding: 2.5rem 2rem;
        text-align: center;
        border: 2px solid;
        margin: 2rem 0;
    }
    .result-positive {
        border-color: rgba(239, 83, 80, 0.6);
        background: linear-gradient(135deg, rgba(239,83,80,0.12), rgba(198,40,40,0.08));
    }
    .result-negative {
        border-color: rgba(77, 208, 225, 0.6);
        background: linear-gradient(135deg, rgba(77,208,225,0.12), rgba(38,166,154,0.08));
    }
    .result-icon  { font-size: 4rem; margin-bottom: 1rem; }
    .result-title { font-size: 1.8rem; font-weight: 700; color: #e0f7fa; margin-bottom: 0.5rem; }
    .result-desc  { font-size: 1rem; color: rgba(224,247,250,0.85); line-height: 1.7; }

    /* --- Review Data --- */
    .review-section {
        background: rgba(255,255,255,0.06);
        border-radius: 12px;
        padding: 1.2rem 1.5rem;
        margin-bottom: 1rem;
        border-left: 3px solid rgba(77,208,225,0.5);
    }
    .review-section h4 { color: #4dd0e1 !important; margin: 0 0 0.6rem 0; font-size: 1rem; font-weight: 600; }
    .review-item { color: #e0f7fa; font-size: 0.95rem; padding: 0.2rem 0; line-height: 1.6; }
    .review-item span { color: rgba(224,247,250,0.6); }

    /* --- Feedback Section --- */
    .feedback-box {
        background: rgba(255,255,255,0.06);
        border-radius: 16px;
        padding: 1.5rem;
        margin-top: 2rem;
        border: 1px solid rgba(224,247,250,0.12);
    }
    .feedback-title { font-size: 1.1rem; font-weight: 600; color: #e0f7fa; margin-bottom: 1rem; }

    /* --- Info Box --- */
    .info-box {
        background: rgba(77,208,225,0.08);
        border-radius: 12px;
        padding: 1rem 1.5rem;
        margin: 1rem 0;
        border-left: 4px solid rgba(77,208,225,0.5);
    }
    .info-box p { color: rgba(224,247,250,0.9) !important; margin: 0 !important; font-size: 0.9rem; line-height: 1.5; }

    /* --- Footer --- */
    .footer { text-align: center; padding: 2rem 0 1rem; color: rgba(224,247,250,0.5); font-size: 0.85rem; }

    /* --- Streamlit text elements --- */
    .stMarkdown p, .stMarkdown li { color: #e0f7fa !important; }
    .stMarkdown strong { color: #ffffff !important; }

    /* --- Clean form styling --- */
    .stForm { border: none !important; padding: 0 !important; background: transparent !important; }
    section[data-testid="stForm"] { border: none !important; background: transparent !important; }

    .stMarkdown > hr, .element-container > hr {
        border: none !important; height: 0 !important;
        margin: 0 !important; padding: 0 !important; visibility: hidden !important;
    }

    /* Hide empty Streamlit containers */
    [data-testid="column"] > div:empty,
    .element-container:empty,
    .row-widget:empty { display: none !important; }

    div[data-testid="stVerticalBlock"] > div[data-testid="element-container"]:has(> div:empty) {
        display: none !important;
    }
    .element-container:has(> div[data-testid="stVerticalBlock"] > div:empty),
    div[data-testid="stVerticalBlock"]:has(> div:empty:only-child) {
        display: none !important; height: 0 !important; margin: 0 !important; padding: 0 !important;
    }
    div[data-testid="stVerticalBlock"] > div:empty,
    div[data-testid="stVerticalBlock"] > div > div:empty {
        display: none !important; height: 0 !important; margin: 0 !important; padding: 0 !important;
    }
    section[data-testid="stForm"] { margin-top: 0 !important; padding-top: 0 !important; }

    /* --- Popover panel --- */
    [data-baseweb="layer"] > div {
        background: transparent !important;
    }
    [data-baseweb="popover"] {
        background: rgba(15,32,39,0.98) !important;
        border: 1px solid rgba(77,208,225,0.15) !important;
        border-radius: 16px !important;
        box-shadow: 0 12px 40px rgba(0,0,0,0.5) !important;
        overflow: hidden !important;
        backdrop-filter: blur(24px) !important;
        -webkit-backdrop-filter: blur(24px) !important;
    }
    [data-baseweb="popover"] > div,
    [data-baseweb="popover"] > div > div,
    [data-baseweb="popover"] > div > div > div {
        background: rgba(15,32,39,0.98) !important;
    }

    /* --- Doctor profile pill (topbar) --- */
    .trigger-pill {
        display: flex;
        align-items: center;
        justify-content: flex-end;
        gap: 10px;
        padding: 4px 0;
        white-space: nowrap;
    }
    .trigger-avatar {
        width: 38px; height: 38px;
        border-radius: 50%;
        flex-shrink: 0;
        overflow: hidden;
        border: 2px solid rgba(77,208,225,0.45);
        box-shadow: 0 2px 8px rgba(0,0,0,0.3);
    }
    .trigger-avatar img, .trigger-avatar svg {
        width: 100%; height: 100%; object-fit: cover; display: block;
    }
    .trigger-name  { font-size: 0.82rem; font-weight: 600; color: #e0f7fa; line-height: 1.2; }
    .trigger-role  { font-size: 0.68rem; color: rgba(224,247,250,0.4); line-height: 1.2; }

    /* --- "⋮" popover trigger button --- */
    [data-testid="stPopover"] > button {
        width: 34px !important; height: 34px !important;
        min-width: 34px !important; min-height: 34px !important;
        border-radius: 9px !important;
        background: rgba(255,255,255,0.05) !important;
        border: 1px solid rgba(224,247,250,0.10) !important;
        box-shadow: none !important;
        color: rgba(224,247,250,0.45) !important;
        font-size: 1.1rem !important;
        padding: 0 !important;
        transition: all 0.2s ease !important;
    }
    [data-testid="stPopover"] > button:hover {
        background: rgba(77,208,225,0.09) !important;
        border-color: rgba(77,208,225,0.3) !important;
        color: #4dd0e1 !important;
        transform: none !important; box-shadow: none !important;
    }

    /* --- Doctor card in popover --- */
    .doctor-card {
        display: flex; align-items: center; gap: 12px;
        padding: 10px 14px; border-radius: 14px; margin-bottom: 4px;
        border: 1.5px solid transparent;
    }
    .doctor-card-active  { background: rgba(77,208,225,0.09); border-color: rgba(77,208,225,0.32); }
    .doctor-card-inactive { background: rgba(255,255,255,0.025); border-color: rgba(255,255,255,0.05); }
    .doctor-avatar {
        width: 44px; height: 44px; border-radius: 50%; flex-shrink: 0;
        overflow: hidden; border: 2px solid rgba(77,208,225,0.25);
        box-shadow: 0 2px 8px rgba(0,0,0,0.3);
    }
    .doctor-avatar img, .doctor-avatar svg { width: 100%; height: 100%; object-fit: cover; display: block; }
    .doctor-avatar-active { border-color: rgba(77,208,225,0.65); box-shadow: 0 2px 12px rgba(77,208,225,0.15); }
    .doctor-info { flex: 1; min-width: 0; }
    .doctor-name  { font-size: 0.9rem; font-weight: 600; color: #e0f7fa; line-height: 1.3; }
    .doctor-name-active { color: #4dd0e1; }
    .doctor-specialty { font-size: 0.73rem; color: rgba(224,247,250,0.45); line-height: 1.3; }
    .doctor-badge {
        font-size: 0.65rem; font-weight: 600; color: #4dd0e1;
        background: rgba(77,208,225,0.10); padding: 3px 10px;
        border-radius: 20px; letter-spacing: 0.02em; flex-shrink: 0;
    }

    /* --- Doctor switch: invisible button overlaid on inactive card --- */
    .doctor-card-inactive { cursor: pointer !important; }
    [class*="st-key-doc_"] {
        height: 0 !important;
        overflow: visible !important;
        margin: 0 !important;
        padding: 0 !important;
    }
    [class*="st-key-doc_"] .stButton {
        margin: 0 !important;
    }
    [class*="st-key-doc_"] .stButton > button {
        position: relative !important;
        bottom: 75px !important;
        height: 75px !important;
        width: 100% !important;
        opacity: 0 !important;
        cursor: pointer !important;
        min-height: 0 !important;
        padding: 0 !important;
        margin: 0 !important;
        border: none !important;
        box-shadow: none !important;
        background: transparent !important;
    }

    .stRadio label { color: #e0f7fa !important; font-size: 1rem !important; }
    .stRadio [data-testid="stMarkdownContainer"] p { color: #e0f7fa !important; }

</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------------------------
# Session state
# ---------------------------------------------------------------------------
if "doctor" not in st.session_state:
    st.session_state.doctor = "mikaela"
if "lang" not in st.session_state:
    st.session_state.lang = "it"
if "step" not in st.session_state:
    st.session_state.step = "form"
if "form_step" not in st.session_state:
    st.session_state.form_step = 0
if "prediction" not in st.session_state:
    st.session_state.prediction = None
if "form_data" not in st.session_state:
    st.session_state.form_data = {}
if "api_payload" not in st.session_state:
    st.session_state.api_payload = {}
if "results_history" not in st.session_state:
    st.session_state.results_history = []

t          = TRANSLATIONS[st.session_state.lang]
FORM_STEPS = t["form_steps"]
GENDER_MAP = GENDER_MAPS[st.session_state.lang]
DEPT_MAP   = DEPT_MAPS[st.session_state.lang]

# ---------------------------------------------------------------------------
# Top bar : sélecteur de médecin (pill + popover)
# ---------------------------------------------------------------------------
import base64, pathlib

def _build_avatar(img_path: pathlib.Path, fallback_svg: str) -> str:
    """Return <img> base64 or fallback SVG string."""
    for ext in ("jpg", "jpeg", "png", "webp"):
        p = img_path.with_suffix(f".{ext}")
        if p.exists():
            mime = "image/jpeg" if ext in ("jpg", "jpeg") else f"image/{ext}"
            b64 = base64.b64encode(p.read_bytes()).decode()
            return f'<img src="data:{mime};base64,{b64}" alt="avatar"/>'
    return fallback_svg

_STATIC = pathlib.Path(__file__).parent / "static"
_STATIC.mkdir(exist_ok=True)

MIKAELA_AVATAR = _build_avatar(
    _STATIC / "mikaela",
    '<svg viewBox="0 0 100 100" xmlns="http://www.w3.org/2000/svg">'
    '<defs><linearGradient id="gm" x1="0" y1="0" x2="0" y2="1">'
    '<stop offset="0%" stop-color="#26c6da"/><stop offset="100%" stop-color="#00838f"/>'
    '</linearGradient></defs>'
    '<rect width="100" height="100" rx="50" fill="url(#gm)"/>'
    '<ellipse cx="50" cy="42" rx="28" ry="30" fill="#8B4513"/>'
    '<rect x="22" y="42" width="13" height="28" rx="6" fill="#8B4513"/>'
    '<rect x="65" y="42" width="13" height="28" rx="6" fill="#8B4513"/>'
    '<ellipse cx="50" cy="40" rx="21" ry="23" fill="#FDDCB5"/>'
    '<ellipse cx="50" cy="24" rx="23" ry="10" fill="#8B4513"/>'
    '<ellipse cx="41" cy="41" rx="3" ry="3.3" fill="#fff"/>'
    '<ellipse cx="59" cy="41" rx="3" ry="3.3" fill="#fff"/>'
    '<circle cx="41.5" cy="41.5" r="1.9" fill="#2E7D32"/>'
    '<circle cx="59.5" cy="41.5" r="1.9" fill="#2E7D32"/>'
    '<path d="M44 52 Q50 57 56 52" stroke="#C97C6B" stroke-width="1.3" fill="none" stroke-linecap="round"/>'
    '<ellipse cx="50" cy="92" rx="30" ry="21" fill="#ffffff"/>'
    '<path d="M41 77 Q39 84 43 87" stroke="#4dd0e1" stroke-width="2" fill="none" stroke-linecap="round"/>'
    '<circle cx="43" cy="88" r="2.4" fill="#4dd0e1"/>'
    '</svg>',
)

REBECCA_AVATAR = _build_avatar(
    _STATIC / "rebecca",
    '<svg viewBox="0 0 100 100" xmlns="http://www.w3.org/2000/svg">'
    '<defs><linearGradient id="gr" x1="0" y1="0" x2="0" y2="1">'
    '<stop offset="0%" stop-color="#1a4a55"/><stop offset="100%" stop-color="#0d2830"/>'
    '</linearGradient></defs>'
    '<rect width="100" height="100" rx="50" fill="url(#gr)"/>'
    '<circle cx="50" cy="38" r="20" fill="rgba(255,255,255,0.18)"/>'
    '<ellipse cx="50" cy="90" rx="28" ry="22" fill="rgba(255,255,255,0.18)"/>'
    '</svg>'
)

DOCTORS = {
    "mikaela": {"name": "Mikaela C.", "specialty": "Psychiatre · Napoli", "lang": "it", "flag": "🇮🇹", "avatar": MIKAELA_AVATAR},
    "rebecca":  {"name": "Rebecca C.",  "specialty": "Psychiatre · Lyon",   "lang": "fr", "flag": "🇫🇷", "avatar": REBECCA_AVATAR},
}

current_doc = DOCTORS[st.session_state.doctor]

_, pill_col, popover_col = st.columns([4.2, 2.2, 0.6])

with pill_col:
    st.markdown(
        f'<div class="trigger-pill">'
        f'  <div class="trigger-avatar">{current_doc["avatar"]}</div>'
        f'  <div>'
        f'    <div class="trigger-name">{current_doc["name"]}</div>'
        f'    <div class="trigger-role">{current_doc["specialty"]}</div>'
        f'  </div>'
        f'</div>',
        unsafe_allow_html=True,
    )

with popover_col:
    with st.popover("⋮"):
        st.markdown(
            '<p style="color:rgba(224,247,250,0.45);font-size:0.7rem;margin:0 0 10px;'
            'text-transform:uppercase;letter-spacing:0.1em;font-weight:600;'
            'border-bottom:1px solid rgba(77,208,225,0.10);padding-bottom:8px;">Praticien</p>',
            unsafe_allow_html=True,
        )
        for key, doc in DOCTORS.items():
            is_active = key == st.session_state.doctor
            card_cls   = "doctor-card-active"   if is_active else "doctor-card-inactive"
            avatar_cls = "doctor-avatar-active" if is_active else ""
            name_cls   = "doctor-name-active"   if is_active else ""
            badge      = '<span class="doctor-badge">Actif</span>' if is_active else ""
            card_html = (
                f'<div class="doctor-card {card_cls}">'
                f'  <div class="doctor-avatar {avatar_cls}">{doc["avatar"]}</div>'
                f'  <div class="doctor-info">'
                f'    <div class="doctor-name {name_cls}">{doc["flag"]} {doc["name"]}</div>'
                f'    <div class="doctor-specialty">{doc["specialty"]}</div>'
                f'  </div>'
                f'  {badge}'
                f'</div>'
            )
            if is_active:
                st.markdown(card_html, unsafe_allow_html=True)
            else:
                def _switch(k=key, l=doc["lang"]):
                    st.session_state.doctor = k
                    st.session_state.lang = l
                    st.session_state.form_data = {}
                st.markdown(card_html, unsafe_allow_html=True)
                st.button(
                    f"Sélectionner {doc['name']}",
                    key=f"doc_{key}",
                    on_click=_switch,
                    use_container_width=True,
                )

# ---------------------------------------------------------------------------
# Hero
# ---------------------------------------------------------------------------
st.markdown(f"""
<div class="hero">
    <div class="hero-icon">🩺</div>
    <div class="hero-title">NeuroMood</div>
    <div class="hero-subtitle">{t["hero_subtitle"]}</div>
</div>
""", unsafe_allow_html=True)

# ---------------------------------------------------------------------------
# STEP 1: Form
# ---------------------------------------------------------------------------
if st.session_state.step == "form":
    current_step_index = st.session_state.form_step
    total_steps = len(FORM_STEPS) + 1  # +1 for review

    current_step_index = max(0, min(current_step_index, total_steps - 1))
    st.session_state.form_step = current_step_index

    # Progress indicator
    st.markdown(f"""
    <div style="text-align: center; margin-bottom: 0.5rem;">
        <div style="color: rgba(224,247,250,0.8); font-size: 0.9rem; font-weight: 500;">
            {t["step_counter"].format(current=current_step_index + 1, total=total_steps)}
        </div>
        <div style="background: rgba(224,247,250,0.15); height: 4px; border-radius: 2px; margin: 0.5rem auto 0 auto; max-width: 200px; overflow: hidden;">
            <div style="background: linear-gradient(90deg, #26c6da, #4dd0e1); height: 100%; width: {((current_step_index + 1) / total_steps) * 100}%; transition: width 0.3s ease;"></div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    def next_step():
        if st.session_state.form_step < total_steps - 1:
            st.session_state.form_step += 1
        st.rerun()

    def prev_step():
        if st.session_state.form_step > 0:
            st.session_state.form_step -= 1
        st.rerun()

    if current_step_index < len(FORM_STEPS):
        current_step = FORM_STEPS[current_step_index]
        st.markdown(f'<div class="section-title">📋 {current_step["title"]}</div>', unsafe_allow_html=True)

        lang = st.session_state.lang
        with st.form(f"step_form_{current_step_index}_{lang}", clear_on_submit=False):
            for field_key in current_step["fields"]:
                wkey = f"{field_key}_{current_step_index}_{lang}"
                if field_key == "name":
                    st.session_state.form_data[field_key] = st.text_input(
                        t["name_label"],
                        value=st.session_state.form_data.get(field_key, ""),
                        placeholder="ex: Mario Rossi",
                        key=wkey,
                    )
                elif field_key == "gender":
                    opts = t["gender_options"]
                    stored = st.session_state.form_data.get(field_key, opts[0])
                    idx = opts.index(stored) if stored in opts else 0
                    st.session_state.form_data[field_key] = st.selectbox(
                        t["gender_label"], opts, index=idx, key=wkey
                    )
                elif field_key == "age":
                    st.session_state.form_data[field_key] = st.slider(
                        t["age_label"], 16, 60,
                        value=st.session_state.form_data.get(field_key, 22),
                        step=1, key=wkey
                    )
                elif field_key == "department":
                    opts = t["dept_options"]
                    stored = st.session_state.form_data.get(field_key, opts[0])
                    idx = opts.index(stored) if stored in opts else 0
                    st.session_state.form_data[field_key] = st.selectbox(
                        t["dept_label"], opts, index=idx, key=wkey
                    )
                elif field_key == "cgpa":
                    cgpa_display = st.slider(
                        t["cgpa_label"], 0.0, 20.0,
                        value=st.session_state.form_data.get(field_key, 3.0) * 5.0,
                        step=0.5, key=wkey
                    )
                    st.session_state.form_data[field_key] = cgpa_display / 5.0
                elif field_key == "study":
                    st.session_state.form_data[field_key] = st.slider(
                        t["study_label"], 0.0, 16.0,
                        value=st.session_state.form_data.get(field_key, 4.0),
                        step=0.5, key=wkey
                    )
                elif field_key == "sleep":
                    st.session_state.form_data[field_key] = st.slider(
                        t["sleep_label"], 0.0, 12.0,
                        value=st.session_state.form_data.get(field_key, 7.0),
                        step=0.5, key=wkey
                    )
                elif field_key == "social":
                    st.session_state.form_data[field_key] = st.slider(
                        t["social_label"], 0.0, 16.0,
                        value=st.session_state.form_data.get(field_key, 3.0),
                        step=0.5, key=wkey
                    )
                elif field_key == "physical":
                    st.session_state.form_data[field_key] = st.slider(
                        t["physical_label"], 0, 500,
                        value=st.session_state.form_data.get(field_key, 120),
                        step=10, key=wkey
                    )
                elif field_key == "stress":
                    st.session_state.form_data[field_key] = st.slider(
                        t["stress_label"], 1, 10,
                        value=st.session_state.form_data.get(field_key, 5),
                        step=1, key=wkey
                    )

            col_nav1, col_nav2 = st.columns(2)
            with col_nav1:
                if current_step_index > 0:
                    if st.form_submit_button(t["btn_prev"], use_container_width=True):
                        prev_step()
            with col_nav2:
                if st.form_submit_button(t["btn_next"], use_container_width=True):
                    next_step()

    else:
        # Review step
        st.markdown(f'<div class="section-title">{t["review_title"]}</div>', unsafe_allow_html=True)
        fd = st.session_state.form_data
        cgpa_val = fd.get("cgpa", None)
        cgpa_display = f"{cgpa_val * 5.0:.1f} / 20" if cgpa_val is not None else t["lbl_not_filled"]

        st.markdown(f"""
        <div class="review-section">
            <h4>{t["review_patient_info"]}</h4>
            <div class="review-item"><span>{t["lbl_name"]}</span> {fd.get("name", t["lbl_not_filled"])}</div>
            <div class="review-item"><span>{t["lbl_gender"]}</span> {fd.get("gender", t["lbl_not_filled"])}</div>
            <div class="review-item"><span>{t["lbl_age"]}</span> {fd.get("age", t["lbl_not_filled"])} {t["lbl_age_unit"]}</div>
            <div class="review-item"><span>{t["lbl_dept"]}</span> {fd.get("department", t["lbl_not_filled"])}</div>
        </div>
        <div class="review-section">
            <h4>{t["review_academic"]}</h4>
            <div class="review-item"><span>{t["lbl_cgpa"]}</span> {cgpa_display}</div>
            <div class="review-item"><span>{t["lbl_study"]}</span> {fd.get("study", t["lbl_not_filled"])}{t["lbl_study_unit"]}</div>
        </div>
        <div class="review-section">
            <h4>{t["review_lifestyle"]}</h4>
            <div class="review-item"><span>{t["lbl_sleep"]}</span> {fd.get("sleep", t["lbl_not_filled"])} {t["lbl_sleep_unit"]}</div>
            <div class="review-item"><span>{t["lbl_social"]}</span> {fd.get("social", t["lbl_not_filled"])} {t["lbl_social_unit"]}</div>
            <div class="review-item"><span>{t["lbl_physical"]}</span> {fd.get("physical", t["lbl_not_filled"])} {t["lbl_physical_unit"]}</div>
            <div class="review-item"><span>{t["lbl_stress"]}</span> {fd.get("stress", t["lbl_not_filled"])} {t["lbl_stress_unit"]}</div>
        </div>
        """, unsafe_allow_html=True)

        col_nav1, col_nav2 = st.columns(2)
        with col_nav1:
            if st.button(t["btn_prev"], key="review_prev", use_container_width=True):
                prev_step()
        with col_nav2:
            if st.button(t["btn_analyze"], key="get_prediction", use_container_width=True):
                form_data_for_api = {
                    "Age":                st.session_state.form_data.get("age"),
                    "Gender":             GENDER_MAP.get(st.session_state.form_data.get("gender"), "Male"),
                    "Department":         DEPT_MAP.get(st.session_state.form_data.get("department"), "Science"),
                    "CGPA":               st.session_state.form_data.get("cgpa"),
                    "Sleep_Duration":     st.session_state.form_data.get("sleep"),
                    "Study_Hours":        st.session_state.form_data.get("study"),
                    "Social_Media_Hours": st.session_state.form_data.get("social"),
                    "Physical_Activity":  st.session_state.form_data.get("physical"),
                    "Stress_Level":       st.session_state.form_data.get("stress"),
                }
                with st.spinner(t["spinner_text"]):
                    try:
                        response = requests.post(API_URL, json={"features": form_data_for_api}, timeout=10)
                        if response.status_code == 200:
                            import datetime
                            prediction = response.json().get("prediction", 0)
                            st.session_state.prediction = prediction
                            st.session_state.api_payload = form_data_for_api
                            st.session_state.step = "result"
                            cgpa_raw = st.session_state.form_data.get("cgpa")
                            st.session_state.results_history.append({
                                "Timestamp":           datetime.datetime.now().strftime("%Y-%m-%d %H:%M"),
                                "Nom":                 st.session_state.form_data.get("name", ""),
                                "Age":                 form_data_for_api.get("Age"),
                                "Genre":               form_data_for_api.get("Gender"),
                                "Département":         form_data_for_api.get("Department"),
                                "Moyenne_20":          f"{cgpa_raw * 5:.1f}" if cgpa_raw else "",
                                "Heures_étude_jour":   form_data_for_api.get("Study_Hours"),
                                "Sommeil_nuit":        form_data_for_api.get("Sleep_Duration"),
                                "Réseaux_sociaux_jour":form_data_for_api.get("Social_Media_Hours"),
                                "Activité_physique":   form_data_for_api.get("Physical_Activity"),
                                "Stress_1_10":         form_data_for_api.get("Stress_Level"),
                                "Prédiction":          "Risque" if prediction == 1 else "Pas de risque",
                                "Retour_clinique":     "",
                            })
                            st.rerun()
                        else:
                            st.error(t["error_api"].format(status=response.status_code, text=response.text))
                    except requests.exceptions.ConnectionError as e:
                        st.error(t["error_connection"].format(error=e))
                    except Exception as e:
                        st.error(t["error_unexpected"].format(type=type(e).__name__, error=e))

    st.markdown(f"""
    <div class="info-box"><p>{t["info_note"]}</p></div>
    """, unsafe_allow_html=True)


# ---------------------------------------------------------------------------
# STEP 2: Result
# ---------------------------------------------------------------------------
elif st.session_state.step == "result":
    prediction = st.session_state.prediction
    form_data  = st.session_state.get("api_payload", st.session_state.form_data)
    is_at_risk = prediction == 1

    import re
    def _bold(s):
        return re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', s)

    if is_at_risk:
        st.markdown(f"""
        <div class="result-card result-positive">
            <div class="result-icon">{t["result_risk_icon"]}</div>
            <div class="result-title">{t["result_risk_title"]}</div>
            <div class="result-desc">{t["result_risk_desc"]}</div>
        </div>
        """, unsafe_allow_html=True)

        items_html = "".join(
            f'<li style="margin-bottom:0.55rem;">{_bold(item)}</li>'
            for item in t["prescriptions"]
        )
        st.markdown(f"""
        <div class="glass-card">
            <div class="section-title">{t["prescriptions_title"]}</div>
            <p style="color:rgba(224,247,250,0.85);margin:1rem 0 0.6rem;">{t["prescriptions_intro"]}</p>
            <ul style="color:#e0f7fa;line-height:1.85;padding-left:1.3rem;margin:0;">
                {items_html}
            </ul>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div class="result-card result-negative">
            <div class="result-icon">{t["result_ok_icon"]}</div>
            <div class="result-title">{t["result_ok_title"]}</div>
            <div class="result-desc">{t["result_ok_desc"]}</div>
        </div>
        """, unsafe_allow_html=True)

    # CSS injecté uniquement sur la page résultat pour rendre le st.form comme une glass-card
    st.markdown("""
    <style>
    section[data-testid="stForm"] {
        background: rgba(255,255,255,0.08) !important;
        backdrop-filter: blur(25px) !important;
        -webkit-backdrop-filter: blur(25px) !important;
        border-radius: 20px !important;
        padding: 2.5rem !important;
        border: 1px solid rgba(255,255,255,0.15) !important;
        box-shadow: 0 8px 32px rgba(0,0,0,0.2) !important;
        margin-bottom: 2rem !important;
    }
    </style>
    """, unsafe_allow_html=True)

    # Feedback entièrement dans un st.form → tout dans le même bloc visuel
    with st.form("feedback_form"):
        st.markdown(f"""
        <div class="section-title">{t["feedback_title"]}</div>
        <p style="color:rgba(224,247,250,0.85);margin-top:0.8rem;margin-bottom:1.2rem;">{t["feedback_desc"]}</p>
        """, unsafe_allow_html=True)

        feedback_col1, feedback_col2 = st.columns([3, 1])
        with feedback_col1:
            actual_status = st.selectbox(
                t["feedback_question"],
                t["feedback_options"],
                key="feedback_actual"
            )
        with feedback_col2:
            st.write("")
            st.write("")
            submitted = st.form_submit_button(t["btn_send_feedback"], use_container_width=True)

    if submitted:
        actual_int = 1 if actual_status == t["feedback_options"][1] else 0
        # Mise à jour du retour clinique dans l'historique
        if st.session_state.results_history:
            st.session_state.results_history[-1]["Retour_clinique"] = (
                "Oui" if actual_int == 1 else "Non"
            )
        feedback_payload = {
            "features":   form_data,
            "prediction": int(prediction),
            "actual":     actual_int,
        }
        try:
            fb_response = requests.post(FEEDBACK_URL, json=feedback_payload, timeout=10)
            if fb_response.status_code == 200:
                result = fb_response.json()
                st.success(t["feedback_success"].format(total=result.get("total_feedbacks", 0)))
                if result.get("retrain_triggered"):
                    st.info(t["feedback_retrain"])
            else:
                st.error(t["error_feedback"].format(status=fb_response.status_code))
        except Exception as e:
            st.error(t["error_connection"].format(error=e))

    st.markdown('<div style="margin-top: 2rem;"></div>', unsafe_allow_html=True)

    btn_col, csv_col = st.columns(2)
    with btn_col:
        if st.button(t["btn_new_patient"], use_container_width=True):
            st.session_state.step = "form"
            st.session_state.form_step = 0
            st.session_state.prediction = None
            st.session_state.form_data = {}
            st.session_state.api_payload = {}
            st.rerun()
    with csv_col:
        if st.session_state.results_history:
            import io, csv as _csv
            buf = io.StringIO()
            writer = _csv.DictWriter(buf, fieldnames=st.session_state.results_history[0].keys())
            writer.writeheader()
            writer.writerows(st.session_state.results_history)
            st.download_button(
                label=t["btn_download_csv"],
                data=buf.getvalue().encode("utf-8"),
                file_name="neuromood_patients.csv",
                mime="text/csv",
                use_container_width=True,
            )
        else:
            st.caption(t["csv_no_data"])

# ---------------------------------------------------------------------------
# Footer
# ---------------------------------------------------------------------------
st.markdown(f"""
<div class="footer">
    <strong>NeuroMood</strong> &mdash; {t["footer_subtitle"]}<br>
    M1 DataEng &middot; Ynov Campus &middot; 2025-2026
</div>
""", unsafe_allow_html=True)
