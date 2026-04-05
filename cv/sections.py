# Copyright (c) RenChu Wang - All Rights Reserved

import dataclasses as dcls
import functools
import typing
from collections import abc as cabc

from .files import get_data, get_template

__all__ = ["Body", "Section", "SectionContent"]


@dcls.dataclass(frozen=True)
class Body:
    name: str
    data: dict[str, object]
    keywords: list[str]

    def render(self) -> str:
        return self._template.render(**self.data)

    @functools.cached_property
    def _template(self):
        return get_template(self.name, keywords=self.keywords)


@dcls.dataclass(frozen=True)
class Section:
    keywords: list[str]
    "Keywords to highlight."

    cfg: str
    "The configuration file location."

    def render(self) -> str:
        return self._template.render(section=self.section)

    @functools.cached_property
    def cfg_data(self) -> cabc.Mapping[str, typing.Any]:
        return get_data(self.cfg)

    @property
    def name(self) -> str:
        return self.cfg_data["name"]

    @property
    def hidden_msg(self) -> str:
        return self.cfg_data.get("hidden", "")

    @property
    def title(self) -> str:
        return self.cfg_data.get("title", "")

    @functools.cached_property
    def body(self) -> Body:
        return Body(name=self.name, data=self.cfg_data["body"], keywords=self.keywords)

    @functools.cached_property
    def _template(self):
        return get_template("sections")

    @property
    def section(self):
        return SectionContent(
            name=self.name,
            title=self.title,
            body=self.body.render(),
        )


@dcls.dataclass(frozen=True)
class SectionContent:
    name: str
    title: str
    body: str
