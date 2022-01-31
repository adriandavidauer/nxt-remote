# nxt-remote
A python remote for the LEGO NXT using [nxt-python](https://github.com/schodet/nxt-python). This project was developed using python 3.7 on Windows.

## Install
Follow the [install guide of nxt-python](https://github.com/schodet/nxt-python#requirements) and make sure to properly install *PyUSB* and *PyBluez*. 
I needed to put the **libusb-1.0.dll** in the *system32* folder to make *PyUSB* work.
On Ubuntu you need to install `libbluetooth-dev` with 
```bash
sudo apt-get install libbluetooth-dev
```
Running
```bash
pip install -r requirements.txt
```
should not give any errors after installing all dependencies.

## Usage
To start the remote just run

```bash
python remote.py KEYBOARD
```
for KEYBOARD mode


or
```bash
python remote.py CAM --model_path <PATH_TO_MODEL> --labels <PATH_LABEL>
```
for CAM mode.


It will just send every key(in KEYBOARD mode) or the class name(in CAM mode) as a string to the Mailbox 0 as default.
On the NXT a program can read these commands from the Mailbox.

## Known Issues
The Bluetooth connection is not working with my setup of nxt-python under Windows.
