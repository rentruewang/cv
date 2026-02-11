# Copyright (c) RenChu Wang - All Rights Reserved

from argparse import ArgumentParser

import gha
import pdm
import sh


def main(cfg: str):
    gha.setup()
    pdm.install()

    with sh.run_in_root():
        pdm.run(f"python -m cv {cfg}")


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("config")
    flags = vars(parser.parse_args())
    main(flags["config"])
