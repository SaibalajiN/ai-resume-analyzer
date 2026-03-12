# ⚡ Job Application Assistant

An AI-powered web app that gives job seekers a complete toolkit for landing interviews — built with Llama 3.3 70B and Streamlit.

🔗 **[Live Demo]https://ai-resume-analyzer-h4ryhvbqr7w54cnhnh5pcn.streamlit.app/**

## 🚀 Features

### 📊 Resume Analyzer
- Scores your resume against any job description (0–100)
- Identifies matching skills and missing keywords
- Highlights strengths and suggests improvements
- Provides an AI-generated overall assessment

### ✍️ Bullet Rewriter
- Paste any weak resume bullet and get 3 powerful rewrites
- Tailors rewrites to a target role and job description keywords
- Explains why the new versions are stronger

### 📄 Cover Letter Generator
- Generates a tailored cover letter from your resume + job description
- Choose your tone: Professional, Enthusiastic, Concise, or Storytelling
- Avoids clichés and focuses on specific achievements

### 🤖 ATS Simulator
- Simulates how an Applicant Tracking System scans your resume
- Returns a PASS/FAIL verdict with ATS compatibility score
- Keyword-by-keyword match breakdown
- Flags format issues and critical missing keywords
- Tells you exactly how to pass the ATS

## 🛠️ Tech Stack

- **Python**
- **Streamlit** — web interface
- **Groq API (Llama 3.3 70B)** — LLM backbone
- **Deployed on Streamlit Cloud**

## 💡 Why I Built This

After going through my own job search, I wanted a tool that goes beyond basic resume scoring — something that actually helps you fix the problems and apply with confidence. This app covers the full application workflow in one place.

## 🚀 Run Locally

1. Clone the repo
```bash
   git clone https://github.com/YOUR_USERNAME/ai-resume-analyzer.git
   cd ai-resume-analyzer
```

2. Install dependencies
```bash
   pip install streamlit groq
```

3. Add your Groq API key
```bash
   export GROQ_API_KEY="your_key_here"
```

4. Run the app
```bash
   streamlit run app.py
```


## 👤 Author

**Saibalaji Neeli**
[LinkedIn](https://www.linkedin.com/in/saibalaji-neeli-08225818b/) · [Portfolio](https://www.datascienceportfol.io/neelis)
