# Copyright (c) RenChu Wang - All Rights Reserved

import dataclasses as dcls


@dcls.dataclass(frozen=True)
class Skill:
    category: str
    items: list[str]

    @property
    def items_str(self):
        return ", ".join(map(str.strip, self.items))


def skills():
    yield Skill(
        category="Programming",
        items=[
            "Python",
            "Modern C++",
            "Go",
            "Java",
            "JavaScript",
            "Dart",
        ],
    )
    yield Skill(
        category="Machine Learning",
        items=[
            "NumPy",
            "PyTorch",
            "Pandas",
            "TF",
            "Keras",
            "Spark",
            "BoTorch",
            "GPyTorch",
            "Ax",
        ],
    )
    yield Skill(
        category="Platforms",
        items=["Azure", " AWS", " Google Cloud", " Databricks", " Docker"],
    )
    yield Skill(
        category="Tools",
        items=[
            "Linux",
            "SQL",
            "Flask",
            "Django",
            "D3.js",
            "Git",
        ],
    )
