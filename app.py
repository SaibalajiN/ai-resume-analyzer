import streamlit as st
from groq import Groq
import os

st.set_page_config(
    page_title="Job Application Assistant",
    page_icon="⚡",
    layout="wide"
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=DM+Sans:ital,wght@0,300;0,400;0,500;1,300&display=swap');

*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

html, body, .stApp {
    background-color: #07070f;
    color: #e8e6f0;
    font-family: 'DM Sans', sans-serif;
}
.stApp {
    background:
        radial-gradient(ellipse 80% 50% at 15% -5%, rgba(99,60,255,0.13) 0%, transparent 55%),
        radial-gradient(ellipse 60% 40% at 85% 105%, rgba(0,200,180,0.09) 0%, transparent 55%),
        #07070f;
}

#MainMenu, footer, header { visibility: hidden; }
.block-container { padding: 2rem 3rem 5rem; max-width: 1400px; }

.hero { text-align: center; padding: 3rem 0 2rem; }
.hero-tag {
    display: inline-block;
    font-size: 0.68rem; font-weight: 500; letter-spacing: 0.2em; text-transform: uppercase;
    color: #7c6fff; background: rgba(124,111,255,0.1);
    border: 1px solid rgba(124,111,255,0.25);
    padding: 0.3rem 1rem; border-radius: 100px; margin-bottom: 1.2rem;
}
.hero h1 {
    font-family: 'Syne', sans-serif;
    font-size: clamp(2.5rem, 5.5vw, 4.5rem); font-weight: 800; line-height: 1.05; letter-spacing: -0.03em;
    background: linear-gradient(135deg, #ffffff 0%, #a89fff 50%, #00c8b4 100%);
    -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text;
    margin-bottom: 0.8rem;
}
.hero p { font-size: 1rem; color: rgba(232,230,240,0.5); max-width: 500px; margin: 0 auto; line-height: 1.6; font-weight: 300; }

.glow-divider {
    height: 1px;
    background: linear-gradient(90deg, transparent, rgba(124,111,255,0.35), rgba(0,200,180,0.25), transparent);
    margin: 1.5rem 0;
}

.stTabs [data-baseweb="tab-list"] {
    background: rgba(255,255,255,0.03) !important; border: 1px solid rgba(255,255,255,0.07) !important;
    border-radius: 12px !important; padding: 4px !important; gap: 2px !important;
}
.stTabs [data-baseweb="tab"] {
    background: transparent !important; border-radius: 9px !important;
    color: rgba(232,230,240,0.45) !important; font-family: 'Syne', sans-serif !important;
    font-size: 0.82rem !important; font-weight: 700 !important; letter-spacing: 0.05em !important;
    padding: 0.55rem 1.2rem !important; border: none !important; transition: all 0.2s !important;
}
.stTabs [aria-selected="true"] {
    background: linear-gradient(135deg, rgba(99,57,255,0.7), rgba(79,45,224,0.7)) !important;
    color: white !important; box-shadow: 0 2px 12px rgba(99,57,255,0.3) !important;
}
.stTabs [data-baseweb="tab-highlight"], .stTabs [data-baseweb="tab-border"] { display: none !important; }

.stTextArea textarea {
    background: #1a1a2e !important; border: 1px solid rgba(255,255,255,0.08) !important;
    border-radius: 12px !important; color: #e8e6f0 !important; font-family: 'DM Sans', sans-serif !important;
    font-size: 0.88rem !important; line-height: 1.65 !important; padding: 1rem !important; transition: border-color 0.2s !important;
}
.stTextArea textarea:focus { border-color: rgba(124,111,255,0.45) !important; box-shadow: 0 0 0 3px rgba(124,111,255,0.07) !important; }
.stTextArea label, .stTextInput label { display: none !important; }
.stTextInput input {
    background: rgba(255,255,255,0.03) !important; border: 1px solid rgba(255,255,255,0.08) !important;
    border-radius: 12px !important; color: #e8e6f0 !important; font-family: 'DM Sans', sans-serif !important;
    font-size: 0.88rem !important; padding: 0.7rem 1rem !important;
}
.stSelectbox > div > div {
    background: rgba(255,255,255,0.03) !important; border: 1px solid rgba(255,255,255,0.08) !important;
    border-radius: 12px !important; color: #e8e6f0 !important;
}
.stSelectbox label { display: none !important; }

.stButton > button {
    width: 100%; background: linear-gradient(135deg, #6339ff, #4f2de0) !important;
    color: white !important; border: none !important; border-radius: 12px !important;
    padding: 0.8rem 2rem !important; font-family: 'Syne', sans-serif !important;
    font-size: 0.92rem !important; font-weight: 700 !important; letter-spacing: 0.03em !important;
    cursor: pointer !important; transition: all 0.2s !important; box-shadow: 0 4px 20px rgba(99,57,255,0.3) !important;
}
.stButton > button:hover { transform: translateY(-2px) !important; box-shadow: 0 8px 28px rgba(99,57,255,0.45) !important; }

.score-card {
    background: linear-gradient(135deg, rgba(99,57,255,0.12), rgba(0,200,180,0.06));
    border: 1px solid rgba(124,111,255,0.18); border-radius: 20px; padding: 2.5rem;
    text-align: center; margin: 1.5rem 0;
}
.score-number { font-family: 'Syne', sans-serif; font-size: 5rem; font-weight: 800; line-height: 1; margin-bottom: 0.4rem; }
.score-label { font-size: 1rem; font-weight: 500; opacity: 0.65; letter-spacing: 0.04em; }

.result-card {
    background: rgba(255,255,255,0.022); border: 1px solid rgba(255,255,255,0.07);
    border-radius: 16px; padding: 1.4rem 1.6rem; margin-bottom: 1rem;
}
.result-card.green  { border-left: 3px solid #00c8a0; }
.result-card.red    { border-left: 3px solid #ff5c7a; }
.result-card.orange { border-left: 3px solid #ffaa40; }
.result-card.blue   { border-left: 3px solid #7c6fff; }
.result-card.teal   { border-left: 3px solid #00c8b4; }

.card-title { font-family: 'Syne', sans-serif; font-size: 0.72rem; font-weight: 700; letter-spacing: 0.15em; text-transform: uppercase; margin-bottom: 0.9rem; }
.card-title.green  { color: #00c8a0; } .card-title.red    { color: #ff5c7a; }
.card-title.orange { color: #ffaa40; } .card-title.blue   { color: #7c6fff; } .card-title.teal   { color: #00c8b4; }

.card-item { display: flex; align-items: flex-start; gap: 0.6rem; margin-bottom: 0.55rem; font-size: 0.88rem; color: rgba(232,230,240,0.72); line-height: 1.55; }
.dot { width:5px; height:5px; border-radius:50%; flex-shrink:0; margin-top:0.45rem; }
.dot.green{background:#00c8a0;} .dot.red{background:#ff5c7a;} .dot.orange{background:#ffaa40;} .dot.blue{background:#7c6fff;} .dot.teal{background:#00c8b4;}

.summary-box { background: rgba(124,111,255,0.055); border: 1px solid rgba(124,111,255,0.18); border-radius: 16px; padding: 1.4rem 1.7rem; font-size: 0.93rem; color: rgba(232,230,240,0.78); line-height: 1.75; margin-top: 0.5rem; }
.output-box { background: rgba(255,255,255,0.025); border: 1px solid rgba(255,255,255,0.08); border-radius: 14px; padding: 1.4rem 1.7rem; font-size: 0.9rem; color: rgba(232,230,240,0.8); line-height: 1.75; margin-top: 0.5rem; white-space: pre-wrap; }
.bullet-card { background: rgba(255,255,255,0.025); border: 1px solid rgba(0,200,180,0.2); border-radius: 14px; padding: 1.2rem 1.5rem; margin-bottom: 0.8rem; font-size: 0.9rem; color: rgba(232,230,240,0.82); line-height: 1.65; }
.bullet-num { font-family: 'Syne', sans-serif; font-size: 0.68rem; font-weight: 700; letter-spacing: 0.12em; text-transform: uppercase; color: #00c8b4; margin-bottom: 0.5rem; }

.verdict-pass { font-family: 'Syne', sans-serif; font-size: 2rem; font-weight: 800; color: #00c8a0; text-align: center; padding: 1.5rem; background: rgba(0,200,160,0.07); border: 1px solid rgba(0,200,160,0.2); border-radius: 16px; margin: 1.2rem 0; }
.verdict-fail { font-family: 'Syne', sans-serif; font-size: 2rem; font-weight: 800; color: #ff5c7a; text-align: center; padding: 1.5rem; background: rgba(255,92,122,0.07); border: 1px solid rgba(255,92,122,0.2); border-radius: 16px; margin: 1.2rem 0; }

.section-label { font-family: 'Syne', sans-serif; font-size: 0.72rem; font-weight: 700; letter-spacing: 0.15em; text-transform: uppercase; color: rgba(232,230,240,0.38); margin-bottom: 0.5rem; }
.section-title { font-family: 'Syne', sans-serif; font-size: 1.15rem; font-weight: 700; color: #e8e6f0; margin: 1.8rem 0 0.9rem; }
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="hero">
    <div class="hero-tag">⚡ Powered by Llama 3.3 · 70B</div>
    <h1>Job Application Assistant</h1>
    <p>Your AI-powered toolkit for landing interviews — analyze, optimize, and apply with confidence.</p>
</div>
<div class="glow-divider"></div>
""", unsafe_allow_html=True)

GROQ_API_KEY = os.environ.get("GROQ_API_KEY", "")
if not GROQ_API_KEY:
    st.markdown('<div class="section-label">🔑 API Key</div>', unsafe_allow_html=True)
    GROQ_API_KEY = st.text_input("groq_key", type="password", placeholder="Enter your Groq API key...", label_visibility="collapsed")

def call_llm(prompt):
    client = Groq(api_key=GROQ_API_KEY)
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content

def parse_analysis(text):
    sections = {"score": "", "matching": [], "missing": [], "strengths": [], "improvements": [], "summary": ""}
    lines = text.strip().split('\n')
    current = None
    for line in lines:
        line = line.strip()
        if line.startswith("MATCH SCORE:"): sections["score"] = line.replace("MATCH SCORE:", "").strip()
        elif line.startswith("MATCHING SKILLS:"): current = "matching"
        elif line.startswith("MISSING KEYWORDS:"): current = "missing"
        elif line.startswith("STRENGTHS:"): current = "strengths"
        elif line.startswith("IMPROVEMENTS:"): current = "improvements"
        elif line.startswith("SUMMARY:"): current = "summary"
        elif line.startswith("- ") and current in ["matching","missing","strengths","improvements"]: sections[current].append(line[2:])
        elif current == "summary" and line: sections["summary"] += line + " "
    return sections

def render_card(color, icon, title, items):
    items_html = "".join([f'<div class="card-item"><div class="dot {color}"></div>{i}</div>' for i in items])
    return f'<div class="result-card {color}"><div class="card-title {color}">{icon} {title}</div>{items_html}</div>'

if "resume_text" not in st.session_state: st.session_state.resume_text = ""
if "jd_text" not in st.session_state: st.session_state.jd_text = ""

tab1, tab2, tab3, tab4 = st.tabs(["📊  Resume Analyzer", "✍️  Bullet Rewriter", "📄  Cover Letter", "🤖  ATS Simulator"])

# ── TAB 1: RESUME ANALYZER ──
with tab1:
    st.markdown("<br>", unsafe_allow_html=True)
    col1, col2 = st.columns(2, gap="large")
    with col1:
        st.markdown('<div class="section-label">📋 Your Resume</div>', unsafe_allow_html=True)
        resume_t1 = st.text_area("r1", height=300, placeholder="Paste your resume here...", label_visibility="collapsed", value=st.session_state.resume_text)
    with col2:
        st.markdown('<div class="section-label">💼 Job Description</div>', unsafe_allow_html=True)
        jd_t1 = st.text_area("j1", height=300, placeholder="Paste the job description here...", label_visibility="collapsed", value=st.session_state.jd_text)
    st.markdown("<br>", unsafe_allow_html=True)

    if st.button("⚡ Analyze My Resume", key="btn1"):
        if not resume_t1 or not jd_t1: st.error("Please paste both your resume and the job description.")
        elif not GROQ_API_KEY: st.error("Please enter your Groq API key.")
        else:
            st.session_state.resume_text = resume_t1
            st.session_state.jd_text = jd_t1
            with st.spinner("Analyzing your resume..."):
                raw = call_llm(f"""Analyze the resume against the job description. Return EXACTLY in this format:

MATCH SCORE: [0-100]
MATCHING SKILLS:
- [skill]
- [skill]
- [skill]
MISSING KEYWORDS:
- [keyword]
- [keyword]
- [keyword]
STRENGTHS:
- [strength]
- [strength]
- [strength]
IMPROVEMENTS:
- [improvement]
- [improvement]
- [improvement]
SUMMARY:
[2-3 sentence assessment]

Resume: {resume_t1}
Job Description: {jd_t1}""")
                parsed = parse_analysis(raw)

            try: score = int(''.join(filter(str.isdigit, parsed["score"])))
            except: score = 0
            sc = "#00c8a0" if score>=70 else "#ffaa40" if score>=50 else "#ff5c7a"
            lbl = "Strong Match 🎉" if score>=70 else "Moderate Match ⚠️" if score>=50 else "Weak Match ❌"

            st.markdown('<div class="glow-divider" style="margin:2rem 0"></div>', unsafe_allow_html=True)
            st.markdown(f'<div class="score-card"><div class="score-number" style="color:{sc}">{score}<span style="font-size:2rem;opacity:0.35">/100</span></div><div class="score-label">{lbl}</div></div>', unsafe_allow_html=True)

            c1, c2 = st.columns(2, gap="large")
            with c1:
                st.markdown(render_card("green","✓","Matching Skills",parsed["matching"]), unsafe_allow_html=True)
                st.markdown(render_card("blue","💪","Strengths",parsed["strengths"]), unsafe_allow_html=True)
            with c2:
                st.markdown(render_card("red","✗","Missing Keywords",parsed["missing"]), unsafe_allow_html=True)
                st.markdown(render_card("orange","→","Improvements",parsed["improvements"]), unsafe_allow_html=True)
            st.markdown('<div class="section-title">📝 Overall Summary</div>', unsafe_allow_html=True)
            st.markdown(f'<div class="summary-box">{parsed["summary"]}</div>', unsafe_allow_html=True)

# ── TAB 2: BULLET REWRITER ──
with tab2:
    st.markdown("<br>", unsafe_allow_html=True)
    col1, col2 = st.columns(2, gap="large")
    with col1:
        st.markdown('<div class="section-label">📌 Original Bullet Point</div>', unsafe_allow_html=True)
        bullet_in = st.text_area("bi", height=120, placeholder='"Worked on machine learning models to improve recommendation system"', label_visibility="collapsed")
        st.markdown('<div class="section-label" style="margin-top:1rem">🎯 Target Role (optional)</div>', unsafe_allow_html=True)
        role_in = st.text_input("ri", placeholder='e.g. "Data Scientist at Google"', label_visibility="collapsed")
    with col2:
        st.markdown('<div class="section-label">💼 Job Description Keywords (optional)</div>', unsafe_allow_html=True)
        jd_b = st.text_area("jb", height=180, placeholder="Paste job description to tailor rewrites to specific keywords...", label_visibility="collapsed")
    st.markdown("<br>", unsafe_allow_html=True)

    if st.button("✍️ Rewrite My Bullet", key="btn2"):
        if not bullet_in: st.error("Please paste a bullet point to rewrite.")
        elif not GROQ_API_KEY: st.error("Please enter your Groq API key.")
        else:
            with st.spinner("Rewriting your bullet..."):
                ctx = f"\nTarget role: {role_in}" if role_in else ""
                jctx = f"\nJob keywords: {jd_b}" if jd_b else ""
                result = call_llm(f"""Rewrite this resume bullet into 3 powerful versions. Start with strong action verbs, include metrics, focus on impact.

Return EXACTLY:
VERSION 1:
[bullet]

VERSION 2:
[bullet]

VERSION 3:
[bullet]

EXPLANATION:
[2-3 sentences on what makes these better]

Original: {bullet_in}{ctx}{jctx}""")

            st.markdown('<div class="glow-divider" style="margin:1.5rem 0"></div>', unsafe_allow_html=True)
            st.markdown('<div class="section-title">✨ Rewritten Versions</div>', unsafe_allow_html=True)

            lines = result.strip().split('\n')
            versions, explanation = [], ""
            cur_v, cur_t = None, ""
            in_exp = False
            for line in lines:
                line = line.strip()
                if line.startswith("VERSION"):
                    if cur_v and cur_t: versions.append((cur_v, cur_t.strip()))
                    cur_v, cur_t = line.replace(":","").strip(), ""
                elif line.startswith("EXPLANATION:"):
                    if cur_v and cur_t: versions.append((cur_v, cur_t.strip()))
                    cur_v = None; in_exp = True
                elif cur_v and line: cur_t += line + " "
                elif in_exp and line: explanation += line + " "

            for lbl, txt in versions:
                st.markdown(f'<div class="bullet-card"><div class="bullet-num">{lbl}</div>{txt}</div>', unsafe_allow_html=True)
            if explanation:
                st.markdown('<div class="section-title">💡 Why These Are Better</div>', unsafe_allow_html=True)
                st.markdown(f'<div class="summary-box">{explanation}</div>', unsafe_allow_html=True)

# ── TAB 3: COVER LETTER ──
with tab3:
    st.markdown("<br>", unsafe_allow_html=True)
    col1, col2 = st.columns(2, gap="large")
    with col1:
        st.markdown('<div class="section-label">📋 Your Resume</div>', unsafe_allow_html=True)
        resume_cl = st.text_area("rcl", height=220, placeholder="Paste your resume here...", label_visibility="collapsed", value=st.session_state.resume_text)
        st.markdown('<div class="section-label" style="margin-top:1rem">🏢 Company Name</div>', unsafe_allow_html=True)
        company = st.text_input("co", placeholder='e.g. "Google"', label_visibility="collapsed")
        st.markdown('<div class="section-label" style="margin-top:0.8rem">👤 Hiring Manager (optional)</div>', unsafe_allow_html=True)
        manager = st.text_input("mg", placeholder='e.g. "Sarah Chen" or leave blank', label_visibility="collapsed")
    with col2:
        st.markdown('<div class="section-label">💼 Job Description</div>', unsafe_allow_html=True)
        jd_cl = st.text_area("jcl", height=220, placeholder="Paste the job description here...", label_visibility="collapsed", value=st.session_state.jd_text)
        st.markdown('<div class="section-label" style="margin-top:1rem">🎯 Tone</div>', unsafe_allow_html=True)
        tone = st.selectbox("tn", ["Professional & Confident","Enthusiastic & Energetic","Concise & Direct","Storytelling & Personal"], label_visibility="collapsed")
    st.markdown("<br>", unsafe_allow_html=True)

    if st.button("📄 Generate Cover Letter", key="btn3"):
        if not resume_cl or not jd_cl: st.error("Please paste both your resume and the job description.")
        elif not GROQ_API_KEY: st.error("Please enter your Groq API key.")
        else:
            st.session_state.resume_text = resume_cl
            st.session_state.jd_text = jd_cl
            with st.spinner("Writing your cover letter..."):
                addr = manager if manager else "Hiring Manager"
                comp = company if company else "your company"
                cl = call_llm(f"""Write a compelling cover letter. Tone: {tone}. Addressed to: {addr}. Company: {comp}.
3-4 paragraphs, under 350 words. Hook opening (not 'I am applying for'). 2-3 specific achievements matching the JD. Confident close.
No clichés like 'team player', 'passionate about', 'great fit'. Start with 'Dear {addr},'

Resume: {resume_cl}
Job Description: {jd_cl}""")

            st.markdown('<div class="glow-divider" style="margin:1.5rem 0"></div>', unsafe_allow_html=True)
            st.markdown('<div class="section-title">📄 Your Cover Letter</div>', unsafe_allow_html=True)
            st.markdown(f'<div class="output-box">{cl}</div>', unsafe_allow_html=True)
            st.markdown('<div style="margin-top:0.8rem;font-size:0.8rem;color:rgba(232,230,240,0.3);text-align:center">Select all text above and copy to use in your application</div>', unsafe_allow_html=True)

# ── TAB 4: ATS SIMULATOR ──
with tab4:
    st.markdown("<br>", unsafe_allow_html=True)
    col1, col2 = st.columns(2, gap="large")
    with col1:
        st.markdown('<div class="section-label">📋 Your Resume</div>', unsafe_allow_html=True)
        resume_ats = st.text_area("rats", height=300, placeholder="Paste your resume here...", label_visibility="collapsed", value=st.session_state.resume_text)
    with col2:
        st.markdown('<div class="section-label">💼 Job Description</div>', unsafe_allow_html=True)
        jd_ats = st.text_area("jats", height=300, placeholder="Paste the job description here...", label_visibility="collapsed", value=st.session_state.jd_text)
    st.markdown("<br>", unsafe_allow_html=True)

    if st.button("🤖 Run ATS Simulation", key="btn4"):
        if not resume_ats or not jd_ats: st.error("Please paste both your resume and the job description.")
        elif not GROQ_API_KEY: st.error("Please enter your Groq API key.")
        else:
            st.session_state.resume_text = resume_ats
            st.session_state.jd_text = jd_ats
            with st.spinner("Simulating ATS scan..."):
                raw_ats = call_llm(f"""Simulate an ATS scanner analyzing this resume vs job description. Return EXACTLY:

ATS VERDICT: [PASS or FAIL]
ATS SCORE: [0-100]
KEYWORD MATCHES:
- [keyword]: [found or not found]
- [keyword]: [found or not found]
- [keyword]: [found or not found]
- [keyword]: [found or not found]
- [keyword]: [found or not found]
FORMAT ISSUES:
- [issue or "None detected"]
CRITICAL MISSING KEYWORDS:
- [keyword]
- [keyword]
- [keyword]
WARNINGS:
- [warning]
- [warning]
HOW TO PASS THIS ATS:
- [fix]
- [fix]
- [fix]

Resume: {resume_ats}
Job Description: {jd_ats}""")

            lines = raw_ats.strip().split('\n')
            ats = {"verdict":"","score":"","keywords":[],"format_issues":[],"critical_missing":[],"warnings":[],"fixes":[]}
            cur = None
            for line in lines:
                line = line.strip()
                if line.startswith("ATS VERDICT:"): ats["verdict"] = line.replace("ATS VERDICT:","").strip()
                elif line.startswith("ATS SCORE:"): ats["score"] = line.replace("ATS SCORE:","").strip()
                elif line.startswith("KEYWORD MATCHES:"): cur = "keywords"
                elif line.startswith("FORMAT ISSUES:"): cur = "format_issues"
                elif line.startswith("CRITICAL MISSING"): cur = "critical_missing"
                elif line.startswith("WARNINGS:"): cur = "warnings"
                elif line.startswith("HOW TO PASS"): cur = "fixes"
                elif line.startswith("- ") and cur: ats[cur].append(line[2:])

            st.markdown('<div class="glow-divider" style="margin:1.5rem 0"></div>', unsafe_allow_html=True)

            if "PASS" in ats["verdict"].upper():
                st.markdown('<div class="verdict-pass">✅ ATS VERDICT: PASS</div>', unsafe_allow_html=True)
            else:
                st.markdown('<div class="verdict-fail">❌ ATS VERDICT: FAIL</div>', unsafe_allow_html=True)

            try: ascore = int(''.join(filter(str.isdigit, ats["score"])))
            except: ascore = 0
            asc = "#00c8a0" if ascore>=70 else "#ffaa40" if ascore>=50 else "#ff5c7a"
            st.markdown(f'<div class="score-card" style="margin:1rem 0"><div class="score-number" style="color:{asc}">{ascore}<span style="font-size:2rem;opacity:0.35">/100</span></div><div class="score-label">ATS Compatibility Score</div></div>', unsafe_allow_html=True)

            c1, c2 = st.columns(2, gap="large")
            with c1:
                kw_html = "".join([f'<div class="card-item"><div class="dot {"green" if "not" not in k.lower() and "found" in k.lower() else "red"}"></div>{k}</div>' for k in ats["keywords"]])
                st.markdown(f'<div class="result-card green"><div class="card-title green">🔍 Keyword Matches</div>{kw_html}</div>', unsafe_allow_html=True)
                fmt_html = "".join([f'<div class="card-item"><div class="dot orange"></div>{i}</div>' for i in ats["format_issues"]])
                st.markdown(f'<div class="result-card orange"><div class="card-title orange">⚠️ Format Issues</div>{fmt_html}</div>', unsafe_allow_html=True)
            with c2:
                cm_html = "".join([f'<div class="card-item"><div class="dot red"></div>{i}</div>' for i in ats["critical_missing"]])
                st.markdown(f'<div class="result-card red"><div class="card-title red">🚨 Critical Missing Keywords</div>{cm_html}</div>', unsafe_allow_html=True)
                fix_html = "".join([f'<div class="card-item"><div class="dot teal"></div>{i}</div>' for i in ats["fixes"]])
                st.markdown(f'<div class="result-card teal"><div class="card-title teal">✅ How to Pass This ATS</div>{fix_html}</div>', unsafe_allow_html=True)
            if ats["warnings"]:
                warn_html = "".join([f'<div class="card-item"><div class="dot blue"></div>{i}</div>' for i in ats["warnings"]])
                st.markdown(f'<div class="result-card blue"><div class="card-title blue">💡 Warnings</div>{warn_html}</div>', unsafe_allow_html=True)
