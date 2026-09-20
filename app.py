import streamlit as st
from dotenv import load_dotenv
from core.llm import groq_service
from core.graphs import build_analysis_graph
from core.coach_graph import build_coach_graph
from services.store import ensure_learner, load_state, save_state
from ui import css, header, PAGES

load_dotenv()
st.set_page_config(page_title="EduPath", page_icon="assets/logo.svg", layout="wide", initial_sidebar_state="collapsed")
css()

if "learner_id" not in st.session_state:
    st.session_state.learner_id=ensure_learner()
if "state" not in st.session_state:
    st.session_state.state=load_state(st.session_state.learner_id)
if "chat" not in st.session_state:
    st.session_state.chat=[]
if "interview_nonce" not in st.session_state:
    st.session_state.interview_nonce=0

header(groq_service.live)
# IMPORTANT: st.navigation treats a dict as a section -> [pages] mapping.
# Passing {page_name: StreamlitPage} makes Streamlit try to iterate a single
# StreamlitPage, which causes: "TypeError: 'StreamlitPage' object is not iterable".
# Use a list for a flat navigation bar.
pages=[
    st.Page(
        f"pages/{name.split(' ',1)[1].lower().replace(' ','_')}.py",
        title=name.split(' ',1)[1],
    )
    for name in PAGES
]
selected=st.navigation(pages, position="top")
selected.run()
