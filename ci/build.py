# Copyright (c) RenChu Wang - All Rights Reserved

import gha
import pdm
import sh

if __name__ == "__main__":
    gha.setup()
    pdm.install()

    with sh.run_in_root():
        pdm.run(f"python -m generate")
