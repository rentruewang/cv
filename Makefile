# Copyright (c) RenChu Wang - All Rights Reserved

# Run targets in the order given, even with `make -j`.
.NOTPARALLEL:

.DEFAULT_GOAL := build

.PHONY: build pre-commit formatting typing install free-disk-space

build:
	bash ci/build.sh

pre-commit:
	bash ci/pre-commit.sh

formatting:
	bash ci/formatting.sh

typing:
	bash ci/typing.sh

install:
	bash ci/install.sh

free-disk-space:
	bash ci/free-disk-space.sh
