# GP2040-Flasher

> A simple tool to flash [GP2040-CE](https://github.com/OpenStickCommunity/GP2040-CE) boards/controllers with the latest firmware

Quick screencast of it in action:

https://github.com/SavageCore/GP2040-Flasher-Pi/assets/171312/424dc74c-3bee-4f4f-bb7d-0d4fcac6b63b

![PXL_20230616_003118005](https://github.com/SavageCore/GP2040-Flasher-Pi/assets/171312/c4d1ca1c-7698-4c9f-a170-003628e8d6bc)



## Installation

This guide assumes you're running a Raspberry Pi (< 4) with PiTFT and have followed the [Easy Install](https://learn.adafruit.com/adafruit-pitft-28-inch-resistive-touchscreen-display-raspberry-pi/easy-install-2) guide making sure to setup as a [Raw Framebuffer Device](https://learn.adafruit.com/adafruit-pitft-28-inch-resistive-touchscreen-display-raspberry-pi/easy-install-2#pitft-as-raw-framebuffer-device-2982165).

1. Follow the instructions to install [picotool](https://github.com/raspberrypi/picotool).
2. Install SDL2 Dev libraries for your operating system.
2. Clone this repository.
3. Run `pip install -r requirements.txt` to install the required Python packages.

## Usage

1. cd into the directory where you cloned this repository.
2. Run `sudo python3 main.py` to start the program. (You must run as root to access the GPIO pins and the framebuffer.)
3. Select the firmware you want to flash with the top 2 buttons.
4. Hold the BOOTSEL button on the device you wish to flash and plug it into the Pi.
5. The firmware will be flashed to the device and it will reboot as a controller. (The firmware is nuked if needed)

Also included is a script to create a systemd service to start the flasher on boot. To use it, run `./create-systemd-service.sh` and it will start on next boot. To stop it from starting on boot, run `sudo systemctl disable gp2040-flasher`. If you want to start it manually, run `sudo systemctl start gp2040-flasher`.

You can double press the bottom button to exit the program. Note if you installed the systemd service, it will restart the program.
