import streamlit as st
import requests

# ---------------------------------------------------------------------------
# Config
# ---------------------------------------------------------------------------
st.set_page_config(
    page_title="MindPulse - Outil d'Aide au Diagnostic",
    page_icon="🩺",
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
        background: linear-gradient(160deg, #0f2027 0%, #203a43 40%, #2c5364 100%);
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

    /* --- Section Titles --- */
    .section-title {
        font-size: 1.3rem;
        font-weight: 600;
        color: #e0f7fa;
        margin-bottom: 1.5rem;
        display: flex;
        align-items: center;
        gap: 0.5rem;
        padding-bottom: 0.75rem;
        border-bottom: 1px solid rgba(224,247,250,0.15);
    }

    /* --- ALL Form Inputs - universal fix --- */
    /* Labels */
    .stNumberInput label, .stSelectbox label, .stSlider label {
        color: #e0f7fa !important;
        font-weight: 500 !important;
        font-size: 0.95rem !important;
    }

    /* Number inputs */
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

    /* Number input +/- buttons */
    .stNumberInput button {
        color: #e0f7fa !important;
        border-color: rgba(224,247,250,0.25) !important;
        background: rgba(255,255,255,0.08) !important;
    }
    .stNumberInput button:hover {
        background: rgba(77,208,225,0.2) !important;
        border-color: #4dd0e1 !important;
    }

    /* Selectbox */
    .stSelectbox > div > div {
        background: rgba(255,255,255,0.1) !important;
        border: 1px solid rgba(224,247,250,0.25) !important;
        border-radius: 10px !important;
        color: #ffffff !important;
    }
    .stSelectbox [data-baseweb="select"] span {
        color: #ffffff !important;
    }

    /* Slider track */
    .stSlider [data-baseweb="slider"] > div > div {
        background: rgba(224,247,250,0.2) !important;
    }
    /* Slider filled track */
    .stSlider [data-baseweb="slider"] > div > div > div {
        background: linear-gradient(90deg, #26c6da, #4dd0e1) !important;
    }
    /* Slider thumb */
    .stSlider [data-baseweb="slider"] [role="slider"] {
        background: #e0f7fa !important;
        border-color: #4dd0e1 !important;
        box-shadow: 0 2px 8px rgba(77,208,225,0.4) !important;
    }
    /* Slider value label */
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

    .result-icon {
        font-size: 4rem;
        margin-bottom: 1rem;
    }

    .result-title {
        font-size: 1.8rem;
        font-weight: 700;
        color: #e0f7fa;
        margin-bottom: 0.5rem;
    }

    .result-desc {
        font-size: 1rem;
        color: rgba(224,247,250,0.85);
        line-height: 1.7;
    }

    /* --- Review Data --- */
    .review-section {
        background: rgba(255,255,255,0.06);
        border-radius: 12px;
        padding: 1.2rem 1.5rem;
        margin-bottom: 1rem;
        border-left: 3px solid rgba(77,208,225,0.5);
    }
    .review-section h4 {
        color: #4dd0e1 !important;
        margin: 0 0 0.6rem 0;
        font-size: 1rem;
        font-weight: 600;
    }
    .review-item {
        color: #e0f7fa;
        font-size: 0.95rem;
        padding: 0.2rem 0;
        line-height: 1.6;
    }
    .review-item span {
        color: rgba(224,247,250,0.6);
    }

    /* --- Feedback Section --- */
    .feedback-box {
        background: rgba(255,255,255,0.06);
        border-radius: 16px;
        padding: 1.5rem;
        margin-top: 2rem;
        border: 1px solid rgba(224,247,250,0.12);
    }

    .feedback-title {
        font-size: 1.1rem;
        font-weight: 600;
        color: #e0f7fa;
        margin-bottom: 1rem;
    }

    /* --- Info Box --- */
    .info-box {
        background: rgba(77,208,225,0.08);
        border-radius: 12px;
        padding: 1rem 1.5rem;
        margin: 1rem 0;
        border-left: 4px solid rgba(77,208,225,0.5);
    }

    .info-box p {
        color: rgba(224,247,250,0.9) !important;
        margin: 0 !important;
        font-size: 0.9rem;
        line-height: 1.5;
    }

    /* --- Footer --- */
    .footer {
        text-align: center;
        padding: 2rem 0 1rem;
        color: rgba(224,247,250,0.5);
        font-size: 0.85rem;
    }

    /* --- Success/Error messages --- */
    .stAlert {
        background: rgba(255,255,255,0.1) !important;
        border-radius: 12px !important;
        border: 1px solid rgba(224,247,250,0.15) !important;
    }

    /* --- Streamlit text elements --- */
    .stMarkdown p, .stMarkdown li {
        color: #e0f7fa !important;
    }
    .stMarkdown strong {
        color: #ffffff !important;
    }

    /* --- Clean form styling --- */
    .stForm {
        border: none !important;
        padding: 0 !important;
        background: transparent !important;
    }

    section[data-testid="stForm"] {
        border: none !important;
        background: transparent !important;
    }

    .stMarkdown > hr,
    .element-container > hr {
        border: none !important;
        height: 0 !important;
        margin: 0 !important;
        padding: 0 !important;
        visibility: hidden !important;
    }

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
    <div class="hero-icon">🩺</div>
    <div class="hero-title">MindPulse</div>
    <div class="hero-subtitle">Outil d'aide au diagnostic - Évaluation du risque de dépression</div>
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
    {"title": "Informations du Patient", "fields": ["gender", "age", "department"]},
    {"title": "Parcours Académique", "fields": ["cgpa", "study"]},
    {"title": "Mode de Vie du Patient", "fields": ["sleep", "social", "physical", "stress"]},
]

# Mapping FR -> EN for the ML model
GENDER_MAP = {"Homme": "Male", "Femme": "Female"}
DEPT_MAP = {"Science": "Science", "Ingénierie": "Engineering", "Médecine": "Medical", "Arts": "Arts", "Affaires": "Business"}


# ---------------------------------------------------------------------------
# STEP 1: Form
# ---------------------------------------------------------------------------
if st.session_state.step == "form":
    current_step_index = st.session_state.form_step
    total_steps = len(FORM_STEPS) + 1  # +1 for review step

    # Ensure form_step is within valid range
    if current_step_index < 0:
        st.session_state.form_step = 0
        current_step_index = 0
    elif current_step_index > total_steps - 1:
        st.session_state.form_step = total_steps - 1
        current_step_index = total_steps - 1

    # Progress indicator
    st.markdown(f"""
    <div style="text-align: center; margin-bottom: 2rem;">
        <div style="color: rgba(224,247,250,0.8); font-size: 0.9rem; font-weight: 500;">
            Étape {current_step_index + 1} sur {total_steps}
        </div>
        <div style="background: rgba(224,247,250,0.15); height: 4px; border-radius: 2px; margin: 0.5rem auto; max-width: 200px; overflow: hidden;">
            <div style="background: linear-gradient(90deg, #26c6da, #4dd0e1); height: 100%; width: {((current_step_index + 1) / total_steps) * 100}%; transition: width 0.3s ease;"></div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Navigation functions
    def next_step():
        if st.session_state.form_step < total_steps - 1:
            st.session_state.form_step += 1
        st.rerun()

    def prev_step():
        if st.session_state.form_step > 0:
            st.session_state.form_step -= 1
        st.rerun()

    if current_step_index < len(FORM_STEPS):
        # Render current step
        current_step = FORM_STEPS[current_step_index]
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)

        # Add section title
        st.markdown(f'<div class="section-title">📋 {current_step["title"]}</div>', unsafe_allow_html=True)

        with st.form(f"step_form_{current_step_index}", clear_on_submit=False):
            # Input fields for the current step
            for field_key in current_step["fields"]:
                if field_key == "gender":
                    st.session_state.form_data[field_key] = st.selectbox(
                        "Genre du patient", ["Homme", "Femme"],
                        index=["Homme", "Femme"].index(st.session_state.form_data.get(field_key, "Homme")),
                        key=f"{field_key}_{current_step_index}"
                    )
                elif field_key == "age":
                    st.session_state.form_data[field_key] = st.slider(
                        "Quel âge a le patient ?", 16, 60,
                        value=st.session_state.form_data.get(field_key, 22),
                        step=1, key=f"{field_key}_{current_step_index}"
                    )
                elif field_key == "department":
                    departments = ["Science", "Ingénierie", "Médecine", "Arts", "Affaires"]
                    st.session_state.form_data[field_key] = st.selectbox(
                        "Dans quel département étudie le patient ?", departments,
                        index=departments.index(st.session_state.form_data.get(field_key, "Science")),
                        key=f"{field_key}_{current_step_index}"
                    )
                elif field_key == "cgpa":
                    # Display as /20 but store as /4 for API compatibility
                    cgpa_display = st.slider(
                        "Quelle est sa moyenne générale (/20) ?", 0.0, 20.0,
                        value=st.session_state.form_data.get(field_key, 3.0) * 5.0,  # Convert 4 scale to 20 scale for display
                        step=0.5, key=f"{field_key}_{current_step_index}"
                    )
                    st.session_state.form_data[field_key] = cgpa_display / 5.0  # Store as /4 for API
                elif field_key == "study":
                    st.session_state.form_data[field_key] = st.slider(
                        "Combien d'heures par jour étudie-t-il/elle ?", 0.0, 16.0,
                        value=st.session_state.form_data.get(field_key, 4.0),
                        step=0.5, key=f"{field_key}_{current_step_index}"
                    )
                elif field_key == "sleep":
                    st.session_state.form_data[field_key] = st.slider(
                        "Combien d'heures dort le patient par nuit ?", 0.0, 12.0,
                        value=st.session_state.form_data.get(field_key, 7.0),
                        step=0.5, key=f"{field_key}_{current_step_index}"
                    )
                elif field_key == "social":
                    st.session_state.form_data[field_key] = st.slider(
                        "Temps passé sur les réseaux sociaux (h/jour) ?", 0.0, 16.0,
                        value=st.session_state.form_data.get(field_key, 3.0),
                        step=0.5, key=f"{field_key}_{current_step_index}"
                    )
                elif field_key == "physical":
                    st.session_state.form_data[field_key] = st.slider(
                        "Activité physique hebdomadaire du patient (min/semaine) ?", 0, 500,
                        value=st.session_state.form_data.get(field_key, 120),
                        step=10, key=f"{field_key}_{current_step_index}"
                    )
                elif field_key == "stress":
                    st.session_state.form_data[field_key] = st.slider(
                        "Niveau de stress ressenti par le patient (1-10) ?", 1, 10,
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

        # Add section title for review step
        st.markdown('<div class="section-title">✅ Récapitulatif du Patient</div>', unsafe_allow_html=True)

        fd = st.session_state.form_data

        # Convert CGPA back to /20 scale for display
        cgpa_value = fd.get('cgpa', 'Non renseigné')
        if cgpa_value != 'Non renseigné':
            cgpa_display = f"{cgpa_value * 5.0:.1f} / 20"
        else:
            cgpa_display = 'Non renseigné'

        st.markdown(f"""
        <div class="review-section">
            <h4>👤 Informations du Patient</h4>
            <div class="review-item"><span>Genre :</span> {fd.get('gender', 'Non renseigné')}</div>
            <div class="review-item"><span>Âge :</span> {fd.get('age', 'Non renseigné')} ans</div>
            <div class="review-item"><span>Département :</span> {fd.get('department', 'Non renseigné')}</div>
        </div>
        <div class="review-section">
            <h4>📚 Parcours Académique</h4>
            <div class="review-item"><span>Moyenne générale :</span> {cgpa_display}</div>
            <div class="review-item"><span>Heures d'étude / jour :</span> {fd.get('study', 'Non renseigné')}h</div>
        </div>
        <div class="review-section">
            <h4>💪 Mode de Vie</h4>
            <div class="review-item"><span>Sommeil :</span> {fd.get('sleep', 'Non renseigné')}h / nuit</div>
            <div class="review-item"><span>Réseaux sociaux :</span> {fd.get('social', 'Non renseigné')}h / jour</div>
            <div class="review-item"><span>Activité physique :</span> {fd.get('physical', 'Non renseigné')} min / semaine</div>
            <div class="review-item"><span>Stress :</span> {fd.get('stress', 'Non renseigné')} / 10</div>
        </div>
        """, unsafe_allow_html=True)


        col_nav1, col_nav2 = st.columns(2)
        with col_nav1:
            if st.button("⬅️ Précédent", key="review_prev", use_container_width=True):
                prev_step()
        with col_nav2:
            if st.button("🔮 Lancer l'Analyse", key="get_prediction", use_container_width=True):
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
                with st.spinner("🔄 Analyse du profil du patient..."):
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
            <strong>ℹ️ Note :</strong> Cet outil d'aide au diagnostic repose sur un modèle de Machine Learning.
            Il ne se substitue pas au jugement clinique du praticien. Les données sont traitées localement.
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
            <div class="result-title">Risque de Dépression Détecté</div>
            <div class="result-desc">
                Le modèle indique un risque potentiel de dépression pour ce patient.
                Une évaluation clinique approfondie est recommandée.
            </div>
        </div>
        """, unsafe_allow_html=True)

        # Recommendations for at-risk patients
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.markdown('<div class="section-title">📋 Prescriptions Recommandées</div>', unsafe_allow_html=True)
        st.markdown("""
        Voici les recommandations à transmettre au patient pour améliorer son bien-être :

        - **🎬 Faire un marathon Le Seigneur des Anneaux** - Thérapie cinématographique immersive (durée : 11h34 version longue)
        - **🍰 Manger des pâtisseries** - Augmentation du taux de sérotonine par voie gustative
        - **🥾 Randonner** - Sylvothérapie et reconnexion avec la nature
        - **🤘 Pogoter** - Libération d'endorphines par expression corporelle intensive
        - **✊ Détruire le capitalisme** - Traitement de fond pour éradiquer la cause structurelle du mal-être
        """)
        st.markdown('</div>', unsafe_allow_html=True)

    else:
        st.markdown(f"""
        <div class="result-card result-negative">
            <div class="result-icon">✅</div>
            <div class="result-title">Pas de Risque Significatif</div>
            <div class="result-desc">
                Le modèle n'indique pas de risque significatif de dépression pour ce patient.
                Le patient semble maintenir un bon équilibre de vie.
            </div>
        </div>
        """, unsafe_allow_html=True)

    # Feedback section
    st.markdown('<div class="feedback-box">', unsafe_allow_html=True)
    st.markdown('<div class="feedback-title">📊 Retour Clinique</div>', unsafe_allow_html=True)
    st.markdown("Votre diagnostic clinique permet d'améliorer la précision du modèle.")

    feedback_col1, feedback_col2 = st.columns([3, 1])

    with feedback_col1:
        actual_status = st.selectbox(
            "Le patient présente-t-il effectivement des symptômes de dépression ?",
            ["Non", "Oui"],
            key="feedback_actual"
        )

    with feedback_col2:
        st.write("")  # Spacing
        st.write("")
        if st.button("Envoyer le Diagnostic", use_container_width=True):
            feedback_payload = {
                "features": form_data,
                "prediction": int(prediction),
                "actual": 1 if actual_status == "Oui" else 0,
            }

            try:
                fb_response = requests.post(FEEDBACK_URL, json=feedback_payload, timeout=10)
                if fb_response.status_code == 200:
                    result = fb_response.json()
                    st.success(f"✅ Diagnostic enregistré (total: {result.get('total_feedbacks', 0)})")
                    if result.get("retrain_triggered"):
                        st.info("🔄 Ré-entraînement du modèle déclenché !")
                else:
                    st.error(f"❌ Erreur: {fb_response.status_code}")
            except Exception as e:
                st.error(f"❌ Erreur de connexion: {e}")

    st.markdown('</div>', unsafe_allow_html=True)

    # New assessment button
    st.markdown('<div style="margin-top: 2rem;"></div>', unsafe_allow_html=True)
    if st.button("🔄 Nouveau Patient", use_container_width=True):
        st.session_state.step = "form"
        st.session_state.form_step = 0  # Reset to first step
        st.session_state.prediction = None
        st.session_state.form_data = {}
        st.session_state.api_payload = {}
        st.rerun()

# ---------------------------------------------------------------------------
# Footer
# ---------------------------------------------------------------------------
st.markdown("""
<div class="footer">
    <strong>MindPulse</strong> &mdash; Outil d'Aide au Diagnostic<br>
    M1 DataEng &middot; Ynov Campus &middot; 2025-2026
</div>
""", unsafe_allow_html=True)
