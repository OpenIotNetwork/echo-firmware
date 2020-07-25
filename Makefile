PORT = /dev/cu.usbmodemPy9f7f541

.DEFAULT_GOAL := all

upload:
	rshell -p $(PORT) cp -r *.py /flash

reset:
	rshell -p $(PORT) repl '~' 'import machine' '~' 'machine.reset()' '~'

all:
	@$(MAKE) upload
	@$(MAKE) reset
