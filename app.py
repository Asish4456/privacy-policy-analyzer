import streamlit as st
from analyzer import analyze_policy
from utils import (
    generate_short_explanations,
    extract_text_from_pdf,
    generate_report,
    highlight_risky_terms
)

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="Privacy Policy Analyzer",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# ---------------- GLOBAL STYLES ----------------
st.markdown("""
<style>
body {
    background-color: #0e1117;
}
.main-title {
    font-size: 40px;
    font-weight: 700;
    margin-bottom: 6px;
}
.subtitle {
    font-size: 16px;
    color: #9aa0a6;
    margin-bottom: 30px;
}
.card {
    background: #ffffff;
    padding: 22px;
    border-radius: 12px;
    border: 1px solid #e6e6e6;
    margin-bottom: 22px;
}
.section-title {
    font-size: 22px;
    font-weight: 600;
    margin: 30px 0 15px;
}
.badge {
    padding: 6px 14px;
    border-radius: 20px;
    font-weight: 600;
    display: inline-block;
}
.low { background: #e6f4ea; color: #137333; }
.medium { background: #fff4e5; color: #b06000; }
.high { background: #fdecea; color: #a50e0e; }
mark {
    background-color: #ffe58f;
    padding: 2px 4px;
    border-radius: 4px;
}
</style>
""", unsafe_allow_html=True)

# ---------------- HEADER ----------------
st.markdown('<div class="main-title">Privacy Policy Analyzer</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="subtitle">Understand privacy risks hidden inside long legal documents using AI-assisted analysis.</div>',
    unsafe_allow_html=True
)

# ---------------- INPUT CARD ----------------
st.markdown('<div class="card">', unsafe_allow_html=True)

st.subheader("📄 Provide Privacy Policy")
uploaded_file = st.file_uploader("Upload PDF", type=["pdf"])
policy_text = st.text_area("Or paste policy text", height=220)

st.markdown('</div>', unsafe_allow_html=True)

# ---------------- ANALYZE BUTTON ----------------
analyze = st.button("Analyze Policy", use_container_width=True)

# ---------------- PROCESSING ----------------
if analyze:
    if not uploaded_file and not policy_text.strip():
        st.warning("Please upload a PDF or paste privacy policy text.")
        st.stop()

    with st.spinner("Analyzing policy and detecting privacy risks..."):
        try:
            if uploaded_file:
                text_input = extract_text_from_pdf(uploaded_file)
                if not text_input.strip():
                    st.error("Could not extract text from PDF.")
                    st.stop()
            else:
                text_input = policy_text

            result = analyze_policy(text_input)

        except Exception as e:
            st.error("Analysis failed due to an internal error.")
            st.exception(e)
            st.stop()

    # ---------------- RESULTS ----------------
    st.markdown('<div class="section-title">Risk Assessment</div>', unsafe_allow_html=True)

    risk = result.get("risk_level", "Unknown")
    score = result.get("risk_score", 0)

    badge_class = risk.lower() if risk.lower() in ["low", "medium", "high"] else "medium"
    st.markdown(
        f'<span class="badge {badge_class}">Risk Level: {risk}</span>',
        unsafe_allow_html=True
    )

    st.progress(min(score / 10, 1.0))
    st.caption(f"Risk Score: {score} / 10")

    # ---------------- INSIGHTS ----------------
    st.markdown('<div class="section-title">Key Privacy Insights</div>', unsafe_allow_html=True)

    insights = generate_short_explanations(result.get("detected", []))
    for level, text in insights:
        if level == "High":
            st.error(text)
        elif level == "Medium":
            st.warning(text)
        else:
            st.success(text)

    # ---------------- HIGHLIGHTED POLICY ----------------
    st.markdown('<div class="section-title">Highlighted Risky Content</div>', unsafe_allow_html=True)

    highlighted = highlight_risky_terms(text_input, result.get("detected", []))

    st.markdown(
        f"""
        <div style="
            max-height:320px;
            overflow-y:auto;
            padding:16px;
            background:#ffffff;
            border-radius:10px;
            border:1px solid #ddd;
            color:#000;
            line-height:1.6;
        ">
        {highlighted}
        </div>
        """,
        unsafe_allow_html=True
    )

    # ---------------- DOWNLOAD ----------------
    report = generate_report(risk, insights)

    st.download_button(
        "Download Privacy Report",
        data=report,
        file_name="privacy_risk_report.txt",
        mime="text/plain",
        use_container_width=True
    )
