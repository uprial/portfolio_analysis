# vim: ts=4 sts=4 sw=4 noexpandtab: syntax=make

all:
	pylint --disable="missing-docstring" *.py
