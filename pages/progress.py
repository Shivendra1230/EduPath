from ui import hero, metric, plotly_base
import streamlit as st, pandas as pd
import plotly.graph_objects as go

s=st.session_state.state
hero("04 · SKILL INTELLIGENCE","See the capability map, not a generic checklist.","Priority combines role importance, skill distance, prerequisite blockers and evidence confidence.")

if not s.get("gaps"):
    st.info("Analyze a learner profile first."); st.stop()

gaps=s["gaps"]
critical=s.get("critical_path",[])
a,b,c=st.columns(3)
with a: metric("Skills mapped",str(len(gaps)),"role-specific signals")
with b: metric("Critical path",str(len(critical)),"dependency chain")
with c: metric("Readiness",f"{s.get('readiness',0)}/100","current estimate")

st.markdown("### Critical path")
st.markdown(" → ".join(critical) or "No critical blockers.")

left,right=st.columns(2,gap="large")
with left:
    df=pd.DataFrame([{"Skill":g["skill"],"Current":g["current"],"Target":g["target"]} for g in gaps])
    fig=go.Figure()
    fig.add_bar(name="Current",x=df["Skill"],y=df["Current"])
    fig.add_bar(name="Target",x=df["Skill"],y=df["Target"])
    fig.update_layout(barmode="group",title="Capability distance")
    st.plotly_chart(plotly_base(fig,390),use_container_width=True)
with right:
    df=pd.DataFrame([{"Skill":g["skill"],"Confidence":round(g["confidence"]*100,1),"Gap":g["gap"]} for g in gaps])
    fig=go.Figure(go.Scatter(x=df["Confidence"],y=df["Gap"],mode="markers+text",text=df["Skill"],textposition="middle right"))
    fig.update_layout(title="Evidence confidence vs skill gap",xaxis_title="Evidence confidence (%)",yaxis_title="Gap")
    st.plotly_chart(plotly_base(fig,390),use_container_width=True)

df=pd.DataFrame([{"Skill":g["skill"],"Current":g["current"],"Target":g["target"],"Gap":g["gap"],"Weight":g["weight"],"Priority":g["priority_score"],"Confidence":round(g["confidence"]*100,1)} for g in gaps])
st.dataframe(df,use_container_width=True,hide_index=True)
