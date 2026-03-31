# Copyright (c) RenChu Wang - All Rights Reserved

import dataclasses as dcls
import functools
import os

import nox


@nox.session
def build(session: nox.Session):
    "Nox `build` command. Calls `python main.py`."

    pdm(session).run("python", "main.py")


@nox.session
def pre_commit(session: nox.Session):
    "Runs the pre-commit commands."

    formatting(session)
    typing(session)


@nox.session
def formatting(session: nox.Session):
    "Nox `formatting` command. Calls `autoflake`, `isort`, `black`, in that order."
    autoflake(session)
    isort(session)
    black(session)


@nox.session
def autoflake(session: nox.Session):
    "Nox `autoflake` command. Calls `autoflake` command."
    pdm(session).run("autoflake", ".")


@nox.session
def isort(session: nox.Session):
    "Nox `isort` command. Calls `isort` command."
    pdm(session).run("isort", ".")


@nox.session
def black(session: nox.Session):
    "Nox `black` command. Calls `black` command."
    pdm(session).run("black", ".")


@nox.session
def mypy(session: nox.Session):
    "Nox `mypy` command. Calls `mypy` command."
    pdm(session).run("mypy", ".")


@nox.session
def typing(session: nox.Session):
    "Nox `typing` command. Calls `mypy` command."
    mypy(session)


@functools.cache
def github(session: nox.Session):
    "Global singleton of `github`."
    return _Github(session)


@functools.cache
def pdm(session: nox.Session):
    "Global singleton of `pdm`."
    return _Pdm(session)


@dcls.dataclass(frozen=True)
class _Github:
    "The manager for setting up github."

    session: nox.Session
    "The nox session to use."

    @functools.cache
    def setup(self) -> None:
        "The shared entrypoint to GitHub Actions scripts"

        # Does nothing outside of GitHub Actions.
        if not self.active():
            return

        self._remove_unwanted_files()
        self._log_storage_usage()

    def _run(self, *args: str):
        self.session.run_install(*args, external=True)

    def _remove_unwanted_files(self) -> None:
        "Remove the files GitHub Actions pre-installed."

        print("Removing files we did not ask for...")

        for folder in [
            "/usr/local/lib/android",
            "/usr/share/dotnet",
            "/usr/local/.ghcup",
        ]:
            self._run("sudo", "rm", "-rf", folder)

        self._run("docker", "system", "prune", "-af", "--volumes")

    def _log_storage_usage(self) -> None:
        "Log how much usage is currently being used by GitHub Actions."
        print("Investigating how much storage is used in GitHub Actions...")

        self._run("df", "-h")

    @staticmethod
    def active() -> bool:
        "Detect whether or not it is running in GitHub Actions."

        print("Checking if we are in GitHub Actions...", end=" ")
        result = os.getenv("GITHUB_ACTIONS") == "true"
        print("Yes" if result else "No")
        return result


@dcls.dataclass(frozen=True)
class _Pdm:
    session: nox.Session

    def __post_init__(self):
        github(self.session).setup()

        if _is_remote(self.session):
            self._run("pdm", "config", "python.use_venv", "true")

    def sync(self) -> None:
        self._sync_or_install("sync")

    def install(self):
        self._sync_or_install("install")

    def _install_and_run(self, *args: str):
        self.install()
        self._run(*args)

    def run(self, *args: str):
        self._install_and_run("pdm", "run", *args)

    def _sync_or_install(self, mode: str) -> None:
        # Don't repeatedly reinstall locally.
        if not _is_remote(self.session):
            return

        self.session.run_install("pdm", mode, "-G:all")

    def _run(self, *args: str):
        self.session.run(*args, external=True)


def _is_remote(session: nox.Session):
    return github(session).active()
