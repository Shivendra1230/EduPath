from langgraph.graph import StateGraph, START, END
from models.state import EduPathState
from core.llm import groq_service

COACH_SYSTEM="""You are EduPath Coach, a real human-like career learning coach.
You are NOT a menu navigator and must NEVER say "open Skill Intelligence" as a substitute for answering.
You have the learner's evidence, target role, goals, gaps, study plan and progress.
Answer the learner's actual question directly.

Rules:
- Use the learner context when relevant; don't invent achievements.
- Explain concepts at the learner's demonstrated level.
- Give concrete next actions with time estimates when planning.
- If asked about resources, explain why each resource fits.
- If asked about interviews, generate questions AND technically useful model answers.
- If asked about resume evidence, distinguish demonstrated evidence from inferred skill.
- If the question is unrelated to career learning, answer normally when safe.
- If current information is needed, say that live web research is required rather than pretending the static context is current.
- Do not repeat canned wording. Every response must address the exact question.
"""

def route_node(state):
    q=(state.get("coach_question") or "").lower()
    current=any(x in q for x in ["latest","today","current","recent","this week","news","2026"])
    state["coach_route"]="web" if current else "coach"
    return state

def answer_node(state):
    q=state.get("coach_question","")
    history=state.get("coach_history",[])[-8:]
    ctx={
      "target_role":state.get("target_role"),
      "career_goal":state.get("career_goal"),
      "readiness":state.get("readiness"),
      "critical_path":state.get("critical_path"),
      "gaps":state.get("gaps",[])[:8],
      "study_objectives":state.get("objectives",[])[:6],
      "resources":state.get("resources",[])[:8],
      "progress":state.get("progress",{}),
      "evidence":state.get("document_text","")[:10000]
    }
    if not groq_service.live:
        state["coach_answer"]="Groq is not connected yet. Add GROQ_API_KEY in .env to enable the live EduPath Coach. Your learner state is already loaded and can still be analyzed locally."
        return state
    msgs=[{"role":"system","content":COACH_SYSTEM},
          {"role":"user","content":f"Learner context:\n{ctx}\nConversation:\n{history}\n\nQuestion:\n{q}"}]
    try:
        state["coach_answer"]=groq_service.chat(COACH_SYSTEM,msgs[-1]["content"],groq_service.reasoning_model,.35,2200)
    except Exception as e:
        state["coach_answer"]=f"I hit a live model error: {e}. Your saved learner state is intact; retry once the model connection is available."
    return state

def build_coach_graph():
    g=StateGraph(EduPathState)
    g.add_node("route",route_node)
    g.add_node("answer",answer_node)
    g.add_edge(START,"route"); g.add_edge("route","answer"); g.add_edge("answer",END)
    return g.compile()
