# Copyright (c) RenChu Wang - All Rights Reserved

import dataclasses as dcls
import functools
import re
import typing
from collections.abc import Iterable, Mapping, Sequence
from pathlib import Path
from typing import Any

from jinja2 import Environment, FileSystemLoader, Template, meta
from markdown_it import MarkdownIt
from omegaconf import OmegaConf

__all__ = [
    "ROOT",
    "get_template",
    "find_template_vars",
    "get_data",
    "MarkdownRender",
]

ROOT = Path(__file__).parent.parent.absolute()
"Project root."

TEMPLATE = ROOT / "templates"
"The tempalate directory."

DATA = ROOT / "data"
"The data directory."

BUILD = ROOT / "build"
"The build directory."


@dcls.dataclass
class MarkdownRender:
    class IsRendered(str):
        "A 'tag' s.t. we know that the item is already processed. ``str`` subclass."

    template: Template
    """
    The jinja template to fill.
    """

    keywords: Sequence[str] = ()
    """
    The keywords to be marked in bold.
    """

    def render(self, **kwargs):
        kwargs = self._render(kwargs)
        return self.template.render(**kwargs)

    @typing.no_type_check
    def _render(self, obj: Any) -> Any:
        # Skip any rendering if it's already previously rendered.
        if isinstance(obj, self.IsRendered):
            return obj

        if isinstance(obj, str):
            obj = self._mark_keywords_bold(obj)
            obj = self._md.renderInline(obj)
            return self.IsRendered(obj)

        if isinstance(obj, Mapping):
            return {key: self._render(val) for key, val in obj.items()}

        if isinstance(obj, Iterable):
            return [self._render(val) for val in obj]

        # Do not recurse into custom objects.
        return obj

    @functools.cached_property
    def _md(self):
        return MarkdownIt()

    @functools.cached_property
    def _compile_keywords(self):
        escaped = [re.escape(kw) for kw in self.keywords]
        captured = [f"({e})" for e in escaped]
        return [re.compile(r, flags=re.IGNORECASE) for r in captured]

    def _mark_keywords_bold(self, text: str):
        for pattern in self._compile_keywords:
            text = pattern.sub(r"**\1**", text)
        assert isinstance(text, str), text
        return text


def env():
    return Environment(loader=FileSystemLoader(TEMPLATE))


def get_template(name: str, /, keywords: Sequence[str] = ()):
    "Get the jinja template."

    j2 = f"{name}.html.j2"
    template = TEMPLATE / j2

    if not template.exists():
        raise FileNotFoundError(f"The file {name} is not found at {TEMPLATE}")

    return MarkdownRender(template=env().get_template(name=j2), keywords=keywords)


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
