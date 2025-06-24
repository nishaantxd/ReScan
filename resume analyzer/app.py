import streamlit as st
from extractor import extract_text_from_pdf_or_image, extract_resume_info
from comparator import compare_resume_with_jd
import matplotlib.pyplot as plt

st.set_page_config(layout="wide")

# ----------------- SESSION STATE FOR THEME ------------------
if "theme_mode" not in st.session_state:
    st.session_state["theme_mode"] = "dark"

# ----------------- THEME TOGGLE BUTTON ------------------
if "theme_mode" not in st.session_state:
    st.session_state.theme_mode = "dark"

def toggle_theme():
    st.session_state.theme_mode = "light" if st.session_state.theme_mode == "dark" else "dark"

st.button("🌞" if st.session_state.theme_mode == "dark" else "🌙", on_click=toggle_theme)


# ----------------- CUSTOM STYLING ------------------
theme = st.session_state["theme_mode"]
bg_gradient = {
    "light": "linear-gradient(135deg, #b8d8f8, #e2c9f7)",
    "dark": "linear-gradient(135deg, #2e3a5e, #4a3d61)"
}[theme]

text_color = "#000" if theme == "light" else "#fff"

st.markdown(f"""
    <style>
    html, body, .stApp {{
        background: {bg_gradient};
        background-attachment: fixed;
        color: {text_color};
        font-family: 'Segoe UI', sans-serif;
        animation: fadeIn 0.6s ease-in-out;
    }}
    @keyframes fadeIn {{
        0% {{opacity: 0; transform: translateY(10px);}}
        100% {{opacity: 1; transform: translateY(0);}}
    }}

    .block-container {{
        max-width: 850px;
        margin: auto;
        padding: 2rem 2.5rem;
        background: rgba(255,255,255,0.07);
        border-radius: 20px;
        backdrop-filter: blur(16px);
        box-shadow: 0 0 20px rgba(0,0,0,0.3);
    }}

    h1, h2, h3, h4, h5, .stTitle {{
        color: {text_color} !important;
        text-align: center;
    }}

    textarea {{
        color: black !important;
        background: white !important;
    }}

    .stTextArea, .stFileUploader {{
        transition: all 0.3s ease-in-out;
        border-radius: 20px;
    }}

    .stFileUploader {{
        background: rgba(255, 255, 255, 0.15);
        padding: 1.2rem;
        border: 1px solid rgba(255,255,255,0.3);
        backdrop-filter: blur(14px);
        box-shadow: 0 0 12px rgba(130,180,255, 0.4);
    }}

    .stFileUploader:hover {{
        transform: scale(1.03);
        background: rgba(255, 255, 255, 0.3);
    }}

    .stButton > button {{
        background: rgba(255, 255, 255, 0.15);
        border: 1px solid rgba(255, 255, 255, 0.25);
        color: {text_color};
        padding: 0.6em 1.3em;
        font-size: 1rem;
        font-weight: 600;
        border-radius: 14px;
        backdrop-filter: blur(10px);
        box-shadow: 0 0 10px rgba(150, 100, 255, 0.6);
        transition: all 0.25s ease-in-out;
    }}

    .stButton > button:hover {{
        transform: scale(1.08);
        background: rgba(255, 255, 255, 0.25);
        color: black;
    }}

    .stButton > button:active {{
        transform: scale(0.9);
    }}

    /* Top right floating theme toggle button */
    div[data-testid="stToolbar"] {{
        display: flex;
        justify-content: flex-end;
    }}

    /* Pie chart size tweak */
    .element-container:has(canvas) {{
        display: flex;
        justify-content: center;
    }}
    </style>
""", unsafe_allow_html=True)

# ----------------- LOGO + TITLE ------------------
st.markdown(
    """
    <div style="display: flex; justify-content: center; align-items: center; margin-top: -20px; margin-bottom: -10px; margin-right: 22px">
        <img src="https://i.ibb.co/5XKqNLMf/notion-face.png" alt="Logo" style="height: 100px;">
    </div>
    """,
    unsafe_allow_html=True
)

st.markdown(f"<h1 style='margin-top:0; color:{text_color};'>ReScan</h1>", unsafe_allow_html=True)

# ----------------- INPUTS ------------------
uploaded_file = st.file_uploader("Upload your resume (PDF/Image)", type=["pdf", "png", "jpg", "jpeg"])
jd_input = st.text_area("Paste Job Description here 👇", height=200)

analyze = st.button("Analyze Resume")

# ----------------- LOGIC ------------------
if analyze and uploaded_file and jd_input:
    resume_text = extract_text_from_pdf_or_image(uploaded_file)
    resume_info = extract_resume_info(resume_text)
    results = compare_resume_with_jd(resume_info, jd_input)

    st.markdown("### 🧾 Extracted Resume Text")
    st.code(resume_text, language="markdown")

    st.markdown("### 📊 Resume vs JD Comparison")
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("🔍 Section-wise Matching Scores")
        for section, score in results["section_scores"].items():
            st.markdown(f"**{section.capitalize()}**: {score}%")

    with col2:
        st.subheader("🧮 Overall Match Score")
        st.metric(label="Match %", value=f"{results['overall_score']}%")

    st.markdown("### ⚠️ Missing Keywords from JD")
    if results["missing_keywords"]:
        st.write(", ".join(results["missing_keywords"]))
    else:
        st.success("No significant missing keywords!")

    st.markdown("### 📈 JD Keyword Match Overview")
    fig, ax = plt.subplots(figsize=(3, 3))
    ax.pie(
        [results['matched_count'], results['missing_count']],
        labels=['Matched', 'Missing'],
        colors=['#4CAF50', '#FF6F61'],
        autopct='%1.1f%%',
        startangle=140
    )
    ax.axis("equal")
    st.pyplot(fig)

elif analyze and not uploaded_file:
    st.warning("Please upload a resume to continue.")
elif analyze and not jd_input:
    st.warning("Paste a job description to analyze your resume.")
