from typing import Any, Dict, List, TypedDict

class EduPathState(TypedDict, total=False):
    document_text: str
    document_name: str
    target_role: str
    career_goal: str
    current_skills: str
    experience: str
    job_description: str
    weekly_hours: float
    profile: Dict[str, Any]
    gaps: List[Dict[str, Any]]
    resources: List[Dict[str, Any]]
    objectives: List[Dict[str, Any]]
    practice: List[Dict[str, Any]]
    interview: List[Dict[str, Any]]
    readiness: int
    critical_path: List[str]
    feedback: str
    progress: Dict[str, Any]
    coach_history: List[Dict[str, str]]
    coach_answer: str
    coach_route: str
    trace: List[str]
    agent_trace: List[Dict[str, Any]]
    quality_check: Dict[str, Any]
    agent_warning: str
