# Architecture

```text
                         ┌──────────────────────────┐
                         │       EduPath UI         │
                         │ Profile / Skills / Study │
                         │ Practice / Coach / Report│
                         └────────────┬─────────────┘
                                      │
                    ┌─────────────────┴─────────────────┐
                    │                                   │
             ANALYSIS GRAPH                       COACH GRAPH
                    │                                   │
          ┌─────────▼─────────┐               ┌────────▼────────┐
          │ Evidence Analyst  │               │ Intent Router   │
          └─────────┬─────────┘               └────────┬────────┘
                    ▼                                   ▼
          ┌───────────────────┐                ┌────────────────┐
          │ Competency Engine │                │ Groq Reasoning │
          └─────────┬─────────┘                │ Coach / Web*   │
                    ▼                          └────────────────┘
          ┌───────────────────┐
          │ Learning Planner  │
          └─────────┬─────────┘
                    ▼
          ┌───────────────────┐
          │ Interview Coach   │
          └─────────┬─────────┘
                    ▼
              Learner State
                    ▲
                    │
             Adaptive Replan
```

Deterministic competency logic controls the core learning decision. LLMs enrich evidence, generate explanations and interview content, and power open-ended coaching.
