# Copyright (c) RenChu Wang - All Rights Reserved

import dataclasses as dcls

from . import files
from .resumes import Section


@dcls.dataclass(frozen=True)
class Project:
    title: str
    date: str
    bullets: list[str]


def _projects():
    yield Project(
        title="BoCoEL - 10x faster LLM evaluation with Bayesian optimization and NLP",
        date="Jan 2024",
        bullets=[
            "Creator and lead developer; 200+ GitHub stars.",
            "Designed Bayesian optimization algorithm accelerating LLM benchmarking 10x via dense retrieval and embedding search.",
        ],
    )

    yield Project(
        title="Tula - stock allocation advisor powered by explainable AI LLM agents",
        date="Oct 2022",
        bullets=[
            "Led a team of 4 to win 1st place out of 1500 participants in BlackRock's event.",
            "Designed fintech ML models for transparent NLP-based financial decisions.",
            "Built backend for volatility index and portfolio aggregation.",
        ],
    )

    yield Project(
        title="Koila - ML library for solving CUDA (GPU) issues in 1 line",
        date="Nov 2021",
        bullets=[
            "Creator and lead developer; 1800+ stars and 50+ forks.",
            "Uses lazy evaluation to solve out-of-memory errors in PyTorch with a minimal API.",
            "Supports CNN, GNN, RNN, Linear layers, and arbitrary PyTorch ops.",
        ],
    )


def projects():
    body = files.get_template("projects").render(projects=_projects())
    return Section(name="projects", body=body)
