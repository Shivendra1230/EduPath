EduPath — Adaptive Career Intelligence

An adaptive multi-agent AI career coach that turns learner evidence into a personalized, continuously evolving learning journey.






🚀 Live Demo

Try EduPath:
https://edupath-xcanomatve6fft4bvapp2i.streamlit.app/

Source Code:
https://github.com/Shivendra1230/EduPath

🎯 The Problem

Learners often know where they want to go, but not:

what they already know well enough

which skills are actually missing

what to learn next

which resources are relevant to their specific gaps

what projects can prove the skill

whether they are ready for interviews

how their learning plan should change when they struggle

Most learning platforms provide a relatively fixed curriculum.

But two learners targeting the same role can have completely different:

backgrounds

project experience

skill levels

available time

weaknesses

learning progress

The core question

What if an AI system could understand where a learner is today, compare that evidence with a target career, and continuously adapt the journey as the learner learns?

That is the problem EduPath is designed to solve.

💡 What is EduPath?

EduPath is an adaptive career intelligence application powered by a multi-agent AI workflow.

A learner provides:

Resume / portfolio / certificates / project notes

Current skills and experience

Target career role

Career goal

Weekly learning capacity

Optional real job description

EduPath then builds a personalized career-learning state:

Learner Evidence
      ↓
Skill & Competency Analysis
      ↓
Target Role Requirements
      ↓
Skill Gap Detection
      ↓
Priority / Critical Path
      ↓
Personalized Learning Plan
      ↓
Resources + Practice Missions
      ↓
Interview Preparation
      ↓
Learner Feedback
      ↓
Adaptive Re-planning
      ↺

The goal is not to generate a roadmap once.

The goal is to maintain a living learning journey that changes with the learner.

🧠 Multi-Agent Architecture

EduPath uses LangGraph to orchestrate specialized agents around a shared learner state.

                         ┌──────────────────────┐
                         │      LEARNER         │
                         │ Resume / Skills /    │
                         │ Goal / Target Role   │
                         └──────────┬───────────┘
                                    │
                                    ▼
                         ┌──────────────────────┐
                         │  Evidence Analyst    │
                         │ Extract skills,      │
                         │ projects & evidence  │
                         └──────────┬───────────┘
                                    │
                                    ▼
                         ┌──────────────────────┐
                         │ Competency Mapper    │
                         │ Current vs Target    │
                         │ capability + gaps    │
                         └──────────┬───────────┘
                                    │
                                    ▼
                         ┌──────────────────────┐
                         │  Resource Curator    │
                         │ Gap → relevant       │
                         │ learning resources   │
                         └──────────┬───────────┘
                                    │
                                    ▼
                         ┌──────────────────────┐
                         │  Learning Planner    │
                         │ Objectives + weekly  │
                         │ learning sequence    │
                         └──────────┬───────────┘
                                    │
                                    ▼
                         ┌──────────────────────┐
                         │  Practice Designer   │
                         │ Proof-of-skill       │
                         │ missions             │
                         └──────────┬───────────┘
                                    │
                                    ▼
                         ┌──────────────────────┐
                         │   Interview Coach    │
                         │ Role + gap-specific  │
                         │ interview practice   │
                         └──────────┬───────────┘
                                    │
                                    ▼
                         ┌──────────────────────┐
                         │    Quality Critic    │
                         │ Validate consistency │
                         │ and output quality   │
                         └──────────┬───────────┘
                                    │
                                    ▼
                         ┌──────────────────────┐
                         │ Personalized Path    │
                         └──────────┬───────────┘
                                    │
                                    ▼
                         ┌──────────────────────┐
                         │ Learner Feedback     │
                         │ Progress / Struggle  │
                         └──────────┬───────────┘
                                    │
                                    └──────► Re-plan

Why multiple agents?

The system separates responsibilities instead of asking one general-purpose prompt to do everything.

For example:

Evidence Analyst focuses on extracting defensible learner evidence.

Competency Mapper focuses on current-vs-target capability.

Resource Curator connects gaps with useful resources.

Learning Planner converts gaps into executable objectives.

Practice Designer creates proof-of-skill tasks.

Interview Coach prepares role-specific interview practice.

Quality Critic checks the generated journey before it is presented.

LangGraph controls the workflow and shared state between these stages.

🔄 The Adaptive Learning Loop

This is the central product behavior.

Imagine a learner says:

"I understand embeddings, but I am struggling with vector database retrieval."

EduPath can use this new feedback as additional learner evidence.

The system can then:

New Feedback
     ↓
Re-evaluate affected skills
     ↓
Increase priority of the struggling competency
     ↓
Re-plan learning objectives
     ↓
Generate targeted practice
     ↓
Continue learning

So the journey becomes:

LEARN
  ↓
PRACTICE
  ↓
EVIDENCE
  ↓
FEEDBACK
  ↓
RE-PLAN
  ↓
LEARN AGAIN

This is the difference between a static roadmap and an adaptive learning agent.

🧩 Core Features

1. Learner Profile

Capture the context required for personalization:

Resume / portfolio

Target role

Career goal

Current skills

Experience

Weekly learning capacity

Optional job description

Supported evidence formats include:

PDF

DOCX

TXT

Markdown

2. Evidence Analysis

EduPath extracts structured evidence from learner-provided material.

The system can track:

Skill

Current capability

Target capability

Confidence

Evidence supporting the assessment

Potential blockers

This creates an evidence ledger instead of relying only on unsupported LLM assumptions.

3. Skill-Gap Mapping

The competency engine compares:

Current capability
        vs
Target-role requirement

and produces:

Gap

Importance / weight

Priority

Confidence

Critical-path dependencies

This helps answer:

"What am I actually missing for this role?"

4. Critical Path

Not every skill should be learned independently.

EduPath can identify dependencies between competencies and surface a sequence such as:

Embeddings
    ↓
Vector Search
    ↓
Retrieval
    ↓
RAG
    ↓
Agentic RAG
    ↓
Evaluation

This turns a large skill map into a more actionable sequence.

5. Personalized Study Path

The planner converts gaps into learning objectives containing:

Skill

Time estimate

Learning outcome

Success criteria

Relevant resources

The learner can mark objectives as completed and track progress.

6. Practice Lab

EduPath generates hands-on missions rather than only recommending content.

Practice formats can include:

Build Sprint

Debug Lab

Design Review

Evaluation Lab

Portfolio Upgrade

Interview-to-Code

Each mission can include:

Context

Task

Deliverable

Steps

Validation criteria

Hints

Common mistakes

Coaching support

The intent is to create evidence of skill, not just course completion.

7. Interview Coach

Interview preparation is tied to the learner's target role and skill gaps.

Questions can cover different modes such as:

Conceptual

Practical

Debugging

System design

Production trade-offs

For each question, EduPath can provide:

What the question is really asking

Why an interviewer asks it

What is being tested

Answer structure

Hint when stuck

Model answer

Common mistakes

Follow-up question

Doubt-clearing support

This turns interview preparation into an interactive coaching experience.

8. Career Copilot

Learners can ask natural-language questions about their journey.

Examples:

"I have only 2 hours today. What should I do?"

"Why is this my highest-priority gap?"

"Teach me vector databases from scratch."

"Review my evidence for this target role."

"Give me interview questions based on my weakest skills."

"Why did you change my learning plan?"

The Copilot uses the learner's current EduPath state instead of treating every question as an unrelated chat.

9. Adaptive Loop

Learner feedback can trigger re-planning.

Examples of feedback:

"I'm stuck on RAG."

"Embeddings are easy for me."

"I only have 3 hours this week."

"I already know Docker."

"I completed this project."

"I still cannot explain vector search in an interview."

These signals can change priorities and the next recommended actions.

10. Progress & Readiness

The dashboard surfaces:

Completed objectives

Remaining gaps

Current readiness

Next actions

Capability overview

Agent execution trace

The purpose is to give the learner a clear answer to:

"Where am I now, and what should I do next?"

🛠️ Technology Stack

Layer

Technology

UI

Streamlit

Language

Python

Agent orchestration

LangGraph

LLM inference

Groq

Fast reasoning model

openai/gpt-oss-20b

Higher-capability reasoning

openai/gpt-oss-120b

Structured data

Pydantic

Persistence

SQLite

Resume parsing

PyMuPDF

DOCX parsing

python-docx

Visualization

Plotly

Configuration

python-dotenv

🏗️ Project Structure

EduPath/
│
├── app.py
├── ui.py
├── requirements.txt
├── .env.example
├── .gitignore
│
├── agents/
│   ├── __init__.py
│   └── analyze.py
│
├── core/
│   ├── adaptive.py
│   ├── coach_graph.py
│   ├── competency.py
│   ├── graphs.py
│   └── llm.py
│
├── models/
│   ├── __init__.py
│   └── state.py
│
├── services/
│   ├── parser.py
│   └── store.py
│
├── pages/
│   ├── command_center.py
│   ├── profile.py
│   ├── evidence.py
│   ├── skill_map.py
│   ├── study_path.py
│   ├── practice_lab.py
│   ├── adaptive_loop.py
│   ├── interview_coach.py
│   ├── career_copilot.py
│   └── progress.py
│
├── data/
│   ├── roles.json
│   └── resources.json
│
├── assets/
│   └── logo.svg
│
├── tests/
│   └── test_core.py
│
├── ARCHITECTURE.md
├── DEMO_SCRIPT.md
├── LINKEDIN_POSTS.md
└── verify_install.py

⚙️ Local Setup

1. Clone the repository

git clone https://github.com/Shivendra1230/EduPath.git
cd EduPath

2. Create an environment

Using Conda:

conda create -n edupath python=3.12
conda activate edupath

Or using Python's built-in virtual environment:

python -m venv .venv

Activate it on Windows:

.venv\Scripts\activate

3. Install dependencies

pip install -r requirements.txt

4. Configure Groq

Copy:

.env.example

to:

.env

Set:

GROQ_API_KEY=your_groq_api_key

GROQ_MODEL_FAST=openai/gpt-oss-20b
GROQ_MODEL_REASONING=openai/gpt-oss-120b

Never commit .env or your API key to GitHub.

5. Run the application

streamlit run app.py

Then open the local Streamlit URL shown in the terminal.

🧪 Testing

Run the core tests:

pytest -q tests

Compile-check Python files:

python -m compileall .

☁️ Deployment

EduPath is deployed using Streamlit Community Cloud.

Production configuration

Repository: Shivendra1230/EduPath
Branch: main
Entry point: app.py

Set the following secrets in the deployment environment:

GROQ_API_KEY = "your_groq_api_key"
GROQ_MODEL_FAST = "openai/gpt-oss-20b"
GROQ_MODEL_REASONING = "openai/gpt-oss-120b"

Live application

https://edupath-xcanomatve6fft4bvapp2i.streamlit.app/

🎬 Recommended Demo Flow

For a short hackathon demonstration:

1. Start with the problem

Show that two learners targeting the same career can have different starting points.

2. Upload learner evidence

Use a resume / project profile and select a target role.

3. Run the analysis

Show the multi-agent workflow:

Evidence Analyst
      ↓
Competency Mapper
      ↓
Resource Curator
      ↓
Learning Planner
      ↓
Practice Designer
      ↓
Interview Coach
      ↓
Quality Critic

4. Show the Skill Map

Explain how current capability differs from target-role requirements.

5. Show the Study Path

Demonstrate that gaps become concrete learning objectives.

6. Show Practice Lab

Open a skill-specific mission.

7. Show Interview Coach

Open a question and demonstrate:

Question explanation

Interviewer intent

Hint

Model answer

Follow-up

Doubt clearing

8. Trigger adaptation

Tell EduPath:

"I'm struggling with vector databases."

Then show the affected priority / learning path being re-evaluated.

9. Ask the Copilot

Ask:

"Why did you change my learning path?"

This demonstrates stateful, context-aware coaching.

🧠 Design Principles

Evidence over assumptions

The system should distinguish between:

Skill mentioned

and:

Skill demonstrated with evidence

Personalization over generic curricula

The target role stays the same, but the path can differ for every learner.

Action over information

A gap should lead to:

Objective
→ Resource
→ Practice
→ Validation

not just a list of topics.

Feedback over static planning

A learner's new evidence should be able to influence future recommendations.

Specialized agents over one giant prompt

Each agent has a focused responsibility and operates through shared state.

🔐 Security Notes

API keys are loaded from environment variables.

.env is ignored by Git.

Never place secrets in source code.

Never commit production credentials.

For public deployment, keep only non-sensitive configuration in the repository.

🚧 Current Scope & Future Direction

EduPath is an evolving prototype focused on demonstrating an adaptive multi-agent learning workflow.

Potential future improvements include:

richer learner mastery modeling

stronger evidence verification

real-time web/resource discovery

automated skill assessments

portfolio artifact evaluation

calendar/task integrations

longitudinal learning analytics

stronger readiness evaluation

richer agent observability

external job-market skill signals

👨‍💻 Project

EduPath — Adaptive Career Intelligence

Built for the Agentic AI Hackathon conducted by Product Space.

Links

🌐 Live Demo: https://edupath-xcanomatve6fft4bvapp2i.streamlit.app/

💻 GitHub: https://github.com/Shivendra1230/EduPath

⭐ The Core Idea

EduPath does not generate one roadmap and stop. It continuously adapts the learner's journey as new evidence, progress, and feedback arrive.