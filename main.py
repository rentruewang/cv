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
    hide: bool
    to: str


@typing.no_type_check
def main(cfg: Path) -> None:
    assert cfg.exists() and cfg.is_file()
    flags = dict(OmegaConf.load(cfg))

    files.BUILD.mkdir(exist_ok=True)
    if not (gitignore := files.BUILD / ".gitignore").exists():
        gitignore.write_text("*")

    for injection in flags["injection"]:
        gc = GenerationConfig(
            sections=flags["sections"],
            hide=injection["hide"],
            to=injection["to"],
        )
        generate_resume(gc)
    _ = shutil.copy2(files.TEMPLATE / "resume.css", files.BUILD)


def generate_resume(cfg: GenerationConfig, /):
    out = resumes.resume(Section(sec, hide=cfg.hide) for sec in cfg.sections)
    tee(out, file=cfg.to)


def tee(out: str, file: str) -> None:
    with (files.BUILD / file).open("w+") as f:
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
