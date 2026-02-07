# Copyright (c) RenChu Wang - All Rights Reserved


import shutil

import hydra
import rich

from cv import contacts, educations, files, positions, projects, resumes, skills


@hydra.main(
    config_path="conf",
    config_name="main",
    version_base=None,
)
def main(cfg) -> None:
    sections = [
        contacts.contacts(),
        educations.educations(),
        positions.positions(),
        projects.projects(),
        skills.skills(),
    ]

    out = resumes.resume(sections)

    # Write output.
    output_and_print(out)


def output_and_print(out: str) -> None:
    files.BUILD.mkdir(exist_ok=True)
    with (files.BUILD / "index.html").open("w+") as f:
        print(out, file=f)

    shutil.copy2(files.SOURCE / "resume.css", files.BUILD)

    rich.print(out)


if __name__ == "__main__":
    main()
