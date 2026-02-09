import streamlit as st
import requests

# ---------------------------------------------------------------------------
# Config
# ---------------------------------------------------------------------------
st.set_page_config(
    page_title="MindPulse - Student Depression Risk",
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
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        font-family: 'Inter', sans-serif;
    }

    /* Hide Streamlit branding */
    #MainMenu, footer, header {visibility: hidden;}
    .block-container {padding: 2rem 1rem;}

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
        background: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(20px);
        border-radius: 24px;
        padding: 2.5rem;
        border: 1px solid rgba(255, 255, 255, 0.18);
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
        margin-bottom: 2rem;
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
        background: white !important;
        color: #667eea !important;
        border: none !important;
        border-radius: 16px !important;
        padding: 1rem 2rem !important;
        font-size: 1.1rem !important;
        font-weight: 600 !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 4px 15px rgba(0,0,0,0.2) !important;
    }

    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 25px rgba(0,0,0,0.3) !important;
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
</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------------------------
# Header
# ---------------------------------------------------------------------------
st.markdown("""
<div class="hero">
    <div class="hero-icon">🧠</div>
    <div class="hero-title">MindPulse</div>
    <div class="hero-subtitle">Student Mental Health Risk Assessment</div>
</div>
""", unsafe_allow_html=True)

# ---------------------------------------------------------------------------
# Initialize session state
# ---------------------------------------------------------------------------
if "step" not in st.session_state:
    st.session_state.step = "form"  # form | result
if "prediction" not in st.session_state:
    st.session_state.prediction = None
if "form_data" not in st.session_state:
    st.session_state.form_data = {}

# ---------------------------------------------------------------------------
# STEP 1: Form
# ---------------------------------------------------------------------------
if st.session_state.step == "form":
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">📋 Student Profile</div>', unsafe_allow_html=True)

    with st.form("student_form"):
        col1, col2 = st.columns(2)

        with col1:
            st.markdown("**👤 Demographics**")
            gender = st.selectbox("Gender", ["Male", "Female"], key="gender")
            age = st.number_input("Age", min_value=16, max_value=60, value=22, key="age")
            department = st.selectbox(
                "Department",
                ["Science", "Engineering", "Medical", "Arts", "Business"],
                key="department"
            )

        with col2:
            st.markdown("**📚 Academic**")
            cgpa = st.number_input("CGPA", min_value=0.0, max_value=4.0, value=3.0, step=0.1, key="cgpa")
            study_hours = st.number_input(
                "Study Hours (per day)",
                min_value=0.0, max_value=16.0, value=4.0, step=0.5, key="study"
            )

        st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

        st.markdown("**🏃 Lifestyle Factors**")
        col3, col4 = st.columns(2)

        with col3:
            sleep_duration = st.slider(
                "Sleep Duration (hours/day)",
                0.0, 12.0, 7.0, 0.5, key="sleep"
            )
            social_media_hours = st.slider(
                "Social Media (hours/day)",
                0.0, 16.0, 3.0, 0.5, key="social"
            )

        with col4:
            physical_activity = st.slider(
                "Physical Activity (min/week)",
                0, 500, 120, 10, key="physical"
            )
            stress_level = st.slider(
                "Stress Level (1-10)",
                1, 10, 5, 1, key="stress"
            )

        st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

        submitted = st.form_submit_button("🔮 Get Prediction", use_container_width=True)

        if submitted:
            # Prepare data
            form_data = {
                "Age": age,
                "Gender": gender,
                "Department": department,
                "CGPA": cgpa,
                "Sleep_Duration": sleep_duration,
                "Study_Hours": study_hours,
                "Social_Media_Hours": social_media_hours,
                "Physical_Activity": physical_activity,
                "Stress_Level": stress_level,
            }

            # Call API
            with st.spinner("🔄 Analyzing your profile..."):
                try:
                    response = requests.post(
                        API_URL,
                        json={"features": form_data},
                        timeout=10
                    )

                    if response.status_code == 200:
                        result = response.json()
                        prediction = result.get("prediction", 0)

                        # Save to session
                        st.session_state.prediction = prediction
                        st.session_state.form_data = form_data
                        st.session_state.step = "result"
                        st.rerun()
                    else:
                        st.error(f"❌ API Error: {response.status_code} - {response.text}")

                except requests.exceptions.ConnectionError:
                    st.error("❌ Cannot reach the API. Please ensure the serving container is running.")
                except Exception as e:
                    st.error(f"❌ Unexpected error: {e}")

    st.markdown('</div>', unsafe_allow_html=True)

    # Info box
    st.markdown("""
    <div class="info-box">
        <p>
            <strong>ℹ️ Privacy Notice:</strong> This is an educational ML model for demonstration purposes.
            Not a substitute for professional medical advice. All data is processed locally.
        </p>
    </div>
    """, unsafe_allow_html=True)

# ---------------------------------------------------------------------------
# STEP 2: Result
# ---------------------------------------------------------------------------
elif st.session_state.step == "result":
    prediction = st.session_state.prediction
    form_data = st.session_state.form_data

    is_at_risk = prediction == 1

    # Result card
    if is_at_risk:
        st.markdown(f"""
        <div class="result-card result-positive">
            <div class="result-icon">⚠️</div>
            <div class="result-title">Risk Detected</div>
            <div class="result-desc">
                The model indicates a potential risk of depression based on your profile.
                We recommend reaching out to mental health support services.
            </div>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div class="result-card result-negative">
            <div class="result-icon">✅</div>
            <div class="result-title">No Significant Risk</div>
            <div class="result-desc">
                Based on your profile, the model does not indicate significant depression risk.
                Continue maintaining your healthy lifestyle habits.
            </div>
        </div>
        """, unsafe_allow_html=True)

    # Recommendations
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">💡 Recommendations</div>', unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("**📞 Support Resources (France)**")
        st.markdown("""
        - **3114** - National prevention hotline
        - **SOS Amitié** - 09 72 39 40 50
        - **Fil Santé Jeunes** - 0 800 235 236
        - **Nightline** - Student listening service
        """)

    with col2:
        st.markdown("**🎯 Personalized Tips**")
        tips = []

        if form_data["Stress_Level"] >= 7:
            tips.append("- Practice stress management (meditation, breathing)")
        if form_data["Sleep_Duration"] < 6:
            tips.append("- Aim for 7-9 hours of sleep per night")
        if form_data["Physical_Activity"] < 60:
            tips.append("- Increase physical activity (150+ min/week)")
        if form_data["Social_Media_Hours"] > 5:
            tips.append("- Reduce screen time and social media")
        if form_data["Study_Hours"] > 10:
            tips.append("- Balance study time with breaks")

        if not tips:
            tips = [
                "- Keep up your healthy habits",
                "- Stay connected with friends & family",
                "- Maintain work-life balance"
            ]

        st.markdown("\n".join(tips))

    st.markdown('</div>', unsafe_allow_html=True)

    # Feedback section
    st.markdown('<div class="feedback-box">', unsafe_allow_html=True)
    st.markdown('<div class="feedback-title">📊 Help Improve Our Model</div>', unsafe_allow_html=True)
    st.markdown("Your feedback helps train the model to become more accurate over time.")

    feedback_col1, feedback_col2 = st.columns([3, 1])

    with feedback_col1:
        actual_status = st.selectbox(
            "Are you actually experiencing depression symptoms?",
            ["No", "Yes"],
            key="feedback_actual"
        )

    with feedback_col2:
        st.write("")  # Spacing
        st.write("")
        if st.button("Submit Feedback", use_container_width=True):
            feedback_payload = {
                "features": form_data,
                "prediction": int(prediction),
                "actual": 1 if actual_status == "Yes" else 0,
            }

            try:
                fb_response = requests.post(FEEDBACK_URL, json=feedback_payload, timeout=10)
                if fb_response.status_code == 200:
                    result = fb_response.json()
                    st.success(f"✅ Thank you! Feedback saved (total: {result.get('total_feedbacks', 0)})")
                    if result.get("retrain_triggered"):
                        st.info("🔄 Model retraining triggered!")
                else:
                    st.error(f"❌ Error: {fb_response.status_code}")
            except Exception as e:
                st.error(f"❌ Connection error: {e}")

    st.markdown('</div>', unsafe_allow_html=True)

    # New assessment button
    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
    if st.button("🔄 New Assessment", use_container_width=True):
        st.session_state.step = "form"
        st.session_state.prediction = None
        st.session_state.form_data = {}
        st.rerun()

# ---------------------------------------------------------------------------
# Footer
# ---------------------------------------------------------------------------
st.markdown("""
<div class="footer">
    <strong>MindPulse</strong> &mdash; Educational ML Project<br>
    M1 DataEng &middot; Ynov Campus &middot; 2025-2026
</div>
""", unsafe_allow_html=True)
