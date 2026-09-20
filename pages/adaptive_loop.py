from ui import hero, metric, plotly_base
import streamlit as st
from core.adaptive import replan
from services.store import save_state
import plotly.graph_objects as go

s=st.session_state.state
hero("07 · ADAPTIVE LOOP","Tell EduPath what happened. It replans.","This is the core loop: evidence → recommendation → practice → feedback → new recommendation. Difficulty and struggle become new learner evidence.")

feedback=st.text_area("What happened while learning?",height=170,placeholder="Example: I finished the FastAPI task quickly, but Docker networking was confusing. I can run containers but cannot explain bridge networking.")

if st.button("Replan from this evidence →",type="primary",use_container_width=True):
    if not feedback.strip(): st.warning("Tell the coach what happened first.")
    else:
        s["feedback"]=feedback
        with st.status("Adaptive Planner is recalculating your path…"):
            s=replan(s)
            st.session_state.state=s
            save_state(st.session_state.learner_id,s)
        st.success("Path updated. The next recommendation now reflects your feedback.")
        st.rerun()

if s.get("feedback"):
    st.markdown("### Latest learner evidence")
    st.markdown(f'<div class="success-box">{s["feedback"]}</div>',unsafe_allow_html=True)

    st.markdown("### Adaptive signal")
    gaps=s.get("gaps",[])
    left,right=st.columns(2)
    with left:
        fig=go.Figure(go.Bar(x=[g["priority_score"] for g in gaps[:8]],y=[g["skill"] for g in gaps[:8]],orientation="h"))
        fig.update_layout(title="Current priority after feedback",yaxis=dict(autorange="reversed"))
        st.plotly_chart(plotly_base(fig,350),use_container_width=True)
    with right:
        fig=go.Figure(go.Scatter(x=[g["confidence"]*100 for g in gaps[:10]],y=[g["gap"] for g in gaps[:10]],mode="markers+text",text=[g["skill"] for g in gaps[:10]],textposition="middle right"))
        fig.update_layout(title="Evidence confidence vs gap",xaxis_title="Confidence (%)",yaxis_title="Gap")
        st.plotly_chart(plotly_base(fig,350),use_container_width=True)

    st.markdown("### New critical path")
    st.write(" → ".join(s.get("critical_path",[])) or "No critical blockers.")
