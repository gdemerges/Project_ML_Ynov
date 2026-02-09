import streamlit as st
import requests

# ---------------------------------------------------------------------------
# Config
# ---------------------------------------------------------------------------
st.set_page_config(
    page_title="MindPulse - Risque de Dépression Étudiante",
    page_icon="🧠",
    layout="centered",
    initial_sidebar_state="collapsed",
)

API_URL = "http://serving-api:8080/predict"
FEEDBACK_URL = "http://serving-api:8080/feedback"

# ---------------------------------------------------------------------------
# CSS moderne - Glassmorphism + Gradients
# ---------------------------------------------------------------------------
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

    /* --- Global --- */
    .stApp {
        background: linear-gradient(135deg, #2c3e50 0%, #34495e 100%);
        font-family: 'Inter', sans-serif;
    }

    /* Hide Streamlit branding */
    #MainMenu, footer, header {visibility: hidden;}
    .block-container {
        padding: 2rem 1rem;
        position: relative;
        z-index: 1;
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
        color: white;
        margin-bottom: 0.5rem;
        text-shadow: 0 2px 20px rgba(0,0,0,0.2);
    }
    .hero-subtitle {
        font-size: 1.1rem;
        color: rgba(255,255,255,0.85);
        font-weight: 400;
    }

    /* --- Glass Card --- */
    .glass-card {
        background: rgba(255, 255, 255, 0.12);
        backdrop-filter: blur(25px);
        -webkit-backdrop-filter: blur(25px);
        border-radius: 28px;
        padding: 2.5rem;
        border: 1px solid rgba(255, 255, 255, 0.25);
        box-shadow: 0 12px 40px rgba(0, 0, 0, 0.15),
                    inset 0 1px 0 rgba(255, 255, 255, 0.3);
        margin-bottom: 2rem;
        position: relative;
        overflow: hidden;
    }

    .glass-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(255,255,255,0.1), transparent);
        transition: left 0.5s;
    }

    .glass-card:hover::before {
        left: 100%;
    }

    /* --- Section Titles --- */
    .section-title {
        font-size: 1.3rem;
        font-weight: 600;
        color: white;
        margin-bottom: 1.5rem;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }

    /* --- Form Inputs --- */
    .stNumberInput label, .stSelectbox label, .stSlider label {
        color: rgba(255,255,255,0.95) !important;
        font-weight: 500 !important;
        font-size: 0.95rem !important;
    }

    .stNumberInput input, .stSelectbox > div > div {
        background: rgba(255,255,255,0.15) !important;
        border: 1px solid rgba(255,255,255,0.3) !important;
        border-radius: 12px !important;
        color: white !important;
        font-weight: 500;
    }

    .stSlider > div > div > div {
        background: rgba(255,255,255,0.3) !important;
    }

    .stSlider > div > div > div > div {
        background: white !important;
    }

    /* --- Buttons --- */
    .stButton > button {
        width: 100%;
        background: linear-gradient(135deg, #ffffff 0%, #f0f0f0 100%) !important;
        color: #667eea !important;
        border: none !important;
        border-radius: 16px !important;
        padding: 1rem 2rem !important;
        font-size: 1.1rem !important;
        font-weight: 600 !important;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
        box-shadow: 0 4px 15px rgba(0,0,0,0.2),
                    inset 0 1px 0 rgba(255,255,255,0.8) !important;
        position: relative;
        overflow: hidden;
    }

    .stButton > button::before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(102,126,234,0.2), transparent);
        transition: left 0.5s;
    }

    .stButton > button:hover::before {
        left: 100%;
    }

    .stButton > button:hover {
        transform: translateY(-3px) scale(1.02);
        box-shadow: 0 8px 30px rgba(0,0,0,0.3) !important;
    }

    .stButton > button:active {
        transform: translateY(-1px) scale(0.98);
    }

    /* --- Result Cards --- */
    .result-card {
        background: rgba(255,255,255,0.15);
        backdrop-filter: blur(20px);
        border-radius: 20px;
        padding: 2rem;
        text-align: center;
        border: 2px solid;
        margin: 2rem 0;
    }

    .result-positive {
        border-color: rgba(239, 68, 68, 0.5);
        background: linear-gradient(135deg, rgba(239,68,68,0.15), rgba(220,38,38,0.1));
    }

    .result-negative {
        border-color: rgba(34, 197, 94, 0.5);
        background: linear-gradient(135deg, rgba(34,197,94,0.15), rgba(22,163,74,0.1));
    }

    .result-icon {
        font-size: 4rem;
        margin-bottom: 1rem;
    }

    .result-title {
        font-size: 1.8rem;
        font-weight: 700;
        color: white;
        margin-bottom: 0.5rem;
    }

    .result-desc {
        font-size: 1rem;
        color: rgba(255,255,255,0.9);
        line-height: 1.6;
    }

    /* --- Feedback Section --- */
    .feedback-box {
        background: rgba(255,255,255,0.08);
        border-radius: 16px;
        padding: 1.5rem;
        margin-top: 2rem;
        border: 1px solid rgba(255,255,255,0.15);
    }

    .feedback-title {
        font-size: 1.1rem;
        font-weight: 600;
        color: white;
        margin-bottom: 1rem;
    }

    /* --- Info Box --- */
    .info-box {
        background: rgba(255,255,255,0.1);
        border-radius: 12px;
        padding: 1rem 1.5rem;
        margin: 1rem 0;
        border-left: 4px solid rgba(255,255,255,0.5);
    }

    .info-box p {
        color: rgba(255,255,255,0.95) !important;
        margin: 0 !important;
        font-size: 0.95rem;
    }

    /* --- Divider --- */
    .divider {
        height: 1px;
        background: linear-gradient(90deg, transparent, rgba(255,255,255,0.3), transparent);
        margin: 2rem 0;
    }

    /* --- Footer --- */
    .footer {
        text-align: center;
        padding: 2rem 0 1rem;
        color: rgba(255,255,255,0.7);
        font-size: 0.85rem;
    }

    /* --- Success/Error messages --- */
    .stAlert {
        background: rgba(255,255,255,0.15) !important;
        border-radius: 12px !important;
        border: 1px solid rgba(255,255,255,0.2) !important;
    }






    /* --- Clean form styling --- */
    .stForm {
        border: none !important;
        padding: 0 !important;
        background: transparent !important;
    }

    /* Remove borders from forms */
    section[data-testid="stForm"] {
        border: none !important;
        background: transparent !important;
    }

    /* Target ONLY the horizontal divider, not form buttons */
    .stMarkdown > hr,
    .element-container > hr {
        border: none !important;
        height: 0 !important;
        margin: 0 !important;
        padding: 0 !important;
        visibility: hidden !important;
    }

    /* Hide specific empty Streamlit containers that appear after progress bar */
    [data-testid="column"] > div:empty,
    .element-container:empty,
    .row-widget:empty {
        display: none !important;
    }


</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------------------------
# Header
# ---------------------------------------------------------------------------
st.markdown("""
<div class="hero">
    <div class="hero-icon">🧠</div>
    <div class="hero-title">MindPulse</div>
    <div class="hero-subtitle">Évaluation du risque de dépression chez les étudiants</div>
</div>
""", unsafe_allow_html=True)

# ---------------------------------------------------------------------------
# Initialize session state
# ---------------------------------------------------------------------------
if "step" not in st.session_state:
    st.session_state.step = "form"  # form | result
if "form_step" not in st.session_state:
    st.session_state.form_step = 0 # New: current step in multi-step form
if "prediction" not in st.session_state:
    st.session_state.prediction = None
if "form_data" not in st.session_state:
    st.session_state.form_data = {}
if "api_payload" not in st.session_state:
    st.session_state.api_payload = {}

# Define form steps and their fields
FORM_STEPS = [
    {"title": "Informations Démographiques", "fields": ["gender", "age", "department"]},
    {"title": "Profil Académique", "fields": ["cgpa", "study"]},
    {"title": "Habitudes de Vie", "fields": ["sleep", "social", "physical", "stress"]},
]

# Mapping FR -> EN for the ML model
GENDER_MAP = {"Homme": "Male", "Femme": "Female"}
DEPT_MAP = {"Science": "Science", "Ingénierie": "Engineering", "Médecine": "Medical", "Arts": "Arts", "Affaires": "Business"}


# ---------------------------------------------------------------------------
# STEP 1: Form
# ---------------------------------------------------------------------------
if st.session_state.step == "form":
    current_step_index = st.session_state.form_step
    total_steps = len(FORM_STEPS)

    # Progress bar or step indicator is removed.

    # Navigation functions
    def next_step():
        st.session_state.form_step += 1
        st.rerun()

    def prev_step():
        st.session_state.form_step -= 1
        st.rerun()

    if current_step_index < total_steps:
        # Render current step
        current_step = FORM_STEPS[current_step_index]
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        # The section title for each step is removed as per user request.

        with st.form(f"step_form_{current_step_index}", clear_on_submit=False):
            # Input fields for the current step
            for field_key in current_step["fields"]:
                if field_key == "gender":
                    st.session_state.form_data[field_key] = st.selectbox(
                        "Genre", ["Homme", "Femme"],
                        index=["Homme", "Femme"].index(st.session_state.form_data.get(field_key, "Homme")),
                        key=f"{field_key}_{current_step_index}"
                    )
                elif field_key == "age":
                    st.session_state.form_data[field_key] = st.number_input(
                        "Âge", min_value=16, max_value=60,
                        value=st.session_state.form_data.get(field_key, 22),
                        key=f"{field_key}_{current_step_index}"
                    )
                elif field_key == "department":
                    departments = ["Science", "Ingénierie", "Médecine", "Arts", "Affaires"]
                    st.session_state.form_data[field_key] = st.selectbox(
                        "Département", departments,
                        index=departments.index(st.session_state.form_data.get(field_key, "Science")),
                        key=f"{field_key}_{current_step_index}"
                    )
                elif field_key == "cgpa":
                    st.session_state.form_data[field_key] = st.number_input(
                        "CGPA", min_value=0.0, max_value=4.0,
                        value=st.session_state.form_data.get(field_key, 3.0),
                        step=0.1, key=f"{field_key}_{current_step_index}"
                    )
                elif field_key == "study":
                    st.session_state.form_data[field_key] = st.number_input(
                        "Heures d'étude (par jour)", min_value=0.0, max_value=16.0,
                        value=st.session_state.form_data.get(field_key, 4.0),
                        step=0.5, key=f"{field_key}_{current_step_index}"
                    )
                elif field_key == "sleep":
                    st.session_state.form_data[field_key] = st.slider(
                        "Durée du sommeil (heures/jour)", 0.0, 12.0,
                        value=st.session_state.form_data.get(field_key, 7.0),
                        step=0.5, key=f"{field_key}_{current_step_index}"
                    )
                elif field_key == "social":
                    st.session_state.form_data[field_key] = st.slider(
                        "Temps sur les réseaux sociaux (heures/jour)", 0.0, 16.0,
                        value=st.session_state.form_data.get(field_key, 3.0),
                        step=0.5, key=f"{field_key}_{current_step_index}"
                    )
                elif field_key == "physical":
                    st.session_state.form_data[field_key] = st.slider(
                        "Activité physique (min/semaine)", 0, 500,
                        value=st.session_state.form_data.get(field_key, 120),
                        step=10, key=f"{field_key}_{current_step_index}"
                    )
                elif field_key == "stress":
                    st.session_state.form_data[field_key] = st.slider(
                        "Niveau de stress (1-10)", 1, 10,
                        value=st.session_state.form_data.get(field_key, 5),
                        step=1, key=f"{field_key}_{current_step_index}"
                    )
            
            # Navigation buttons
            col_nav1, col_nav2 = st.columns(2)
            with col_nav1:
                if current_step_index > 0:
                    if st.form_submit_button("⬅️ Précédent", use_container_width=True):
                        prev_step()
            with col_nav2:
                if st.form_submit_button("Suivant ➡️", use_container_width=True):
                    next_step()

        st.markdown('</div>', unsafe_allow_html=True)

    else:
        # Review and Submit Step
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        # The section title for the review step is removed as per user request.
        st.write("Veuillez vérifier les informations saisies :")

        display_data = {
            "Âge": st.session_state.form_data.get("age"),
            "Genre": st.session_state.form_data.get("gender"),
            "Département": st.session_state.form_data.get("department"),
            "CGPA": st.session_state.form_data.get("cgpa"),
            "Heures d'étude (par jour)": st.session_state.form_data.get("study"),
            "Durée du sommeil (heures/jour)": st.session_state.form_data.get("sleep"),
            "Temps sur les réseaux sociaux (heures/jour)": st.session_state.form_data.get("social"),
            "Activité physique (min/semaine)": st.session_state.form_data.get("physical"),
            "Niveau de stress (1-10)": st.session_state.form_data.get("stress"),
        }
        
        # Display data in a structured, readable format
        st.markdown("### 📝 Résumé de votre profil")
        st.markdown('<div style="margin: 1rem 0;">', unsafe_allow_html=True)
        for key, value in display_data.items():
            st.write(f"**{key}:** {value}")
        st.markdown('</div>', unsafe_allow_html=True)


        col_nav1, col_nav2 = st.columns(2)
        with col_nav1:
            if st.button("⬅️ Précédent", key="review_prev", use_container_width=True):
                prev_step()
        with col_nav2:
            if st.button("🔮 Obtenir la Prédiction", key="get_prediction", use_container_width=True):
                # Prepare data for API call from session_state
                form_data_for_api = {
                    "Age": st.session_state.form_data.get("age"),
                    "Gender": GENDER_MAP.get(st.session_state.form_data.get("gender"), "Male"),
                    "Department": DEPT_MAP.get(st.session_state.form_data.get("department"), "Science"),
                    "CGPA": st.session_state.form_data.get("cgpa"),
                    "Sleep_Duration": st.session_state.form_data.get("sleep"),
                    "Study_Hours": st.session_state.form_data.get("study"),
                    "Social_Media_Hours": st.session_state.form_data.get("social"),
                    "Physical_Activity": st.session_state.form_data.get("physical"),
                    "Stress_Level": st.session_state.form_data.get("stress"),
                }

                # Call API
                with st.spinner("🔄 Analyse de votre profil..."):
                    try:
                        payload = {"features": form_data_for_api}
                        response = requests.post(
                            API_URL,
                            json=payload,
                            timeout=10
                        )

                        if response.status_code == 200:
                            result = response.json()
                            prediction = result.get("prediction", 0)

                            # Save to session (EN keys for API/feedback, used in result page)
                            st.session_state.prediction = prediction
                            st.session_state.api_payload = form_data_for_api
                            st.session_state.step = "result"
                            st.rerun()
                        else:
                            st.error(f"❌ Erreur API: {response.status_code} - {response.text}")

                    except requests.exceptions.ConnectionError as e:
                        st.error(f"❌ Impossible de joindre l'API. Veuillez vous assurer que le conteneur de service est en cours d'exécution.\n\nDétail: {e}")
                    except Exception as e:
                        st.error(f"❌ Erreur inattendue ({type(e).__name__}): {e}")

        st.markdown('</div>', unsafe_allow_html=True)

    # Info box (retained at the bottom of the form section)
    st.markdown("""
    <div class="info-box">
        <p>
            <strong>ℹ️ Avis de Confidentialité :</strong> Ceci est un modèle ML éducatif à des fins de démonstration.
            Ne remplace pas un avis médical professionnel. Toutes les données sont traitées localement.
        </p>
    </div>
    """, unsafe_allow_html=True)


# ---------------------------------------------------------------------------
# STEP 2: Result
# ---------------------------------------------------------------------------
elif st.session_state.step == "result":
    prediction = st.session_state.prediction
    api_data = st.session_state.get("api_payload", st.session_state.form_data)
    form_data = api_data  # EN keys used for recommendations and feedback

    is_at_risk = prediction == 1

    # Result card
    if is_at_risk:
        st.markdown(f"""
        <div class="result-card result-positive">
            <div class="result-icon">⚠️</div>
            <div class="result-title">Risque Détecté</div>
            <div class="result-desc">
                Le modèle indique un risque potentiel de dépression basé sur votre profil.
                Nous vous recommandons de contacter des services de soutien en santé mentale.
            </div>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div class="result-card result-negative">
            <div class="result-icon">✅</div>
            <div class="result-title">Pas de risque significatif</div>
            <div class="result-desc">
                Basé sur votre profil, le modèle n'indique pas de risque significatif de dépression.
                Continuez à maintenir vos saines habitudes de vie.
            </div>
        </div>
        """, unsafe_allow_html=True)

    # Recommendations
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">💡 Recommandations</div>', unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("**📞 Ressources de Soutien (France)**")
        st.markdown("""
        - **3114** - Numéro national de prévention du suicide
        - **SOS Amitié** - 09 72 39 40 50
        - **Fil Santé Jeunes** - 0 800 235 236
        - **Nightline** - Service d'écoute étudiant
        """)

    with col2:
        st.markdown("**🎯 Conseils Personnalisés**")
        tips = []

        if form_data["Stress_Level"] >= 7:
            tips.append("- Pratiquer la gestion du stress (méditation, respiration)")
        if form_data["Sleep_Duration"] < 6:
            tips.append("- Viser 7 à 9 heures de sommeil par nuit")
        if form_data["Physical_Activity"] < 60:
            tips.append("- Augmenter l'activité physique (150+ min/semaine)")
        if form_data["Social_Media_Hours"] > 5:
            tips.append("- Réduire le temps d'écran et les réseaux sociaux")
        if form_data["Study_Hours"] > 10:
            tips.append("- Équilibrer le temps d'étude avec des pauses")

        if not tips:
            tips = [
                "- Maintenir de saines habitudes",
                "- Rester connecté avec vos amis et votre famille",
                "- Maintenir l'équilibre vie pro/perso"
            ]

        st.markdown("\n".join(tips))

    st.markdown('</div>', unsafe_allow_html=True)

    # Feedback section
    st.markdown('<div class="feedback-box">', unsafe_allow_html=True)
    st.markdown('<div class="feedback-title">📊 Aidez-nous à Améliorer Notre Modèle</div>', unsafe_allow_html=True)
    st.markdown("Votre retour aide à améliorer la précision du modèle au fil du temps.")

    feedback_col1, feedback_col2 = st.columns([3, 1])

    with feedback_col1:
        actual_status = st.selectbox(
            "Souffrez-vous réellement de symptômes de dépression ?",
            ["Non", "Oui"],
            key="feedback_actual"
        )

    with feedback_col2:
        st.write("")  # Spacing
        st.write("")
        if st.button("Envoyer le Retour", use_container_width=True):
            feedback_payload = {
                "features": form_data,
                "prediction": int(prediction),
                "actual": 1 if actual_status == "Oui" else 0,
            }

            try:
                fb_response = requests.post(FEEDBACK_URL, json=feedback_payload, timeout=10)
                if fb_response.status_code == 200:
                    result = fb_response.json()
                    st.success(f"✅ Merci ! Retour enregistré (total: {result.get('total_feedbacks', 0)})")
                    if result.get("retrain_triggered"):
                        st.info("🔄 Ré-entraînement du modèle déclenché !")
                else:
                    st.error(f"❌ Erreur: {fb_response.status_code}")
            except Exception as e:
                st.error(f"❌ Erreur de connexion: {e}")

    st.markdown('</div>', unsafe_allow_html=True)

    # New assessment button
    st.markdown('<div style="margin-top: 2rem;"></div>', unsafe_allow_html=True)
    if st.button("🔄 Nouvelle Évaluation", use_container_width=True):
        st.session_state.step = "form"
        st.session_state.prediction = None
        st.session_state.form_data = {}
        st.session_state.api_payload = {}
        st.rerun()

# ---------------------------------------------------------------------------
# Footer
# ---------------------------------------------------------------------------
st.markdown("""
<div class="footer">
    <strong>MindPulse</strong> &mdash; Projet ML Éducatif<br>
    M1 DataEng &middot; Ynov Campus &middot; 2025-2026
</div>
""", unsafe_allow_html=True)
