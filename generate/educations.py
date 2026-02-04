# Copyright (c) RenChu Wang - All Rights Reserved

import dataclasses as dcls

from . import files
from .resumes import Section


@dcls.dataclass(frozen=True)
class Education:
    degree: str
    school: str
    start: str
    end: str
    courses: list[str]

    @property
    def courses_str(self):
        return ", ".join(map(str.strip, self.courses))


def _educations():
    yield Education(
        degree="MS CSE",
        school="Georgia Tech",
        start="Aug 2022",
        end="May 2024",
        courses=[
            "Probability for Sci./Eng.",
            "Knowledge-based AI",
            "Ubiquitous Computing",
            "High Perform Computing",
            "Modeling & Simulation",
            "Data Science for Social",
            "Computational Data Analysis",
            "Data Visual Analysis",
        ],
    )

    yield Education(
        degree="BS EE",
        school="National Taiwan Universtiy",
        start="Sep 2017",
        end="Jun 2021",
        courses=[
            "Algorithms",
            "Convex Optimization",
            "Machine Learning",
            "Linear Algebra",
            "Digital Speech Processing",
            "Data Structures",
            "Signal and Systems",
            "Computer Architecture",
            "Integrated Circuit Design",
            "Cloud Computing And Cyber Security",
        ],
    )


def educations():
    body = files.get_template("educations").render(educations=_educations())
    return Section(name="educations", body=body)
