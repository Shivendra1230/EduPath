import streamlit as st
from ui import hero
from core.llm import groq_service
from agents.analyze import interview_node

s = st.session_state.state
hero(
    "08 · INTERVIEW COACH",
    "Practice the questions your gaps create.",
    "EduPath does more than reveal the answer. It explains what the interviewer is testing, how to structure your response, common mistakes, and how to recover when you get stuck.",
)

c1, c2 = st.columns([1, 2])
with c1:
    if st.button("↻ Generate fresh interview set", type="primary"):
        with st.spinner("Interview Coach is creating a new role-specific set…"):
            s = interview_node(s)
            st.session_state.state = s
        st.rerun()
with c2:
    if s.get("agent_warning"):
        st.caption("Some generation steps used a deterministic fallback. Reconnect Groq and regenerate for a fresh model-generated set.")

if not s.get("interview"):
    st.info("Analyze a learner profile first.")
    st.stop()

for i, q in enumerate(s["interview"], 1):
    question = q.get("question", "Question")
    difficulty = q.get("difficulty", "Intermediate")
    skill = q.get("skill", "—")
    with st.expander(f"{i}. {question} · {difficulty}"):
        st.caption(f"Skill gap: {skill}")

        st.markdown("### 🧠 What is this question really asking?")
        st.info(q.get("explanation", "Break the question into concept → application → reasoning."))

        st.markdown("### 🎯 Why the interviewer may ask it")
        st.write(q.get("why_asked", "It is linked to your current target-role gap."))

        tests = q.get("what_interviewer_tests", [])
        if tests:
            st.markdown("### 🔍 What they are testing")
            for item in tests:
                st.write("•", item)

        st.markdown("### 🧩 How to structure your answer")
        framework = q.get("answer_framework", [])
        if framework:
            for idx, item in enumerate(framework, 1):
                st.write(f"**{idx}.** {item}")
        else:
            st.write("Define → explain the workflow → give an example → discuss a trade-off → validate.")

        st.markdown("### 💡 Hint if you get stuck")
        st.warning(q.get("hint", "Start with the simplest correct explanation and connect it to a project."))

        st.markdown("### ✅ Model answer")
        st.write(q.get("answer", q.get("model_answer", "")))

        mistakes = q.get("common_mistakes", [])
        if mistakes:
            st.markdown("### ⚠️ Avoid these mistakes")
            for item in mistakes:
                st.write("•", item)

        st.markdown("### 🔁 Follow-up")
        st.write(q.get("follow_up", "How would you validate this in production?"))

        st.markdown("### 🗣️ Clear your doubt")
        doubt_key = f"doubt_{i}_{skill}"
        doubt = st.text_area(
            "Ask EduPath about this question, your approach, or a confusing concept.",
            key=doubt_key,
            height=90,
            placeholder="e.g. I don't understand what trade-off means here…",
        )
        if st.button("Explain my doubt", key=f"explain_{i}"):
            if not doubt.strip():
                st.warning("Type the doubt first.")
            elif not groq_service.live:
                st.error("Groq is not connected. Add GROQ_API_KEY in deployment secrets.")
            else:
                prompt = f"""You are EduPath's interview tutor. The learner is preparing for {s.get('target_role')}.
Question: {question}
Skill: {skill}
Their doubt: {doubt}

Explain the doubt step-by-step in simple language. Correct any misconception. Give one tiny example, then tell the learner how they should answer the original interview question. Do not be generic."""
                with st.spinner("Coach is clearing the doubt…"):
                    try:
                        answer = groq_service.chat(
                            "You are a patient senior technical interviewer and teacher. Be concrete, proactive and concise.",
                            prompt,
                            groq_service.reasoning_model,
                            0.25,
                            1800,
                        )
                        st.success(answer)
                    except Exception as exc:
                        st.error(f"Could not generate the explanation: {exc}")
