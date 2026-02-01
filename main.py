# Copyright (c) RenChu Wang - All Rights Reserved

from pathlib import Path

import typer


def main(config_path: Path) -> None:
    assert config_path.exists()


if __name__ == "__main__":
    typer.run(main)
