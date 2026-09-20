from langgraph.graph import StateGraph, START, END
from models.state import EduPathState
from agents.analyze import (
    profile_node,
    gap_node,
    resource_node,
    plan_node,
    practice_node,
    interview_node,
    critic_node,
)


def build_analysis_graph():
    """Production analysis supervisor: specialized agents hand off state in sequence."""
    g = StateGraph(EduPathState)
    g.add_node("evidence_analyst", profile_node)
    g.add_node("competency_mapper", gap_node)
    g.add_node("resource_curator", resource_node)
    g.add_node("learning_planner", plan_node)
    g.add_node("practice_designer", practice_node)
    g.add_node("interview_coach", interview_node)
    g.add_node("quality_critic", critic_node)

    g.add_edge(START, "evidence_analyst")
    g.add_edge("evidence_analyst", "competency_mapper")
    g.add_edge("competency_mapper", "resource_curator")
    g.add_edge("resource_curator", "learning_planner")
    g.add_edge("learning_planner", "practice_designer")
    g.add_edge("practice_designer", "interview_coach")
    g.add_edge("interview_coach", "quality_critic")
    g.add_edge("quality_critic", END)
    return g.compile()
