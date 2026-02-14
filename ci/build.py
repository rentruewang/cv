# Copyright (c) RenChu Wang - All Rights Reserved

import shutil

import gha
import pdm
import sh


def main():
    gha.setup()
    pdm.install()

    with sh.run_in_root():
        shutil.rmtree("build", ignore_errors=True)
        pdm.run(f"python main.py")


if __name__ == "__main__":
    main()
