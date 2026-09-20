import streamlit as st
from ui import hero
from core.llm import groq_service

s = st.session_state.state
hero(
    "06 · PRACTICE LAB",
    "Turn learning into proof.",
    "Every mission is different: build, debug, design, evaluate, upgrade or solve. EduPath gives you the context, steps, validation criteria and a proactive hint so you can start immediately.",
)

if not s.get("practice"):
    st.info("Analyze a learner profile first.")
    st.stop()

for i, p in enumerate(s["practice"], 1):
    pid = p.get("id", f"mission_{i}")
    with st.container(border=True):
        st.markdown(f"### {i}. {p.get('title', 'Practice mission')}")
        st.caption(f"{p.get('skill', 'Skill')} · {p.get('difficulty', 'Intermediate')} · {p.get('minutes', 60)} min")
        st.markdown(f"**Mission:** {p.get('mission', 'Apply the skill to a concrete problem.')}")
        if p.get("context"):
            st.markdown(f"**Context:** {p['context']}")
        st.markdown(f"**Deliverable:** {p.get('deliverable', 'A working artifact with evidence of your reasoning.')}")

        with st.expander("View mission plan", expanded=True):
            st.markdown("**Steps**")
            for n, step in enumerate(p.get("steps", []), 1):
                st.write(f"{n}. {step}")
            st.markdown("**Validation**")
            for item in p.get("checks", []):
                st.write("•", item)
            if p.get("hint"):
                st.info(f"💡 Proactive hint: {p['hint']}")
            mistakes = p.get("common_mistakes", [])
            if mistakes:
                st.markdown("**Common mistakes to avoid**")
                for item in mistakes:
                    st.write("•", item)

        if st.button("Open mission workspace", key=f"mission_{pid}"):
            st.session_state["active_mission"] = p

    if st.session_state.get("active_mission", {}).get("id") == pid:
        mission = st.session_state["active_mission"]
        st.markdown("#### 🧪 Mission workspace")
        st.info(mission.get("mission", "Start with the smallest working version."))

        if mission.get("steps"):
            st.markdown("**Do this now**")
            for step in mission["steps"]:
                st.write("☐", step)

        st.markdown("**Need help?**")
        help_text = st.text_area(
            "Tell EduPath what is blocking you and it will coach you without giving away the whole solution.",
            key=f"help_{pid}",
            height=90,
            placeholder="e.g. I don't know how to start the evaluation experiment…",
        )
        if st.button("Coach me", key=f"coach_{pid}"):
            if not help_text.strip():
                st.warning("Describe what is blocking you first.")
            elif not groq_service.live:
                st.error("Groq is not connected. Add GROQ_API_KEY in deployment secrets.")
            else:
                prompt = f"""You are EduPath's hands-on practice coach.
Target role: {s.get('target_role')}
Skill: {mission.get('skill')}
Mission: {mission.get('mission')}
Deliverable: {mission.get('deliverable')}
Learner blocker: {help_text}

Give a short diagnostic, one concrete next step, one small example if useful, and one question that checks understanding. Do not complete the whole mission for the learner."""
                with st.spinner("Practice Coach is diagnosing the blocker…"):
                    try:
                        answer = groq_service.chat(
                            "You are a proactive technical mentor. Coach the learner toward independent completion.",
                            prompt,
                            groq_service.reasoning_model,
                            0.25,
                            1600,
                        )
                        st.success(answer)
                    except Exception as exc:
                        st.error(f"Could not generate coaching: {exc}")
