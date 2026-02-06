# Copyright (c) RenChu Wang - All Rights Reserved

import dataclasses as dcls
import functools
from typing import Any

from jinja2 import Template

from . import files


@dcls.dataclass(frozen=True)
class Renderer:
    template: str
    """
    The template name to receive.
    """

    data: str
    """
    The data to fill in.
    """

    def __post_init__(self) -> None:
        variables = files.find_template_vars(self.template)

        if diff := variables.difference(self.loaded_data.keys()):
            raise KeyError(f"Missing keys: {diff} in data.")

    def render(self) -> str:
        return files.get_template(self.template).render(**self.loaded_data)

    @functools.cached_property
    def loaded_data(self) -> dict[str, Any]:
        return files.get_data(self.data)
