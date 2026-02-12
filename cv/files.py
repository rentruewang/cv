# Copyright (c) RenChu Wang - All Rights Reserved

import dataclasses as dcls
import functools
import typing
from collections.abc import Iterable, Mapping
from pathlib import Path
from typing import Any

from jinja2 import Environment, FileSystemLoader, Template, meta
from markdown_it import MarkdownIt
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


class _Rendered(str):
    "A 'tag' s.t. we know that the item is already processed. ``str`` subclass."


@dcls.dataclass
class MarkdownRender:
    template: Template

    def render(self, **kwargs):
        kwargs = self._render(kwargs)
        return self.template.render(**kwargs)

    @typing.no_type_check
    def _render(self, obj: Any) -> Any:
        match obj:

            case None | int() | float() | bool():
                return obj

            # Skip any rendering if it's already previously rendered.
            case _Rendered(item):
                return item

            case str():
                return _Rendered(self._md.renderInline(obj))

            case Mapping():
                return {key: self._render(val) for key, val in obj.items()}

            case Iterable():
                return [self._render(val) for val in obj]

            # Do not recurse into custom objects.
            case _:
                return obj

    @functools.cached_property
    def _md(self):
        return MarkdownIt()


def env():
    return Environment(loader=FileSystemLoader(TEMPLATE))


def get_template(name: str):
    "Get the jinja template."

    j2 = f"{name}.html.j2"
    template = TEMPLATE / j2

    if not template.exists():
        raise FileNotFoundError(f"The file {name} is not found at {TEMPLATE}")

    return MarkdownRender(env().get_template(name=j2))


def find_template_vars(name: str) -> set[str]:
    "Find the variables from a jinja template."

    j2 = f"{name}.html.j2"
    template = TEMPLATE / j2
    parsed = env().parse(template.read_text())
    return meta.find_undeclared_variables(parsed)


def get_data(name: str) -> Mapping[str, Any]:
    "Get the json config data."

    file = DATA / f"{name}.yaml"

    with open(file) as f:
        result = OmegaConf.load(f)

    assert isinstance(result, Mapping)
    return result
