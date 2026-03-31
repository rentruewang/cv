# Copyright (c) RenChu Wang - All Rights Reserved

import dataclasses as dcls
import functools
import pathlib
import re
import typing
from collections import abc as cabc

import jinja2 as j2
import markdown_it
import omegaconf as oc
from jinja2 import meta

__all__ = [
    "ROOT",
    "get_template",
    "find_template_vars",
    "get_data",
    "MarkdownRender",
]

ROOT = pathlib.Path(__file__).parent.parent.absolute()
"Project root."

TEMPLATE = ROOT / "templates"
"The tempalate directory."

DATA = ROOT / "data"
"The data directory."

BUILD = ROOT / "build"
"The build directory."


class _IsRendered(str):
    "A 'tag' s.t. we know that the item is already processed. ``str`` subclass."


@dcls.dataclass
class MarkdownRender:

    template: j2.Template
    """
    The jinja template to fill.
    """

    keywords: cabc.Sequence[str] = ()
    """
    The keywords to be marked in bold.
    """

    def render(self, **kwargs):
        kwargs = self._render(kwargs)
        return self.template.render(**kwargs)

    @typing.no_type_check
    def _render(self, obj: typing.Any) -> typing.Any:
        match obj:
            # Skip any rendering if it's already previously rendered.
            case _IsRendered():
                return obj

            case str():
                obj = self._maybe_mark_keywords_bold(obj)
                obj = self._md.renderInline(obj)
                return _IsRendered(obj)

            case cabc.Mapping():
                return {key: self._render(val) for key, val in obj.items()}

            case cabc.Iterable():
                return [self._render(val) for val in obj]

            # Do not recurse into custom objects or primitives.
            case _:
                return obj

    @functools.cached_property
    def _md(self):
        return markdown_it.MarkdownIt()

    def _maybe_mark_keywords_bold(self, text: str) -> str:
        "Mark the keywords bold. Skip link."

        if _is_link(text):
            return text

        text = _highlight_keywords(text, self.keywords)
        assert isinstance(text, str), text
        return text


_LINK_REGEX = re.compile(r"(?:__|[*#])|\[(.*?)\]\(.*?\)")
_WS_FRONT = r"(?<!\w)"
_WS_BACK = r"(?!\w)"


def _is_link(link: str):
    return _LINK_REGEX.match(link) is not None


@functools.cache
def _isolated_keyword(kw: str):
    kw = _WS_FRONT + "(" + kw + ")" + _WS_BACK
    return re.compile(kw, flags=re.IGNORECASE)


def _highlight_keywords(text: str, keywords: cabc.Sequence[str]) -> str:
    for kw in keywords:
        pattern = _isolated_keyword(kw)
        text = pattern.sub(r"**\1**", text)
    return text


def env():
    return j2.Environment(loader=j2.FileSystemLoader(TEMPLATE))


def get_template(name: str, /, keywords: cabc.Sequence[str] = ()):
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


def get_data(name: str) -> cabc.Mapping[str, typing.Any]:
    "Get the json config data."

    file = DATA / f"{name}.yaml"

    with open(file) as f:
        result = oc.OmegaConf.load(f)

    assert isinstance(result, cabc.Mapping)
    return result
