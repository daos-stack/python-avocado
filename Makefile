NAME    := python-avocado
SRC_EXT := gz
# for some reason spectool doesn't work on the spec
# in this module
SOURCE  := https://github.com/avocado-framework/avocado/archive/69.0.tar.gz
PATCHES :=

include packaging/Makefile_packaging.mk
