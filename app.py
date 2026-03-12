
import streamlit as st
from groq import Groq
import os

# Page config
st.set_page_config(
    page_title="Resume Analyzer AI",
    page_icon="📄",
    layout="wide"
)

# Custom CSS
st.markdown("""
<style>
    .main { background-color: #f8f9fa; }
    .score-box {
        background: linear-gradient(135deg, #1F4E79, #2874A6);
        color: white;
        padding: 20px;
        border-radius: 15px;
        text-align: center;
        margin: 10px 0;
    }
    .score-number {
        font-size: 60px;
        font-weight: bold;
    }
    .section-box {
        background: white;
        padding: 20px;
        border-radius: 10px;
        border-left: 5px solid #1F4E79;
        margin: 10px 0;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    .green { border-left-color: #27AE60; }
    .red { border-left-color: #E74C3C; }
    .orange { border-left-color: #F39C12; }
</style>
""", unsafe_allow_html=True)

# Header
st.title("📄 AI Resume Analyzer")
st.markdown("**Paste your resume and a job description to get an instant AI-powered match analysis.**")
st.divider()

# API setup
GROQ_API_KEY = os.environ.get("GROQ_API_KEY", "")
if not GROQ_API_KEY:
    GROQ_API_KEY = st.text_input("Enter your Groq API Key", type="password")

def analyze_resume(resume_text, job_description):
    client = Groq(api_key=GROQ_API_KEY)
    prompt = f"""
You are an expert resume analyzer and career coach. Analyze the resume against the job description and return your analysis in EXACTLY this format:

MATCH SCORE: [a number from 0 to 100]

MATCHING SKILLS:
- [skill 1]
- [skill 2]
- [skill 3]

MISSING KEYWORDS:
- [keyword 1]
- [keyword 2]
- [keyword 3]

STRENGTHS:
- [strength 1]
- [strength 2]
- [strength 3]

IMPROVEMENTS:
- [improvement 1]
- [improvement 2]
- [improvement 3]

SUMMARY:
[2-3 sentence overall assessment]

Resume:
{resume_text}

Job Description:
{job_description}
"""
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content

def parse_response(text):
    sections = {
        "score": "",
        "matching": [],
        "missing": [],
        "strengths": [],
        "improvements": [],
        "summary": ""
    }
    lines = text.strip().split('\n')
    current = None

    for line in lines:
        line = line.strip()
        if line.startswith("MATCH SCORE:"):
            sections["score"] = line.replace("MATCH SCORE:", "").strip()
        elif line.startswith("MATCHING SKILLS:"):
            current = "matching"
        elif line.startswith("MISSING KEYWORDS:"):
            current = "missing"
        elif line.startswith("STRENGTHS:"):
            current = "strengths"
        elif line.startswith("IMPROVEMENTS:"):
            current = "improvements"
        elif line.startswith("SUMMARY:"):
            current = "summary"
        elif line.startswith("- ") and current in ["matching", "missing", "strengths", "improvements"]:
            sections[current].append(line[2:])
        elif current == "summary" and line:
            sections["summary"] += line + " "

    return sections

# Input columns
col1, col2 = st.columns(2)

with col1:
    st.subheader("📋 Your Resume")
    resume_text = st.text_area(
        "Paste your resume here",
        height=350,
        placeholder="Paste the full text of your resume..."
    )

with col2:
    st.subheader("💼 Job Description")
    job_desc = st.text_area(
        "Paste the job description here",
        height=350,
        placeholder="Paste the full job description you're applying for..."
    )

st.divider()

# Analyze button
if st.button("🔍 Analyze My Resume", use_container_width=True, type="primary"):
    if not resume_text or not job_desc:
        st.error("Please paste both your resume and the job description.")
    elif not GROQ_API_KEY:
        st.error("Please enter your Groq API key.")
    else:
        with st.spinner("Analyzing your resume... ⏳"):
            raw = analyze_resume(resume_text, job_desc)
            parsed = parse_response(raw)

        # Score
        try:
            score = int(''.join(filter(str.isdigit, parsed["score"])))
        except:
            score = 0

        color = "#27AE60" if score >= 70 else "#F39C12" if score >= 50 else "#E74C3C"
        label = "Strong Match 🎉" if score >= 70 else "Moderate Match ⚠️" if score >= 50 else "Weak Match ❌"

        st.markdown(f"""
        <div class="score-box">
            <div class="score-number" style="color:{color}">{score}/100</div>
            <div style="font-size:20px">{label}</div>
        </div>
        """, unsafe_allow_html=True)

        st.divider()

        # Results grid
        col1, col2 = st.columns(2)

        with col1:
            st.markdown('<div class="section-box green">', unsafe_allow_html=True)
            st.subheader("✅ Matching Skills")
            for item in parsed["matching"]:
                st.markdown(f"• {item}")
            st.markdown('</div>', unsafe_allow_html=True)

            st.markdown('<div class="section-box green">', unsafe_allow_html=True)
            st.subheader("💪 Strengths")
            for item in parsed["strengths"]:
                st.markdown(f"• {item}")
            st.markdown('</div>', unsafe_allow_html=True)

        with col2:
            st.markdown('<div class="section-box red">', unsafe_allow_html=True)
            st.subheader("❌ Missing Keywords")
            for item in parsed["missing"]:
                st.markdown(f"• {item}")
            st.markdown('</div>', unsafe_allow_html=True)

            st.markdown('<div class="section-box orange">', unsafe_allow_html=True)
            st.subheader("🔧 Suggested Improvements")
            for item in parsed["improvements"]:
                st.markdown(f"• {item}")
            st.markdown('</div>', unsafe_allow_html=True)

        st.divider()
        st.subheader("📝 Overall Summary")
        st.info(parsed["summary"])
