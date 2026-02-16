# Copyright (c) RenChu Wang - All Rights Reserved

import dataclasses as dcls
import shutil
import typing
from argparse import ArgumentParser
from pathlib import Path

from omegaconf import OmegaConf

from cv import Section, files, resumes


@dcls.dataclass(frozen=True)
class GenerationConfig:
    sections: list[str]
    keywords: list[str]


@typing.no_type_check
def main(cfg: Path) -> None:
    assert cfg.exists() and cfg.is_file()
    flags = dict(OmegaConf.load(cfg))

    # Make directory
    files.BUILD.mkdir(exist_ok=True)
    if not (gitignore := files.BUILD / ".gitignore").exists():
        gitignore.write_text("*")

    # Copy CSS.
    _ = shutil.copy2(files.TEMPLATE / "resume.css", files.BUILD)

    gc = GenerationConfig(
        sections=flags["sections"],
        keywords=flags["keywords"],
    )
    generate_resume(gc)


def generate_resume(cfg: GenerationConfig, /):
    sections = [Section(cfg=sec, keywords=cfg.keywords) for sec in cfg.sections]
    out = resumes.resume(sections=sections)
    with (files.BUILD / "index.html").open("w+") as f:
        _ = f.write(out)


if __name__ == "__main__":
    CWD = Path(__file__).parent
    parser = ArgumentParser()
    _ = parser.add_argument(
        "--cfg",
        type=Path,
        default=CWD / "config.yaml",
    )
    flags = vars(parser.parse_args())
    main(**flags)
