.PHONY : build install release test hook

build :
	./scripts/build.sh

install : build
	./scripts/install.sh

release : build install
	./scripts/release.sh

tests :
	pytest -v

hook :
	./scripts/pre-commit-hook.sh
