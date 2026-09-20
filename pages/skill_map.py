import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from ui import hero, metric, plotly_base

s = st.session_state.state
hero(
    "04 · SKILL INTELLIGENCE",
    "See the capability system, not a checklist.",
    "EduPath maps evidence → competencies → dependencies → priorities. The charts below are designed for decision-making, not decoration.",
)

if not s.get("gaps"):
    st.info("Analyze a learner profile first.")
    st.stop()

gaps = s["gaps"]
critical = s.get("critical_path", [])
a, b, c = st.columns(3)
with a: metric("Skills mapped", str(len(gaps)), "role-specific signals")
with b: metric("Critical path", str(len(critical)), "dependency chain")
with c: metric("Readiness", f"{s.get('readiness',0)}/100", "current estimate")

# Judge-facing agent control plane: this is backed by the actual LangGraph trace.
st.markdown("### Multi-agent control plane")
trace = s.get("agent_trace", [])
expected = [
    ("Evidence Analyst", "Extract grounded evidence"),
    ("Competency Mapper", "Map skill gaps + dependencies"),
    ("Resource Curator", "Select targeted resources"),
    ("Learning Planner", "Build adaptive objectives"),
    ("Practice Designer", "Create proof missions"),
    ("Interview Coach", "Generate role-linked probes"),
    ("Quality Critic", "Validate the handoff"),
]
cols = st.columns(len(expected))
for i, (name, purpose) in enumerate(expected):
    done = any(x.get("agent") == name for x in trace)
    with cols[i]:
        st.markdown(
            f'<div class="card agent-card"><div class="agent-dot {"done" if done else "idle"}"></div>'
            f'<div class="agent-name">{name}</div><div class="muted">{purpose}</div>'
            f'<div class="agent-status">{"✓ completed" if done else "waiting"}</div></div>',
            unsafe_allow_html=True,
        )

st.markdown("### Critical path")
st.markdown(" → ".join(critical) or "No critical blockers.")

left, right = st.columns(2, gap="large")
with left:
    # Horizontal bars prevent long skill names from colliding.
    df = pd.DataFrame([{"Skill": g["skill"], "Current": g["current"], "Target": g["target"]} for g in gaps])
    df = df.sort_values("Target", ascending=True)
    fig = go.Figure()
    fig.add_bar(name="Target", y=df["Skill"], x=df["Target"], orientation="h")
    fig.add_bar(name="Current", y=df["Skill"], x=df["Current"], orientation="h")
    fig.update_layout(
        barmode="group",
        title="Capability distance",
        xaxis_title="Level (0–5)",
        yaxis_title="",
        xaxis=dict(range=[0, 5.4], dtick=1),
        legend=dict(orientation="h", y=1.12, x=1, xanchor="right"),
    )
    st.plotly_chart(plotly_base(fig, max(390, 34 * len(df) + 100)), use_container_width=True)

with right:
    # No permanent text labels: hover shows the complete skill name cleanly.
    df = pd.DataFrame([
        {"Skill": g["skill"], "Confidence": round(g["confidence"] * 100, 1), "Gap": g["gap"], "Priority": g["priority_score"]}
        for g in gaps
    ])
    fig = go.Figure(go.Scatter(
        x=df["Confidence"],
        y=df["Gap"],
        mode="markers",
        marker=dict(size=11, opacity=.9),
        customdata=df[["Skill", "Priority"]],
        hovertemplate="<b>%{customdata[0]}</b><br>Evidence confidence: %{x:.0f}%<br>Skill gap: %{y}<br>Priority score: %{customdata[1]:.1f}<extra></extra>",
    ))
    fig.update_layout(
        title="Evidence confidence vs skill gap",
        xaxis_title="Evidence confidence (%)",
        yaxis_title="Gap",
        xaxis=dict(range=[0, 100], dtick=20),
        yaxis=dict(dtick=1),
    )
    st.plotly_chart(plotly_base(fig, 430), use_container_width=True)

st.markdown("### Capability ledger")
df = pd.DataFrame([
    {"Skill": g["skill"], "Current": g["current"], "Target": g["target"], "Gap": g["gap"], "Weight": g["weight"], "Priority": g["priority"], "Confidence": f"{g['confidence']*100:.0f}%"}
    for g in gaps
])
st.dataframe(df, use_container_width=True, hide_index=True)
