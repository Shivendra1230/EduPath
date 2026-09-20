from core.competency import compute_gaps, readiness, critical_path, matched_resources
from core.llm import groq_service

PROFILE_SYSTEM = """You are EduPath's Evidence Analyst agent.
Analyze learner evidence conservatively. Extract only information supported by the text.
Do not equate a keyword with mastery. Return JSON with:
name, summary, experience, projects, skills_evidence (object mapping skill to evidence strings).
"""


def _trace(state, agent, action, status="complete"):
    trace = state.get("agent_trace", [])
    trace.append({"agent": agent, "action": action, "status": status})
    state["agent_trace"] = trace
    state["trace"] = state.get("trace", []) + [f"{agent}: {action}"]


def _slug(value):
    return value.lower().replace(" ", "_").replace("/", "_").replace("-", "_")


def profile_node(state):
    text = state.get("document_text", "")
    profile = {"name": "Learner", "summary": "", "experience": "", "projects": [], "skills_evidence": {}}
    if groq_service.live and text:
        try:
            profile = groq_service.json(
                PROFILE_SYSTEM,
                f"Role: {state.get('target_role')}\nEvidence:\n{text[:18000]}",
                groq_service.reasoning_model,
            )
        except Exception as exc:
            state["agent_warning"] = f"Evidence Analyst fallback: {type(exc).__name__}"
    state["profile"] = profile
    _trace(state, "Evidence Analyst", "Extracted grounded skills, projects and experience")
    return state


def gap_node(state):
    gaps = compute_gaps(
        state.get("document_text", ""),
        state.get("target_role", "AI/ML Engineer"),
        state.get("job_description", ""),
    )
    state["gaps"] = gaps
    state["readiness"] = readiness(gaps)
    state["critical_path"] = critical_path(gaps, state.get("target_role", "AI/ML Engineer"))
    _trace(state, "Competency Mapper", "Converted evidence into weighted capability gaps and dependencies")
    return state


def resource_node(state):
    resources = matched_resources(state.get("gaps", []))
    state["resources"] = resources
    _trace(state, "Resource Curator", f"Selected {len(resources)} gap-linked resources")
    return state


def plan_node(state):
    hours = max(1, float(state.get("weekly_hours", 7)))
    resources = state.get("resources", [])
    gaps = [g for g in state.get("gaps", []) if g["gap"] > 0][:6]
    per = max(45, int(hours * 60 / max(len(gaps), 1)))
    objectives = []
    for g in gaps:
        linked = [r for r in resources if g["skill"] in r["skills"]][:2]
        objectives.append({
            "id": _slug(g["skill"]),
            "skill": g["skill"],
            "title": f"Build evidence in {g['skill']}",
            "minutes": min(120, per),
            "outcome": f"Move from {g['current']}/5 toward {g['target']}/5 with a demonstrable artifact.",
            "success": ["Explain the concept without notes", "Complete a practical artifact", "Pass a self-check and explain trade-offs"],
            "resources": linked,
        })
    state["objectives"] = objectives
    _trace(state, "Learning Planner", "Built a time-boxed path ordered by dependency and priority")
    return state


def practice_node(state):
    """Generate distinct, skill-specific proof missions rather than one template repeated for every gap."""
    gaps = [g for g in state.get("gaps", []) if g["gap"] > 0][:6]
    role = state.get("target_role", "AI/ML Engineer")
    fallback = []
    archetypes = [
        ("Build Sprint", "Build a small working implementation that uses the skill in a realistic product scenario.",
         ["Create the smallest working version", "Add one meaningful edge case", "Explain one engineering trade-off"]),
        ("Debug Lab", "Diagnose a deliberately imperfect implementation and improve it using the target skill.",
         ["Identify the root cause", "Implement and verify a fix", "Document why the original approach failed"]),
        ("Design Review", "Design a production-oriented solution and defend the most important technical choices.",
         ["Draw the architecture or workflow", "Choose one implementation strategy", "Defend latency, quality, cost, or reliability trade-offs"]),
        ("Evaluation Lab", "Create a small experiment that measures whether the skill is working correctly.",
         ["Define a measurable success criterion", "Run at least two meaningful cases", "Interpret the result and propose the next experiment"]),
        ("Portfolio Upgrade", "Turn the skill into a portfolio-ready feature inside an existing project.",
         ["Add the feature end-to-end", "Write a concise README section", "Explain the business and technical value"]),
        ("Interview-to-Code", "Solve a realistic interview-style problem and then improve the first solution.",
         ["Explain the approach before coding", "Produce a working solution", "Discuss complexity and one improvement"]),
    ]
    for idx, g in enumerate(gaps):
        archetype, mission, checks = archetypes[idx % len(archetypes)]
        fallback.append({
            "id": f"{_slug(g['skill'])}_{idx+1}",
            "skill": g["skill"],
            "title": f"{g['skill']} — {archetype}",
            "difficulty": "Beginner" if g["current"] <= 1 else "Intermediate" if g["current"] <= 3 else "Advanced",
            "minutes": 60 if g["current"] <= 2 else 90,
            "mission": mission,
            "context": f"You are preparing for a {role} role. Your current evidence suggests {g['skill']} is a meaningful gap.",
            "deliverable": f"A concrete artifact or experiment proving you can apply {g['skill']}.",
            "steps": [f"Define the goal for {g['skill']}", "Build or analyze the smallest useful version", "Test it with one realistic case", "Write down what you learned"],
            "checks": checks,
            "hint": f"Start from the smallest example you can explain completely, then add complexity.",
            "common_mistakes": ["Jumping into implementation without defining success", "Copying a tutorial without changing the requirements", "Ignoring failure cases"],
        })

    state["practice"] = fallback
    if groq_service.live and gaps:
        try:
            data = groq_service.json(
                """You are EduPath's Practice Designer. Create 5-6 DISTINCT hands-on missions for a learner's actual skill gaps.
Return JSON: {\"missions\":[...]}. Each mission must contain:
 id, skill, title, difficulty, minutes, mission, context, deliverable, steps (4 items), checks (3 items), hint, common_mistakes (3 items).
Do NOT use generic wording like 'Small portfolio artifact'. Every mission must be materially different: vary build/debug/design/evaluation/project/interview formats.
Tie each mission to the exact gap, learner level and target role. Make tasks achievable within the stated minutes and specific enough to start immediately.""",
                f"Target role: {role}\nWeekly hours: {state.get('weekly_hours', 7)}\nGaps: {gaps}\nExisting projects/evidence: {state.get('profile', {}).get('projects', [])}",
                groq_service.reasoning_model,
                4200,
            )
            missions = data.get("missions", [])
            if isinstance(missions, list) and len(missions) >= 3:
                # Defensive normalization: keep only complete, non-duplicate missions.
                clean, seen = [], set()
                for m in missions:
                    if not isinstance(m, dict) or not m.get("skill") or not m.get("title"):
                        continue
                    key = (str(m.get("skill")).lower(), str(m.get("title")).lower())
                    if key in seen:
                        continue
                    seen.add(key)
                    m.setdefault("steps", [])
                    m.setdefault("checks", [])
                    m.setdefault("common_mistakes", [])
                    m.setdefault("hint", "Start with the smallest working example you can explain.")
                    clean.append(m)
                if clean:
                    state["practice"] = clean[:6]
        except Exception as exc:
            state["agent_warning"] = state.get("agent_warning", "") + f" Practice Designer fallback: {type(exc).__name__}"
    _trace(state, "Practice Designer", f"Generated {len(state['practice'])} distinct skill-specific proof missions")
    return state


def interview_node(state):
    gaps = [g for g in state.get("gaps", []) if g["gap"] > 0][:6]
    role = state.get("target_role", "AI/ML Engineer")
    fallback = [{
        "question": f"Explain {g['skill']} in the context of a {role} system. What would you choose and why?",
        "skill": g["skill"],
        "difficulty": "Intermediate" if g["current"] >= 2 else "Beginner",
        "why_asked": f"Your evidence shows a {g['skill']} gap, so an interviewer may use this to test whether you can move beyond definitions into practical reasoning.",
        "what_interviewer_tests": [f"Conceptual understanding of {g['skill']}", "Ability to connect the concept to a real system", "Ability to justify a trade-off"],
        "explanation": f"The question is really asking: can you explain {g['skill']}, show where it fits in a real system, and defend one technical decision?",
        "answer": f"Start by defining {g['skill']} in one or two sentences. Then describe the workflow, give one concrete example, state your choice, and finish with one trade-off.",
        "answer_framework": ["Define it", "Explain the workflow", "Give a concrete example", "State a trade-off", "Mention how you would validate it"],
        "hint": f"Do not start with a long definition. Anchor {g['skill']} to a project or system you understand.",
        "common_mistakes": ["Giving only a textbook definition", "Using unexplained jargon", "Ignoring trade-offs or validation"],
        "follow_up": f"How would you test or monitor your {g['skill']} implementation?",
    } for g in gaps]
    state["interview"] = fallback
    if groq_service.live and gaps:
        try:
            data = groq_service.json(
                """You are EduPath's Senior Interview Coach.
Return JSON {\"questions\":[...]} with exactly 5 high-quality questions.
Questions MUST be specific to the candidate's target role, evidence and current skill gaps; do not produce generic filler.
Each item MUST contain:
question, skill, difficulty, why_asked, what_interviewer_tests (3 bullets), explanation, answer, answer_framework (4-6 steps), hint, common_mistakes (3 bullets), follow_up.
The explanation must proactively decode what the interviewer is actually asking in simple language.
The model answer must be technically substantive but appropriate to the learner's level. If the candidate's evidence suggests a topic is weak, teach the missing concept briefly inside the answer instead of pretending mastery.
Mix conceptual, practical, debugging/system-design, trade-off and scenario questions. Avoid repeating the same sentence pattern across questions.""",
                f"Target role: {role}\nCareer goal: {state.get('career_goal')}\nLearner evidence/profile: {state.get('profile', {})}\nCurrent gaps: {gaps}\nProjects: {state.get('profile', {}).get('projects', [])}",
                groq_service.reasoning_model,
                5200,
            )
            questions = data.get("questions", [])
            if isinstance(questions, list) and len(questions) >= 3:
                clean, seen = [], set()
                for q in questions:
                    if not isinstance(q, dict) or not q.get("question"):
                        continue
                    key = str(q["question"]).strip().lower()
                    if key in seen:
                        continue
                    seen.add(key)
                    q.setdefault("explanation", "This question checks whether you can explain the concept and apply it.")
                    q.setdefault("why_asked", "It is linked to one of your current skill gaps.")
                    q.setdefault("what_interviewer_tests", [])
                    q.setdefault("answer_framework", [])
                    q.setdefault("hint", "Start with the simplest correct explanation, then give an example.")
                    q.setdefault("common_mistakes", [])
                    q.setdefault("follow_up", "What trade-off would you consider in production?")
                    clean.append(q)
                if clean:
                    state["interview"] = clean[:5]
        except Exception as exc:
            state["agent_warning"] = state.get("agent_warning", "") + f" Interview Coach fallback: {type(exc).__name__}"
    _trace(state, "Interview Coach", f"Generated {len(state['interview'])} gap-linked interview probes with explanations and doubt support")
    return state


def critic_node(state):
    gaps = state.get("gaps", [])
    objectives = state.get("objectives", [])
    issues = []
    if not gaps:
        issues.append("No competency signals were produced")
    if gaps and not objectives:
        issues.append("No learning objectives were produced")
    if any(g.get("gap", 0) > 0 and not g.get("rationale") for g in gaps):
        issues.append("A gap is missing rationale")
    state["quality_check"] = {"status": "PASS" if not issues else "REVIEW", "issues": issues}
    _trace(state, "Quality Critic", "Validated evidence → gaps → plan consistency")
    return state


def analyze_graph(graph, state):
    return graph.invoke(state)
