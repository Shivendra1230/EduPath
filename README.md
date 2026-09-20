# EduPath — Production Demo Build

EduPath is an evidence-first, adaptive learning agent.

## Why it is different

A normal course recommender asks: "What should everyone learn?"

EduPath asks:

**What can this learner prove today → what does the target role require → what is the highest-impact next skill → what practical evidence should they create → what changed after practice?**

## Requirements covered

- learner skills, experience, target role and career goal
- resume/portfolio/certificate/project parsing
- evidence-grounded skill gaps
- structured objectives
- role-specific resources
- weekly time-boxed plan
- practice/project missions
- completion tracking
- struggle feedback and adaptive replanning
- progress reporting
- natural-language coach
- interview generation and regeneration
- LangGraph orchestration
- Groq live reasoning model
- local SQLite learner-state persistence

## Run

```powershell
conda create -n edupath python=3.11 -y
conda activate edupath
pip install -r requirements.txt
copy .env.example .env
# add GROQ_API_KEY
streamlit run app.py
```

Recommended models:
- `openai/gpt-oss-120b` for coach/reasoning
- `openai/gpt-oss-20b` for fast structured tasks

The app still performs deterministic local analysis if Groq is unavailable, but the Career Copilot requires the API key for live model answers.
