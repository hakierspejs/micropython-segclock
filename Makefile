ifeq (,$(wildcard /dev/tty.usbmodem101))
	PORT=/dev/tty.usbmodem1101
endif
PORT=/dev/tty.usbmodem101

shell:
	mpremote connect $(PORT) repl

ls:
	mpremote connect $(PORT) ls

deploy:
	mpremote connect $(PORT) fs cp ./*.py :

run: deploy
	mpremote connect $(PORT) run example.py

REQUIREMENTS_INFO := $(shell mpremote connect $(PORT) fs ls ./lib/unittest/ | grep __init__.mpy > /dev/null; echo $$?)
test:
ifneq ($(REQUIREMENTS_INFO),0)
	mpremote connect $(PORT) mip install unittest
endif
	mpremote connect $(PORT) run test.py
