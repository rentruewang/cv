# Copyright (c) RenChu Wang - All Rights Reserved

import dataclasses as dcls

from . import files
from .resumes import Section

__all__ = ["contacts"]


@dcls.dataclass(frozen=True)
class Contact:
    icon: str
    label: str
    href: str
    target: str | None = None


def _contacts():
    yield Contact(
        icon="fa-brands fa-github",
        label="/rentruewang",
        href="https://github.com/rentruewang",
        target="_blank",
    )
    yield Contact(
        icon="fa-solid fa-globe",
        label="cv.rentruewang.com",
        href="https://cv.rentruewang.com",
        target="_blank",
    )
    yield Contact(
        icon="fa-solid fa-phone",
        label="+1-669-237-2215",
        href="tel:+16692372215",
        target=None,
    )
    yield Contact(
        icon="fa-solid fa-envelope",
        label="renchuwang@gmail.com",
        href="mailto:renchuwang@gmail.com",
        target=None,
    )
    yield Contact(
        icon="fa-brands fa-linkedin",
        label="/rentruewang",
        href="https://linkedin.com/in/rentruewang",
        target="_blank",
    )


def contacts():
    body = files.get_template("contacts").render(contacts=_contacts())
    return Section(name="contacts", body=body)
