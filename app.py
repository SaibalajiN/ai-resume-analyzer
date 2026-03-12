import streamlit as st
from groq import Groq
import os
import time

st.set_page_config(
    page_title="Resume Analyzer AI",
    page_icon="⚡",
    layout="wide"
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=DM+Sans:wght@300;400;500&display=swap');

*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

html, body, .stApp {
    background-color: #0a0a0f;
    color: #e8e6f0;
    font-family: 'DM Sans', sans-serif;
}

.stApp {
    background:
        radial-gradient(ellipse 80% 50% at 20% -10%, rgba(99, 60, 255, 0.15) 0%, transparent 60%),
        radial-gradient(ellipse 60% 40% at 80% 110%, rgba(0, 200, 180, 0.10) 0%, transparent 60%),
        #0a0a0f;
}

/* Hide streamlit chrome */
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding: 2rem 3rem 4rem; max-width: 1400px; }

/* ── HERO ── */
.hero {
    text-align: center;
    padding: 3.5rem 0 2.5rem;
    position: relative;
}
.hero-tag {
    display: inline-block;
    font-family: 'DM Sans', sans-serif;
    font-size: 0.7rem;
    font-weight: 500;
    letter-spacing: 0.2em;
    text-transform: uppercase;
    color: #7c6fff;
    background: rgba(124, 111, 255, 0.1);
    border: 1px solid rgba(124, 111, 255, 0.25);
    padding: 0.35rem 1rem;
    border-radius: 100px;
    margin-bottom: 1.2rem;
}
.hero h1 {
    font-family: 'Syne', sans-serif;
    font-size: clamp(2.8rem, 6vw, 5rem);
    font-weight: 800;
    line-height: 1.05;
    letter-spacing: -0.03em;
    background: linear-gradient(135deg, #ffffff 0%, #a89fff 50%, #00c8b4 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    margin-bottom: 1rem;
}
.hero p {
    font-size: 1.05rem;
    color: rgba(232, 230, 240, 0.55);
    max-width: 480px;
    margin: 0 auto;
    line-height: 1.6;
    font-weight: 300;
}

/* ── DIVIDER ── */
.glow-divider {
    height: 1px;
    background: linear-gradient(90deg, transparent, rgba(124, 111, 255, 0.4), rgba(0, 200, 180, 0.3), transparent);
    margin: 2rem 0;
}

/* ── INPUT PANELS ── */
.panel-label {
    font-family: 'Syne', sans-serif;
    font-size: 0.75rem;
    font-weight: 700;
    letter-spacing: 0.15em;
    text-transform: uppercase;
    color: rgba(232, 230, 240, 0.4);
    margin-bottom: 0.6rem;
}
.panel-title {
    font-family: 'Syne', sans-serif;
    font-size: 1.1rem;
    font-weight: 700;
    color: #e8e6f0;
    margin-bottom: 0.8rem;
}

/* Streamlit textarea override */
.stTextArea textarea {
    background: rgba(255,255,255,0.03) !important;
    border: 1px solid rgba(255,255,255,0.08) !important;
    border-radius: 12px !important;
    color: #e8e6f0 !important;
    font-family: 'DM Sans', sans-serif !important;
    font-size: 0.9rem !important;
    line-height: 1.6 !important;
    padding: 1rem !important;
    transition: border-color 0.2s !important;
}
.stTextArea textarea:focus {
    border-color: rgba(124, 111, 255, 0.5) !important;
    box-shadow: 0 0 0 3px rgba(124, 111, 255, 0.08) !important;
}
.stTextArea label { display: none !important; }

/* ── BUTTON ── */
.stButton > button {
    width: 100%;
    background: linear-gradient(135deg, #6339ff, #4f2de0) !important;
    color: white !important;
    border: none !important;
    border-radius: 12px !important;
    padding: 0.85rem 2rem !important;
    font-family: 'Syne', sans-serif !important;
    font-size: 1rem !important;
    font-weight: 700 !important;
    letter-spacing: 0.02em !important;
    cursor: pointer !important;
    transition: all 0.2s !important;
    box-shadow: 0 4px 24px rgba(99, 57, 255, 0.35) !important;
}
.stButton > button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 8px 32px rgba(99, 57, 255, 0.5) !important;
}

/* ── SCORE CARD ── */
.score-card {
    background: linear-gradient(135deg, rgba(99, 57, 255, 0.15), rgba(0, 200, 180, 0.08));
    border: 1px solid rgba(124, 111, 255, 0.2);
    border-radius: 20px;
    padding: 2.5rem;
    text-align: center;
    position: relative;
    overflow: hidden;
    margin: 1.5rem 0;
}
.score-card::before {
    content: '';
    position: absolute;
    top: -50%;
    left: -50%;
    width: 200%;
    height: 200%;
    background: radial-gradient(ellipse at center, rgba(99, 57, 255, 0.06) 0%, transparent 60%);
    pointer-events: none;
}
.score-number {
    font-family: 'Syne', sans-serif;
    font-size: 5rem;
    font-weight: 800;
    line-height: 1;
    margin-bottom: 0.5rem;
}
.score-label {
    font-family: 'DM Sans', sans-serif;
    font-size: 1rem;
    font-weight: 500;
    letter-spacing: 0.05em;
    opacity: 0.7;
}

/* ── RESULT CARDS ── */
.result-card {
    background: rgba(255,255,255,0.025);
    border: 1px solid rgba(255,255,255,0.07);
    border-radius: 16px;
    padding: 1.5rem;
    margin-bottom: 1rem;
    transition: border-color 0.2s;
}
.result-card:hover { border-color: rgba(124, 111, 255, 0.25); }
.result-card.green { border-left: 3px solid #00c8a0; }
.result-card.red { border-left: 3px solid #ff5c7a; }
.result-card.orange { border-left: 3px solid #ffaa40; }
.result-card.blue { border-left: 3px solid #7c6fff; }

.card-title {
    font-family: 'Syne', sans-serif;
    font-size: 0.75rem;
    font-weight: 700;
    letter-spacing: 0.15em;
    text-transform: uppercase;
    margin-bottom: 1rem;
}
.card-title.green { color: #00c8a0; }
.card-title.red { color: #ff5c7a; }
.card-title.orange { color: #ffaa40; }
.card-title.blue { color: #7c6fff; }

.card-item {
    display: flex;
    align-items: flex-start;
    gap: 0.6rem;
    margin-bottom: 0.6rem;
    font-size: 0.9rem;
    color: rgba(232, 230, 240, 0.75);
    line-height: 1.5;
}
.card-dot {
    width: 5px;
    height: 5px;
    border-radius: 50%;
    flex-shrink: 0;
    margin-top: 0.45rem;
}
.card-dot.green { background: #00c8a0; }
.card-dot.red { background: #ff5c7a; }
.card-dot.orange { background: #ffaa40; }
.card-dot.blue { background: #7c6fff; }

/* ── SUMMARY BOX ── */
.summary-box {
    background: rgba(124, 111, 255, 0.06);
    border: 1px solid rgba(124, 111, 255, 0.2);
    border-radius: 16px;
    padding: 1.5rem 1.8rem;
    font-size: 0.95rem;
    color: rgba(232, 230, 240, 0.8);
    line-height: 1.7;
    margin-top: 1rem;
}

/* ── SECTION TITLE ── */
.section-title {
    font-family: 'Syne', sans-serif;
    font-size: 1.3rem;
    font-weight: 700;
    color: #e8e6f0;
    margin: 2rem 0 1rem;
}

/* ── INPUT LABEL ── */
.input-label {
    font-family: 'Syne', sans-serif;
    font-size: 0.8rem;
    font-weight: 700;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    color: rgba(232, 230, 240, 0.45);
    margin-bottom: 0.5rem;
}

/* ── SPINNER ── */
.stSpinner { color: #7c6fff !important; }
</style>
""", unsafe_allow_html=True)

# ── HERO ──
st.markdown("""
<div class="hero">
    <div class="hero-tag">⚡ Powered by Llama 3.3 · 70B</div>
    <h1>Resume Analyzer</h1>
    <p>Paste your resume and a job description. Get an instant AI analysis of your match score, gaps, and how to improve.</p>
</div>
<div class="glow-divider"></div>
""", unsafe_allow_html=True)

# ── API SETUP ──
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
        "score": "", "matching": [], "missing": [],
        "strengths": [], "improvements": [], "summary": ""
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

# ── INPUT AREA ──
col1, col2 = st.columns(2, gap="large")

with col1:
    st.markdown('<div class="input-label">📋 Your Resume</div>', unsafe_allow_html=True)
    resume_text = st.text_area(
        "resume", height=320,
        placeholder="Paste the full text of your resume here...",
        label_visibility="collapsed"
    )

with col2:
    st.markdown('<div class="input-label">💼 Job Description</div>', unsafe_allow_html=True)
    job_desc = st.text_area(
        "jd", height=320,
        placeholder="Paste the job description you're applying for...",
        label_visibility="collapsed"
    )

st.markdown("<br>", unsafe_allow_html=True)

# ── ANALYZE BUTTON ──
if st.button("⚡ Analyze My Resume", use_container_width=True):
    if not resume_text or not job_desc:
        st.error("Please paste both your resume and the job description.")
    elif not GROQ_API_KEY:
        st.error("Please enter your Groq API key.")
    else:
        with st.spinner("Analyzing your resume..."):
            raw = analyze_resume(resume_text, job_desc)
            parsed = parse_response(raw)

        st.markdown('<div class="glow-divider" style="margin:2rem 0"></div>', unsafe_allow_html=True)

        # Score
        try:
            score = int(''.join(filter(str.isdigit, parsed["score"])))
        except:
            score = 0

        if score >= 70:
            score_color = "#00c8a0"
            label = "Strong Match 🎉"
        elif score >= 50:
            score_color = "#ffaa40"
            label = "Moderate Match ⚠️"
        else:
            score_color = "#ff5c7a"
            label = "Weak Match ❌"

        st.markdown(f"""
        <div class="score-card">
            <div class="score-number" style="color:{score_color}">{score}<span style="font-size:2rem;opacity:0.4">/100</span></div>
            <div class="score-label">{label}</div>
        </div>
        """, unsafe_allow_html=True)

        # Results grid
        col1, col2 = st.columns(2, gap="large")

        with col1:
            # Matching skills
            items_html = "".join([f'<div class="card-item"><div class="card-dot green"></div>{i}</div>' for i in parsed["matching"]])
            st.markdown(f'<div class="result-card green"><div class="card-title green">✓ Matching Skills</div>{items_html}</div>', unsafe_allow_html=True)

            # Strengths
            items_html = "".join([f'<div class="card-item"><div class="card-dot blue"></div>{i}</div>' for i in parsed["strengths"]])
            st.markdown(f'<div class="result-card blue"><div class="card-title blue">💪 Strengths</div>{items_html}</div>', unsafe_allow_html=True)

        with col2:
            # Missing keywords
            items_html = "".join([f'<div class="card-item"><div class="card-dot red"></div>{i}</div>' for i in parsed["missing"]])
            st.markdown(f'<div class="result-card red"><div class="card-title red">✗ Missing Keywords</div>{items_html}</div>', unsafe_allow_html=True)

            # Improvements
            items_html = "".join([f'<div class="card-item"><div class="card-dot orange"></div>{i}</div>' for i in parsed["improvements"]])
            st.markdown(f'<div class="result-card orange"><div class="card-title orange">→ Improvements</div>{items_html}</div>', unsafe_allow_html=True)

        # Summary
        st.markdown('<div class="section-title">📝 Overall Summary</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="summary-box">{parsed["summary"]}</div>', unsafe_allow_html=True)
