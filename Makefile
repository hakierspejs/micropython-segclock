PORT=/dev/tty.usbmodem101

shell:
	mpremote connect $(PORT) repl

ls:
	mpremote connect $(PORT) ls

deploy:
	mpremote connect $(PORT) fs cp ./*.py :

run: deploy
	mpremote connect $(PORT) run example.py

install_unittest:
	mpremote connect $(PORT) mip install traceback
	wget https://raw.githubusercontent.com/cb4b1fd915/micropython-lib/master/python-stdlib/unittest/unittest/__init__.py -O /tmp/unittest.py
	mpremote connect $(PORT) fs cp /tmp/unittest.py :/lib/unittest.py
	rm /tmp/unittest.py

test: install_unittest deploy
	mpremote connect $(PORT) run test.py
