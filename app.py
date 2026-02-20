import streamlit as st
import google.generativeai as genai

# ----------------------------
# PAGE CONFIG
# ----------------------------
st.set_page_config(
    page_title="Legal Document Explainer Bot",
    page_icon="⚖️",
    layout="wide"
)

# ----------------------------
# CUSTOM STYLES
# ----------------------------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

.stApp {
    background: linear-gradient(135deg, #141E30, #243B55);
    color: white;
}

.block-container {
    padding-top: 2rem;
}

.card {
    background: rgba(255,255,255,0.05);
    padding: 20px;
    border-radius: 15px;
    backdrop-filter: blur(10px);
    margin-bottom: 20px;
}

button {
    border-radius: 10px !important;
    transition: all 0.3s ease-in-out !important;
}

button:hover {
    transform: scale(1.05);
    box-shadow: 0px 0px 15px #00c6ff;
}

.fade-in {
    animation: fadeIn 1s ease-in;
}

@keyframes fadeIn {
    from {opacity: 0;}
    to {opacity: 1;}
}
</style>
""", unsafe_allow_html=True)

# ----------------------------
# LOAD GEMINI
# ----------------------------
try:
    GEMINI_API_KEY = st.secrets["GEMINI_API_KEY"]
except:
    st.error("Please add GEMINI_API_KEY in Streamlit Cloud → Settings → Secrets")
    st.stop()

genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel("models/gemini-2.5-flash")

# ----------------------------
# HEADER
# ----------------------------
st.markdown("<h1 class='fade-in'>⚖️ Legal Document Explainer Bot</h1>", unsafe_allow_html=True)
st.markdown("Simplify complex legal documents into easy-to-understand summaries.")

# ----------------------------
# INPUT SECTION
# ----------------------------
col1, col2 = st.columns([1, 1.4])

with col1:
    st.markdown("<div class='card'>", unsafe_allow_html=True)

    uploaded_file = st.file_uploader("Upload Legal Document (TXT only)", type=["txt"])

    legal_text = st.text_area("Or Paste Legal Text Here", height=250)

    level = st.selectbox(
        "Explanation Level",
        ["Layman", "Teenager", "Business Owner"]
    )

    length = st.selectbox(
        "Summary Length",
        ["Short", "Medium", "Detailed"]
    )

    highlight_risks = st.checkbox("Highlight Legal Risks")
    clause_breakdown = st.checkbox("Clause-by-Clause Explanation")

    generate_btn = st.button("📜 Simplify Document")

    st.markdown("</div>", unsafe_allow_html=True)

# ----------------------------
# GENERATION
# ----------------------------
if generate_btn:

    if uploaded_file:
        legal_text = uploaded_file.read().decode("utf-8")

    if not legal_text:
        st.warning("Please upload or paste a legal document.")
        st.stop()

    with st.spinner("Analyzing legal document..."):

        prompt = f"""
You are a legal simplification expert.

Rewrite the following legal document for a {level}.

Text:
{legal_text}

Length: {length}
Highlight Risks: {highlight_risks}
Clause Breakdown: {clause_breakdown}

Structure EXACTLY like this:

ONE-LINE SUMMARY:

PLAIN ENGLISH SUMMARY:

KEY OBLIGATIONS:

IMPORTANT DATES:

LEGAL RISKS:
(Only if enabled)

CLAUSE BREAKDOWN:
(Only if enabled)

FINAL QUICK RECAP:
"""

        response = model.generate_content(prompt)
        simplified = response.text

    with col2:
        st.markdown("<div class='card fade-in'>", unsafe_allow_html=True)

        st.subheader("📘 Simplified Legal Explanation")
        st.markdown(simplified)

        difficulty_score = min(len(legal_text) // 25, 100)
        st.progress(difficulty_score)
        st.caption(f"Estimated Original Complexity Score: {difficulty_score}/100")

        st.download_button(
            "⬇ Download Simplified Version",
            simplified,
            file_name="legal_summary.txt",
            mime="text/plain"
        )

        if st.button("🔄 Regenerate"):
            st.rerun()

        st.markdown("</div>", unsafe_allow_html=True)

# ----------------------------
# FOOTER
# ----------------------------
if legal_text:
    st.caption(f"Character Count: {len(legal_text)}")