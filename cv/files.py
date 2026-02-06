# Copyright (c) RenChu Wang - All Rights Reserved

import json
from pathlib import Path
from typing import Any

from jinja2 import Environment, FileSystemLoader, Template, meta

__all__ = ["ROOT", "get_template", "find_template_vars", "get_data"]

ROOT = Path(__file__).parent.parent.absolute()
"Project root."

SOURCE = ROOT / "templates"
"The source directory."

BUILD = ROOT / "build"
"The build directory."


def env():
    return Environment(loader=FileSystemLoader(SOURCE))


def get_template(name: str) -> Template:
    "Get the jinja template."

    j2 = f"{name}.html.j2"
    template = SOURCE / j2

    if not template.exists():
        raise FileNotFoundError(f"The file {name} is not found at {SOURCE}")

    return env().get_template(name=j2)


def find_template_vars(name: str) -> set[str]:
    "Find the variables from a jinja template."

    j2 = f"{name}.html.j2"
    template = SOURCE / j2
    parsed = env().parse(template.read_text())
    return meta.find_undeclared_variables(parsed)


def get_data(name: str) -> dict[str, Any]:
    "Get the json config data."

    file = SOURCE / f"{name}.json"
    result = json.loads(file.read_text())
    assert isinstance(result, dict)
    return result
