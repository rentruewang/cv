# Copyright (c) RenChu Wang - All Rights Reserved

from collections.abc import Mapping
from pathlib import Path
from typing import Any

from jinja2 import Environment, FileSystemLoader, Template, meta
from omegaconf import OmegaConf

__all__ = ["ROOT", "get_template", "find_template_vars", "get_data"]

ROOT = Path(__file__).parent.parent.absolute()
"Project root."

TEMPLATE = ROOT / "templates"
"The tempalate directory."

DATA = ROOT / "data"
"The data directory."

BUILD = ROOT / "build"
"The build directory."


def env():
    return Environment(loader=FileSystemLoader(TEMPLATE))


def get_template(name: str) -> Template:
    "Get the jinja template."

    j2 = f"{name}.html.j2"
    template = TEMPLATE / j2

    if not template.exists():
        raise FileNotFoundError(f"The file {name} is not found at {TEMPLATE}")

    return env().get_template(name=j2)


def find_template_vars(name: str) -> set[str]:
    "Find the variables from a jinja template."

    j2 = f"{name}.html.j2"
    template = TEMPLATE / j2
    parsed = env().parse(template.read_text())
    return meta.find_undeclared_variables(parsed)


def get_data(name: str) -> dict[str, Any]:
    "Get the json config data."

    file = DATA / f"{name}.yaml"

    with open(file) as f:
        result = OmegaConf.load(f)

    assert isinstance(result, Mapping)
    return result
