# Copyright (c) RenChu Wang - All Rights Reserved

from pathlib import Path

from jinja2 import Environment, FileSystemLoader, Template

ROOT = Path(__file__).parent.parent.absolute()
"Project root."

SOURCE = ROOT / "templates"
"The source directory."

BUILD = ROOT / "build"
"The build directory."


def get_template(name: str) -> Template:
    """
    Get the jinja template.
    """

    j2 = f"{name}.html.j2"
    template = SOURCE / j2

    if not template.exists():
        raise FileNotFoundError(f"The file {name} is not found at {SOURCE}")

    env = Environment(loader=FileSystemLoader(SOURCE))
    return env.get_template(name=j2)
