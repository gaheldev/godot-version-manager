ifeq ($(OS),Windows_NT)
    platform := Windows
else
    platform := $(shell uname -s)
endif


.PHONY : clean build install release tests hook patch-release minor-release major-release

clean :
	rm -r build
	rm -r dist
	rm *.completion
	rm *.spec

tests :
	pytest -v --runslow --online


######### Windows ########

ifeq ($(platform), Windows)

build :
	@echo not implemented for Windows

install : build
	@echo not implemented for Windows

release : build
	@echo not implemented for Windows

hook :
	@echo not implemented for Windows

patch-version : hook
	@echo not implemented for Windows

minor-release : hook
	@echo not implemented

major-release : hook
	@echo not implemented


endif


#########   OSX   ########

ifeq ($(platform), Darwin)

build :
	@echo not implemented for OSX
	# implement in unix script
	# ./scripts/unix/build

install : build
	@echo not implemented for OSX
	# implement in unix script
	# ./scripts/unix/install

release : build
	@echo not implemented for OSX
	# implement in unix script
	# ./scripts/unix/release

hook :
	@echo not implemented for OSX
	# implement in unix script
	# ./scripts/unix/pre-commit-hook

patch-release : hook
	@echo not implemented for OSX
	# implement in unix script
	# ./scripts/unix/push-patchh-release

minor-release : hook
	@echo not implemented

major-release : hook
	@echo not implemented


endif


#########  Linux  ########

ifeq ($(platform), Linux)

build :
	@./scripts/unix/build

install : build
	@./scripts/unix/install

release : build
	@./scripts/unix/release

hook :
	@./scripts/unix/pre-commit-hook

patch-release : hook
	@./scripts/unix/push-release-version patch

minor-release : hook
	@./scripts/unix/push-release-version minor

major-release : hook
	@./scripts/unix/push-release-version major


endif


