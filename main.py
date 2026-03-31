# Copyright (c) RenChu Wang - All Rights Reserved

import argparse
import contextlib as ctxl
import dataclasses as dcls
import pathlib
import shutil
import typing

import omegaconf as oc

from cv import files, resumes, sections


@ctxl.contextmanager
def log_stage(message: str):

    try:
        print(message, end="... ")
        yield
    except Exception as e:
        print(f"Failed with error: {e}")

    print("Done.")


@dcls.dataclass(frozen=True)
class GenerationConfig:
    sections: list[str]
    keywords: list[str]

    def generate(self):
        return generate_resume(self)


@typing.no_type_check
def main(cfg: pathlib.Path) -> None:
    assert cfg.exists() and cfg.is_file()
    flags = dict(oc.OmegaConf.load(cfg))

    # Make directory
    files.BUILD.mkdir(exist_ok=True)
    if not (gitignore := files.BUILD / ".gitignore").exists():
        gitignore.write_text("*")

    # Copy CSS.
    with log_stage(f"Copy CSS to template: {files.TEMPLATE}"):
        _ = shutil.copy2(files.TEMPLATE / "resume.css", files.BUILD)

    cfg = GenerationConfig(
        sections=flags["sections"],
        keywords=flags["keywords"],
    )
    cfg.generate()


def generate_resume(cfg: GenerationConfig, /):
    secs = [sections.Section(cfg=sec, keywords=cfg.keywords) for sec in cfg.sections]

    with log_stage("Generating resume"):
        out = resumes.resume(sections=secs)

    with (
        log_stage(f"Write file to index.html in build: {files.BUILD}"),
        (files.BUILD / "index.html").open("w+") as f,
    ):
        _ = f.write(out)


if __name__ == "__main__":
    CWD = pathlib.Path(__file__).parent
    parser = argparse.ArgumentParser()
    _ = parser.add_argument(
        "--cfg",
        type=pathlib.Path,
        default=CWD / "config.yaml",
    )
    flags = vars(parser.parse_args())
    main(**flags)
