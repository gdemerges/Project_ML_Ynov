import streamlit as st
import requests
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import numpy as np

# ---------------------------------------------------------------------------
# Page config
# ---------------------------------------------------------------------------
st.set_page_config(
    page_title="MindPulse - Student Depression Analytics",
    page_icon="◉",
    layout="wide",
    initial_sidebar_state="expanded",
)

API_URL = "http://serving-api:8080/predict"
FEEDBACK_URL = "http://serving-api:8080/feedback"

# ---------------------------------------------------------------------------
# Custom CSS – dark analytics dashboard aesthetic
# ---------------------------------------------------------------------------
st.markdown("""
<style>
    /* ---------- global ---------- */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

    .stApp {
        background: linear-gradient(135deg, #0f0f1a 0%, #1a1a2e 50%, #16213e 100%);
        font-family: 'Inter', sans-serif;
    }

    /* hide default streamlit chrome */
    #MainMenu, footer, header {visibility: hidden;}
    .block-container {padding-top: 1rem; padding-bottom: 1rem;}

    /* ---------- typography ---------- */
    h1, h2, h3, .stMarkdown h1, .stMarkdown h2, .stMarkdown h3 {
        color: #e2e8f0 !important;
        font-weight: 600 !important;
        letter-spacing: -0.02em;
    }
    p, span, label, .stMarkdown p {
        color: #94a3b8 !important;
    }

    /* ---------- sidebar ---------- */
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0d1117 0%, #161b22 100%) !important;
        border-right: 1px solid rgba(99, 102, 241, 0.15);
    }
    section[data-testid="stSidebar"] h1,
    section[data-testid="stSidebar"] h2,
    section[data-testid="stSidebar"] h3 {
        color: #c4b5fd !important;
    }
    section[data-testid="stSidebar"] p,
    section[data-testid="stSidebar"] span,
    section[data-testid="stSidebar"] label {
        color: #8b949e !important;
    }

    /* ---------- glass cards ---------- */
    .glass-card {
        background: rgba(255, 255, 255, 0.03);
        border: 1px solid rgba(99, 102, 241, 0.12);
        border-radius: 16px;
        padding: 1.5rem;
        backdrop-filter: blur(12px);
        margin-bottom: 1rem;
        transition: border-color 0.3s ease, box-shadow 0.3s ease;
    }
    .glass-card:hover {
        border-color: rgba(99, 102, 241, 0.35);
        box-shadow: 0 0 30px rgba(99, 102, 241, 0.08);
    }

    /* ---------- hero header ---------- */
    .hero {
        text-align: center;
        padding: 2rem 0 1.5rem;
    }
    .hero-title {
        font-size: 2.4rem;
        font-weight: 700;
        background: linear-gradient(135deg, #818cf8 0%, #c084fc 50%, #f472b6 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        letter-spacing: -0.03em;
        margin-bottom: 0.3rem;
    }
    .hero-sub {
        color: #64748b !important;
        font-size: 1rem;
        font-weight: 400;
    }

    /* ---------- section headers ---------- */
    .section-label {
        font-size: 0.7rem;
        font-weight: 600;
        letter-spacing: 0.12em;
        text-transform: uppercase;
        color: #818cf8 !important;
        margin-bottom: 0.8rem;
    }
    .section-title {
        font-size: 1.15rem;
        font-weight: 600;
        color: #e2e8f0 !important;
        margin-bottom: 1rem;
    }

    /* ---------- metric cards ---------- */
    .metric-row {
        display: flex;
        gap: 1rem;
        margin-bottom: 1rem;
    }
    .metric-card {
        flex: 1;
        background: rgba(255,255,255,0.02);
        border: 1px solid rgba(99,102,241,0.1);
        border-radius: 12px;
        padding: 1.1rem 1.2rem;
        text-align: center;
    }
    .metric-value {
        font-size: 1.8rem;
        font-weight: 700;
        color: #818cf8 !important;
        line-height: 1.1;
    }
    .metric-label {
        font-size: 0.72rem;
        text-transform: uppercase;
        letter-spacing: 0.08em;
        color: #64748b !important;
        margin-top: 0.3rem;
    }

    /* ---------- result banner ---------- */
    .result-positive {
        background: linear-gradient(135deg, rgba(239,68,68,0.12) 0%, rgba(239,68,68,0.04) 100%);
        border: 1px solid rgba(239,68,68,0.3);
        border-radius: 16px;
        padding: 2rem;
        text-align: center;
    }
    .result-negative {
        background: linear-gradient(135deg, rgba(34,197,94,0.12) 0%, rgba(34,197,94,0.04) 100%);
        border: 1px solid rgba(34,197,94,0.3);
        border-radius: 16px;
        padding: 2rem;
        text-align: center;
    }
    .result-title {
        font-size: 1.6rem;
        font-weight: 700;
        margin-bottom: 0.5rem;
    }
    .result-positive .result-title { color: #f87171 !important; }
    .result-negative .result-title { color: #4ade80 !important; }
    .result-desc { color: #94a3b8 !important; font-size: 0.95rem; }

    /* ---------- inputs ---------- */
    .stSlider > div > div > div { color: #818cf8 !important; }
    .stSelectbox > div > div,
    .stTextInput > div > div > input,
    .stNumberInput > div > div > input {
        background: rgba(255,255,255,0.04) !important;
        border-color: rgba(99,102,241,0.2) !important;
        color: #e2e8f0 !important;
        border-radius: 10px !important;
    }

    /* ---------- buttons ---------- */
    .stButton > button[kind="primary"] {
        background: linear-gradient(135deg, #6366f1, #8b5cf6) !important;
        border: none !important;
        border-radius: 12px !important;
        padding: 0.75rem 2rem !important;
        font-weight: 600 !important;
        font-size: 1rem !important;
        letter-spacing: 0.02em;
        transition: all 0.3s ease !important;
    }
    .stButton > button[kind="primary"]:hover {
        box-shadow: 0 0 25px rgba(99,102,241,0.4) !important;
        transform: translateY(-1px);
    }
    .stButton > button[kind="secondary"] {
        background: rgba(255,255,255,0.05) !important;
        border: 1px solid rgba(99,102,241,0.25) !important;
        border-radius: 10px !important;
        color: #c4b5fd !important;
    }

    /* ---------- divider ---------- */
    .custom-divider {
        height: 1px;
        background: linear-gradient(90deg, transparent, rgba(99,102,241,0.3), transparent);
        margin: 1.5rem 0;
        border: none;
    }

    /* ---------- tabs ---------- */
    .stTabs [data-baseweb="tab-list"] {
        gap: 0;
        background: rgba(255,255,255,0.02);
        border-radius: 12px;
        padding: 4px;
        border: 1px solid rgba(99,102,241,0.1);
    }
    .stTabs [data-baseweb="tab"] {
        border-radius: 10px;
        color: #64748b;
        font-weight: 500;
        padding: 8px 20px;
    }
    .stTabs [aria-selected="true"] {
        background: rgba(99,102,241,0.15) !important;
        color: #c4b5fd !important;
    }

    /* ---------- plotly charts transparent bg ---------- */
    .js-plotly-plot .plotly .main-svg { background: transparent !important; }

    /* ---------- footer ---------- */
    .app-footer {
        text-align: center;
        padding: 1.5rem 0 0.5rem;
        color: #475569 !important;
        font-size: 0.78rem;
    }
    .app-footer a { color: #818cf8; text-decoration: none; }
</style>
""", unsafe_allow_html=True)


# ---------------------------------------------------------------------------
# Helper – radar chart for user profile
# ---------------------------------------------------------------------------
def make_radar(values: dict, color="#818cf8"):
    cats = list(values.keys())
    vals = list(values.values())
    vals += vals[:1]
    cats += cats[:1]

    fig = go.Figure()
    fig.add_trace(go.Scatterpolar(
        r=vals, theta=cats, fill="toself",
        fillcolor=f"rgba({','.join(str(int(color.lstrip('#')[i:i+2],16)) for i in (0,2,4))},0.15)",
        line=dict(color=color, width=2),
        marker=dict(size=5, color=color),
    ))
    fig.update_layout(
        polar=dict(
            bgcolor="rgba(0,0,0,0)",
            radialaxis=dict(visible=True, range=[0, 10], showticklabels=False,
                            gridcolor="rgba(99,102,241,0.08)"),
            angularaxis=dict(gridcolor="rgba(99,102,241,0.08)",
                             tickfont=dict(color="#94a3b8", size=11)),
        ),
        showlegend=False,
        margin=dict(l=60, r=60, t=30, b=30),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        height=320,
    )
    return fig


def make_gauge(value, title, max_val=10, color="#818cf8"):
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=value,
        title=dict(text=title, font=dict(size=13, color="#94a3b8")),
        number=dict(font=dict(size=28, color="#e2e8f0")),
        gauge=dict(
            axis=dict(range=[0, max_val], tickcolor="#334155",
                      tickfont=dict(color="#475569", size=10)),
            bar=dict(color=color, thickness=0.7),
            bgcolor="rgba(255,255,255,0.02)",
            borderwidth=0,
            steps=[
                dict(range=[0, max_val * 0.33], color="rgba(34,197,94,0.08)"),
                dict(range=[max_val * 0.33, max_val * 0.66], color="rgba(250,204,21,0.08)"),
                dict(range=[max_val * 0.66, max_val], color="rgba(239,68,68,0.08)"),
            ],
        ),
    ))
    fig.update_layout(
        height=180, margin=dict(l=20, r=20, t=40, b=10),
        paper_bgcolor="rgba(0,0,0,0)", font=dict(color="#e2e8f0"),
    )
    return fig


def make_bar_profile(data_dict):
    cats = list(data_dict.keys())
    vals = list(data_dict.values())
    colors = [f"rgba(129,140,248,{0.3 + 0.7 * v / 10})" for v in vals]

    fig = go.Figure(go.Bar(
        x=vals, y=cats, orientation="h",
        marker=dict(color=colors, line=dict(width=0)),
        text=[f"{v}/10" for v in vals],
        textposition="auto",
        textfont=dict(color="#e2e8f0", size=12),
    ))
    fig.update_layout(
        xaxis=dict(range=[0, 10.5], showgrid=False, showticklabels=False, zeroline=False),
        yaxis=dict(tickfont=dict(color="#94a3b8", size=12), autorange="reversed"),
        margin=dict(l=0, r=20, t=10, b=10),
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        height=250,
    )
    return fig


# ---------------------------------------------------------------------------
# Hero
# ---------------------------------------------------------------------------
st.markdown("""
<div class="hero">
    <div class="hero-title">MindPulse Analytics</div>
    <div class="hero-sub">Student Depression Risk Prediction &mdash; Powered by Machine Learning</div>
</div>
""", unsafe_allow_html=True)

st.markdown('<div class="custom-divider"></div>', unsafe_allow_html=True)

# ---------------------------------------------------------------------------
# Sidebar – input form (matching ML model features)
# ---------------------------------------------------------------------------
with st.sidebar:
    st.markdown('<p class="section-label">Configuration</p>', unsafe_allow_html=True)
    st.markdown('<p class="section-title">Student Profile</p>', unsafe_allow_html=True)

    # ---- Demographics ----
    st.markdown('<p class="section-label" style="margin-top:1rem;">Demographics</p>', unsafe_allow_html=True)

    gender = st.selectbox("Gender", ["Male", "Female"], index=0)
    age = st.number_input("Age", min_value=16, max_value=60, value=22)
    department = st.selectbox("Department", ["Science", "Engineering", "Medical", "Arts", "Business"])

    # ---- Academic ----
    st.markdown('<p class="section-label" style="margin-top:1.2rem;">Academic Performance</p>', unsafe_allow_html=True)

    cgpa = st.slider("CGPA", 0.0, 4.0, 3.0, 0.01)
    study_hours = st.slider("Study Hours (per day)", 0.0, 16.0, 4.0, 0.1)

    # ---- Lifestyle ----
    st.markdown('<p class="section-label" style="margin-top:1.2rem;">Lifestyle Factors</p>', unsafe_allow_html=True)

    sleep_duration = st.slider("Sleep Duration (hours/day)", 0.0, 12.0, 7.0, 0.1)
    social_media_hours = st.slider("Social Media (hours/day)", 0.0, 16.0, 3.0, 0.1)
    physical_activity = st.slider("Physical Activity (minutes/week)", 0, 500, 120, 5)

    # ---- Mental Health ----
    st.markdown('<p class="section-label" style="margin-top:1.2rem;">Mental Health</p>', unsafe_allow_html=True)

    stress_level = st.slider("Stress Level", 1, 10, 5)

    st.markdown('<div class="custom-divider"></div>', unsafe_allow_html=True)

    predict_clicked = st.button("Run Analysis", type="primary", use_container_width=True)

# ---------------------------------------------------------------------------
# Assemble data payload (matching ML model schema)
# ---------------------------------------------------------------------------
data = {
    "Student_ID": 9999,  # Placeholder, not used for prediction
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

# Profile scores for visualization
profile_scores = {
    "CGPA": cgpa / 4 * 10,  # Normalize to 0-10 scale
    "Sleep": sleep_duration / 12 * 10,
    "Study": study_hours / 16 * 10,
    "Social Media": social_media_hours / 16 * 10,
    "Physical Activity": physical_activity / 500 * 10,
    "Stress": stress_level,
}

# ---------------------------------------------------------------------------
# Main dashboard – always-visible profile overview
# ---------------------------------------------------------------------------
st.markdown('<p class="section-label">Overview</p>', unsafe_allow_html=True)
st.markdown('<p class="section-title">Student Risk Profile</p>', unsafe_allow_html=True)

# --- Metric cards row ---
st.markdown(f"""
<div class="metric-row">
    <div class="metric-card">
        <div class="metric-value">{age}</div>
        <div class="metric-label">Age</div>
    </div>
    <div class="metric-card">
        <div class="metric-value">{cgpa:.2f}</div>
        <div class="metric-label">CGPA</div>
    </div>
    <div class="metric-card">
        <div class="metric-value">{sleep_duration:.1f}h</div>
        <div class="metric-label">Sleep</div>
    </div>
    <div class="metric-card">
        <div class="metric-value">{study_hours:.1f}h</div>
        <div class="metric-label">Study</div>
    </div>
    <div class="metric-card">
        <div class="metric-value">{stress_level}/10</div>
        <div class="metric-label">Stress</div>
    </div>
</div>
""", unsafe_allow_html=True)

# --- Charts row ---
col_radar, col_bar = st.columns([1, 1])

with col_radar:
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.markdown('<p class="section-label">Student Profile Radar</p>', unsafe_allow_html=True)
    st.plotly_chart(make_radar(profile_scores), use_container_width=True, config={"displayModeBar": False})
    st.markdown('</div>', unsafe_allow_html=True)

with col_bar:
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.markdown('<p class="section-label">Factor Breakdown</p>', unsafe_allow_html=True)
    st.plotly_chart(make_bar_profile(profile_scores), use_container_width=True, config={"displayModeBar": False})
    st.markdown('</div>', unsafe_allow_html=True)

# --- Gauge row ---
g1, g2, g3 = st.columns(3)
with g1:
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.plotly_chart(make_gauge(stress_level, "Stress Level", color="#f472b6"),
                    use_container_width=True, config={"displayModeBar": False})
    st.markdown('</div>', unsafe_allow_html=True)
with g2:
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    academic_score = round((cgpa / 4 * 5) + (study_hours / 16 * 5), 1)
    st.plotly_chart(make_gauge(academic_score, "Academic Score", color="#34d399"),
                    use_container_width=True, config={"displayModeBar": False})
    st.markdown('</div>', unsafe_allow_html=True)
with g3:
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    lifestyle_score = round((sleep_duration / 8 * 5) + (physical_activity / 500 * 5), 1)
    st.plotly_chart(make_gauge(lifestyle_score, "Lifestyle Score", color="#818cf8"),
                    use_container_width=True, config={"displayModeBar": False})
    st.markdown('</div>', unsafe_allow_html=True)

st.markdown('<div class="custom-divider"></div>', unsafe_allow_html=True)

# ---------------------------------------------------------------------------
# Prediction section
# ---------------------------------------------------------------------------
if predict_clicked:
    st.markdown('<p class="section-label">Analysis</p>', unsafe_allow_html=True)
    st.markdown('<p class="section-title">Prediction Result</p>', unsafe_allow_html=True)

    with st.spinner("Running model inference..."):
        try:
            response = requests.post(API_URL, json=data, timeout=10)

            if response.status_code == 200:
                result = response.json()
                prediction = result.get("prediction", "Unknown")
                confidence = result.get("confidence", None)

                st.session_state["last_prediction"] = prediction
                st.session_state["last_data"] = data

                is_at_risk = prediction in ("Yes", 1, True)

                if is_at_risk:
                    st.markdown(f"""
                    <div class="result-positive">
                        <div class="result-title">Depression Risk Detected</div>
                        <div class="result-desc">
                            The model indicates a potential risk of depression based on the provided factors.
                            {f'<br><strong style="color:#f87171;">Confidence: {confidence:.0%}</strong>' if confidence else ''}
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    st.markdown(f"""
                    <div class="result-negative">
                        <div class="result-title">No Depression Risk Detected</div>
                        <div class="result-desc">
                            Based on the provided factors, the model does not indicate significant depression risk.
                            {f'<br><strong style="color:#4ade80;">Confidence: {confidence:.0%}</strong>' if confidence else ''}
                        </div>
                    </div>
                    """, unsafe_allow_html=True)

                # Recommendations
                st.markdown("")
                rec_col1, rec_col2 = st.columns(2)
                with rec_col1:
                    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
                    st.markdown('<p class="section-label">Recommendations</p>', unsafe_allow_html=True)
                    if is_at_risk:
                        recommendations = ["- Consult a mental health professional", "- Reach out to your university's counseling services"]
                        if stress_level >= 7:
                            recommendations.append("- Practice stress management techniques (meditation, breathing exercises)")
                        if sleep_duration < 6:
                            recommendations.append("- Prioritize getting 7-9 hours of sleep per night")
                        if physical_activity < 60:
                            recommendations.append("- Increase physical activity (aim for 150+ min/week)")
                        if social_media_hours > 5:
                            recommendations.append("- Reduce social media usage and connect in person")
                        st.markdown("\n".join(recommendations))
                    else:
                        recommendations = ["- Maintain your current healthy habits"]
                        if sleep_duration >= 7:
                            recommendations.append("- Continue your good sleep schedule")
                        if physical_activity >= 120:
                            recommendations.append("- Keep up your physical activity routine")
                        if stress_level <= 4:
                            recommendations.append("- Your stress management strategies are working well")
                        recommendations.append("- Stay connected with friends & family")
                        st.markdown("\n".join(recommendations))
                    st.markdown('</div>', unsafe_allow_html=True)

                with rec_col2:
                    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
                    st.markdown('<p class="section-label">Helplines (FR)</p>', unsafe_allow_html=True)
                    st.markdown("""
                    | Service | Number |
                    |---------|--------|
                    | **3114** | National prevention |
                    | **SOS Amitie** | 09 72 39 40 50 |
                    | **Fil Sante Jeunes** | 0 800 235 236 |
                    """)
                    st.markdown('</div>', unsafe_allow_html=True)

                # --- Feedback ---
                st.markdown('<div class="custom-divider"></div>', unsafe_allow_html=True)
                st.markdown('<p class="section-label">Feedback Loop</p>', unsafe_allow_html=True)

                with st.expander("Help improve the model — provide your real status"):
                    fc1, fc2 = st.columns([3, 1])
                    with fc1:
                        actual_value = st.selectbox(
                            "Are you actually experiencing depression?",
                            ["No", "Yes"], key="feedback_actual"
                        )
                    with fc2:
                        st.write("")
                        st.write("")
                        if st.button("Submit feedback", type="secondary", use_container_width=True):
                            feedback_data = {
                                **data,
                                "prediction": prediction,
                                "actual": actual_value,
                            }
                            try:
                                fb = requests.post(FEEDBACK_URL, json=feedback_data, timeout=10)
                                if fb.status_code == 200:
                                    st.success("Feedback submitted — thank you!")
                                else:
                                    st.error(f"Server returned status {fb.status_code}")
                            except Exception as e:
                                st.error(f"Connection error: {e}")

            else:
                st.error(f"API returned status {response.status_code}: {response.text}")

        except requests.exceptions.ConnectionError:
            st.error("Cannot reach the prediction API. Make sure the serving container is running.")
        except requests.exceptions.Timeout:
            st.error("Request timed out. The server may be overloaded.")
        except Exception as e:
            st.error(f"Unexpected error: {e}")

else:
    # Prompt to run
    st.markdown("""
    <div class="glass-card" style="text-align:center; padding:2.5rem;">
        <p style="font-size:1.1rem; color:#64748b !important; margin:0;">
            Configure the student profile in the sidebar, then click
            <strong style="color:#818cf8;">Run Analysis</strong> to get a prediction.
        </p>
    </div>
    """, unsafe_allow_html=True)

# ---------------------------------------------------------------------------
# Footer
# ---------------------------------------------------------------------------
st.markdown('<div class="custom-divider"></div>', unsafe_allow_html=True)
st.markdown("""
<div class="app-footer">
    <strong style="color:#64748b;">MindPulse Analytics</strong> &mdash;
    Educational project only. Not a substitute for professional medical advice.<br>
    M1 DataEng &middot; Ynov Campus &middot; 2025-2026
</div>
""", unsafe_allow_html=True)
