# 📄 AI Resume Analyzer

An AI-powered web application that analyzes how well your resume matches a job description — built with Llama 3 and Streamlit.

## 🔍 What it does

- Scores your resume against a job description (0-100)
- Identifies matching skills and keywords
- Highlights missing keywords you should add
- Shows your strengths and suggests improvements
- Provides an overall AI-generated summary

## 🛠️ Tech Stack

- **Python**
- **Streamlit** — web interface
- **Groq API (Llama 3.3-70b)** — LLM for analysis
- **Google Colab** — development environment

## 🚀 How to run locally

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

## 💡 Why I built this

After struggling with resume rejections during my own job search, I built this tool to help job seekers instantly understand how well their resume matches any job description and what to improve.

## 📸 Screenshot

![App Screenshot](screenshot.png)

## 👤 Author

**Saibalaji Neeli** — [LinkedIn](https://www.linkedin.com/in/saibalaji-neeli-08225818b/) | [Portfolio](https://www.datascienceportfol.io/neelis)
