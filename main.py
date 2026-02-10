# Copyright (c) RenChu Wang - All Rights Reserved


import shutil
from typing import Any

import hydra
import rich

from cv import Section, files, resumes


def main(cfg: dict[str, Any]) -> None:
    sections = cfg["sections"]

    out = resumes.resume(Section(sec) for sec in sections)

    # Write output.
    output_and_print(out)


def output_and_print(out: str) -> None:
    files.BUILD.mkdir(exist_ok=True)
    with (files.BUILD / "index.html").open("w+") as f:
        print(out, file=f)

    shutil.copy2(files.TEMPLATE / "resume.css", files.BUILD)

    rich.print(out)


if __name__ == "__main__":
    main()
