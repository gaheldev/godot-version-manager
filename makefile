ifeq ($(OS),Windows_NT)
    platform := Windows
else
    platform := $(shell uname -s)
endif


.PHONY : build install release tests hook


tests :
	pytest -v


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
	# ./scripts/unix/pre-commit-test-hook

endif


#########  Linux  ########

ifeq ($(platform), Linux)

build :
	./scripts/unix/build

install : build
	./scripts/unix/install

release : build
	./scripts/unix/release

hook :
	./scripts/unix/pre-commit-test-hook

endif


