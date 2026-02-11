# Copyright (c) RenChu Wang - All Rights Reserved

import dataclasses as dcls
import shutil
import typing
from argparse import ArgumentParser
from pathlib import Path

import rich
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

    for injection in flags["injection"]:
        gc = GenerationConfig(
            sections=flags["sections"],
            hide=injection["hide"],
            to=injection["to"],
        )
        generate_resume(gc)

    files.BUILD.mkdir(exist_ok=True)
    _ = shutil.copy2(files.TEMPLATE / "resume.css", files.BUILD)


def generate_resume(cfg: GenerationConfig, /):
    out = resumes.resume(Section(sec) for sec in cfg.sections)
    tee(out, file="index.html")


def tee(out: str, file: str) -> None:
    rich.print(out)
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
