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
            {"title": "Informazioni del Paziente", "fields": ["gender", "age", "department"]},
            {"title": "Percorso Accademico",        "fields": ["cgpa", "study"]},
            {"title": "Stile di Vita del Paziente", "fields": ["sleep", "social", "physical", "stress"]},
        ],
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
            {"title": "Informations du Patient",  "fields": ["gender", "age", "department"]},
            {"title": "Parcours Académique",       "fields": ["cgpa", "study"]},
            {"title": "Mode de Vie du Patient",    "fields": ["sleep", "social", "physical", "stress"]},
        ],
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
        background: #0f2027 !important;
        border: 1px solid rgba(224,247,250,0.15) !important;
        border-radius: 12px !important;
    }
    /* Items non-sélectionnés : bien visibles */
    [data-baseweb="popover"] li {
        color: #e0f7fa !important;
        background: transparent !important;
    }
    [data-baseweb="popover"] li:hover {
        background: rgba(77,208,225,0.12) !important;
        color: #ffffff !important;
    }
    /* Item sélectionné : discret, indicateur léger */
    [data-baseweb="popover"] li[aria-selected="true"] {
        background: rgba(77,208,225,0.08) !important;
        color: rgba(224,247,250,0.5) !important;
    }
    [data-baseweb="popover"] li[aria-selected="true"]:hover {
        background: rgba(77,208,225,0.14) !important;
        color: rgba(224,247,250,0.7) !important;
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
    .stNumberInput label, .stSelectbox label, .stSlider label {
        color: #e0f7fa !important;
        font-weight: 500 !important;
        font-size: 0.95rem !important;
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
    [data-baseweb="popover"] ul { background: #0f2027 !important; border: 1px solid rgba(224,247,250,0.15) !important; border-radius: 12px !important; }
    [data-baseweb="popover"] li { color: #e0f7fa !important; }
    [data-baseweb="popover"] li:hover { background: rgba(77,208,225,0.12) !important; }

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

    /* --- Popover (lang picker) --- */
    [data-testid="stPopover"] > div {
        background: rgba(15,32,39,0.97) !important;
        border: 1px solid rgba(224,247,250,0.2) !important;
        border-radius: 14px !important;
        box-shadow: 0 8px 32px rgba(0,0,0,0.5) !important;
    }
    .stRadio label { color: #e0f7fa !important; font-size: 1rem !important; }
    .stRadio [data-testid="stMarkdownContainer"] p { color: #e0f7fa !important; }

</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------------------------
# Session state
# ---------------------------------------------------------------------------
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

t          = TRANSLATIONS[st.session_state.lang]
FORM_STEPS = t["form_steps"]
GENDER_MAP = GENDER_MAPS[st.session_state.lang]
DEPT_MAP   = DEPT_MAPS[st.session_state.lang]

# ---------------------------------------------------------------------------
# Top bar : sélecteur de langue + photo de profil (alignés à droite)
# ---------------------------------------------------------------------------
LANG_OPTIONS = {"🇮🇹 Italiano": "it", "🇫🇷 Français": "fr"}
LANG_LABELS   = list(LANG_OPTIONS.keys())

_, lang_col, profile_col = st.columns([4.5, 2.2, 0.7])

with lang_col:
    st.markdown('<div class="lang-select">', unsafe_allow_html=True)
    current_label = next(k for k, v in LANG_OPTIONS.items() if v == st.session_state.lang)
    selected = st.selectbox(
        "langue",
        LANG_LABELS,
        index=LANG_LABELS.index(current_label),
        label_visibility="collapsed",
        key="lang_select",
    )
    new_lang = LANG_OPTIONS[selected]
    if new_lang != st.session_state.lang:
        st.session_state.lang = new_lang
        st.session_state.form_data = {}
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

with profile_col:
    st.markdown("""
    <div style="display:flex; justify-content:center; align-items:center; height:100%;">
        <div class="profile-circle">
            <svg viewBox="0 0 100 100" xmlns="http://www.w3.org/2000/svg">
                <circle cx="50" cy="36" r="22" fill="rgba(255,255,255,0.92)"/>
                <ellipse cx="50" cy="94" rx="36" ry="26" fill="rgba(255,255,255,0.92)"/>
            </svg>
        </div>
    </div>
    """, unsafe_allow_html=True)

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
                if field_key == "gender":
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
                            prediction = response.json().get("prediction", 0)
                            st.session_state.prediction = prediction
                            st.session_state.api_payload = form_data_for_api
                            st.session_state.step = "result"
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

    if is_at_risk:
        st.markdown(f"""
        <div class="result-card result-positive">
            <div class="result-icon">{t["result_risk_icon"]}</div>
            <div class="result-title">{t["result_risk_title"]}</div>
            <div class="result-desc">{t["result_risk_desc"]}</div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.markdown(f'<div class="section-title">{t["prescriptions_title"]}</div>', unsafe_allow_html=True)
        st.markdown(t["prescriptions_intro"])
        for item in t["prescriptions"]:
            st.markdown(f"- {item}")
        st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div class="result-card result-negative">
            <div class="result-icon">{t["result_ok_icon"]}</div>
            <div class="result-title">{t["result_ok_title"]}</div>
            <div class="result-desc">{t["result_ok_desc"]}</div>
        </div>
        """, unsafe_allow_html=True)

    # Feedback
    st.markdown('<div class="feedback-box">', unsafe_allow_html=True)
    st.markdown(f'<div class="feedback-title">{t["feedback_title"]}</div>', unsafe_allow_html=True)
    st.markdown(t["feedback_desc"])

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
        if st.button(t["btn_send_feedback"], use_container_width=True):
            feedback_payload = {
                "features":   form_data,
                "prediction": int(prediction),
                "actual":     1 if actual_status == t["feedback_options"][1] else 0,
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
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div style="margin-top: 2rem;"></div>', unsafe_allow_html=True)
    if st.button(t["btn_new_patient"], use_container_width=True):
        st.session_state.step = "form"
        st.session_state.form_step = 0
        st.session_state.prediction = None
        st.session_state.form_data = {}
        st.session_state.api_payload = {}
        st.rerun()

# ---------------------------------------------------------------------------
# Footer
# ---------------------------------------------------------------------------
st.markdown(f"""
<div class="footer">
    <strong>NeuroMood</strong> &mdash; {t["footer_subtitle"]}<br>
    M1 DataEng &middot; Ynov Campus &middot; 2025-2026
</div>
""", unsafe_allow_html=True)
