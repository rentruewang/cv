# Copyright (c) RenChu Wang - All Rights Reserved

import dataclasses as dcls
import functools
from collections.abc import Mapping
from typing import Any

from . import files

__all__ = ["Section"]


@dcls.dataclass(frozen=True)
class Section:
    cfg: str

    def render(self):
        return files.get_template("sections").render(section=self)

    @functools.cached_property
    def cfg_data(self) -> Mapping[str, Any]:
        return files.get_data(self.cfg)

    @property
    def title(self) -> str:
        return self.cfg_data.get("title", "")

    @property
    def name(self):
        return self.cfg_data["name"]

    @functools.cached_property
    def body(self):
        return files.get_template(self.name).render(**self.cfg_data["body"])
