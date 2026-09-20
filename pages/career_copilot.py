from ui import hero, metric
import streamlit as st
from core.coach_graph import build_coach_graph
from services.store import save_state
s=st.session_state.state
hero("09 · CAREER COPILOT","A coach, not a menu.","Ask anything: what to learn, why a gap matters, how to understand a concept, whether your resume proves a skill, how to prepare for an interview, how to use your remaining study time, or how to recover when you are stuck.")
quick=["I have 2 hours today. What should I do?","Why is my highest-priority gap important?","Teach me my hardest gap from scratch.","Review my evidence for the target role.","Give me 5 interview questions with answers."]
cols=st.columns(5)
for c,q in zip(cols,quick):
    if c.button(q,key="quick_"+q,use_container_width=True):
        st.session_state.pending_coach=q
if "pending_coach" in st.session_state:
    q=st.session_state.pop("pending_coach")
    s["coach_question"]=q
    s["coach_history"]=s.get("coach_history",[])+[{"role":"user","content":q}]
    with st.chat_message("assistant"):
        with st.spinner("EduPath is thinking…"):
            result=build_coach_graph().invoke(s)
        ans=result.get("coach_answer","")
        st.markdown(ans)
    s["coach_history"]+= [{"role":"assistant","content":ans}]
    save_state(st.session_state.learner_id,s)
    st.session_state.state=s
    st.rerun()

for m in s.get("coach_history",[]):
    with st.chat_message("user" if m["role"]=="user" else "assistant"):
        st.markdown(m["content"])

q=st.chat_input("Ask EduPath anything about your path…")
if q:
    s["coach_question"]=q
    s["coach_history"]=s.get("coach_history",[])+[{"role":"user","content":q}]
    with st.spinner("EduPath is thinking…"):
        result=build_coach_graph().invoke(s)
    ans=result.get("coach_answer","")
    s["coach_history"]+= [{"role":"assistant","content":ans}]
    save_state(st.session_state.learner_id,s)
    st.session_state.state=s
    st.rerun()
