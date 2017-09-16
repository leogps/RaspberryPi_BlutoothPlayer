RaspberryPi_BluetoothPlayer
===================

Description:
-----------

Raspberry Pi Bluetooth player is a lightweight media player that is intended to run on Raspberry Pi.

Features:
--------

1. Comes with UI for the player without having to rely on the Linux's Graphical Desktop Environment libraries. i.e., the player UI does not require Raspberry Pi to be running any GUI libraries and can work on command-line.
2. Utilizes standard Bluetooth Media Player protocol and there by supports all bluetooth devices that has media player capabilities.
3. Super Lightweight owing to Python and SDL.
4. Replaceable frontend: The application runs readily on a PiTFT but this frontend can be refactored or replaces with any display component.

Software Dependencies:
---------------------

1. [Bluez - Official Linux Bluetooth protocol stack](http://www.bluez.org)
2. [dbus - message bus system](https://www.freedesktop.org/wiki/Software/dbus/)
3. Python
4. [SDL - Simple DirectMedia Layer](https://www.libsdl.org)

Setup:
-----

Because of varying Linux distributions for Raspberry Pi, the setup is very complex and varies based on the Raspberry Pi setup. However, the application is independent of any specific distribution and should run on all Linux distributions Raspberry Pi or not.
Having said that, a PiTFT is used for development and testing and the frontend code under the ui package assumes PiTFT display configuration for the Raspberry Pi.

1. Hardware: PiTFT Display (Optional)
2. Hardware: Bluetooth USB or in-built.
3. Bluez: Compile and install Bluez-5.xx. Dependencies below:

		`sudo apt-get install -y libusb-dev libdbus-1-dev libglib2.0-dev libudev-dev libical-dev libreadline-dev`
		

Hardware Requirements:
---------------------

1. Works readily with [PiTFT](https://www.adafruit.com/product/1601). Follow Adafruit's PiTFT setup for Raspberry Pi before running the application.

Screenshots:
-----------

Coming soon.


[License](http://creativecommons.org/licenses/by/4.0/legalcode)

[License summary](http://creativecommons.org/licenses/by/4.0/)
