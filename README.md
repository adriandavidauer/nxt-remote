# nxt-remote
A python remote for the LEGO NXT using [nxt-python](https://github.com/schodet/nxt-python). This project was developed using python 3.7 on Windows.
This remote can be used with the Keyboard or a Webcam and an Imagemodel trained with [teachable machine](https://teachablemachine.withgoogle.com/train)

## Install
Follow the [install guide of nxt-python](https://github.com/schodet/nxt-python#requirements) and make sure to properly install *PyUSB* and *PyBluez*. 
### Gotchas on Windows
I needed to put the **libusb-1.0.dll** in the *system32* folder to make *PyUSB* work.

### Gotchas on Ubuntu 
On Ubuntu you need to install `libbluetooth-dev` with 
```bash
sudo apt-get install libbluetooth-dev
```

After installing all dependencies running
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

## Models for CAM mode
Models for CAM mode can be trained using [teachable machine](https://teachablemachine.withgoogle.com/train)
1. Choose `Image Project`
2. Choose `Standard Image Model`
3. Train your Model

    3.1. Choose Number of classes and set their class names
    
    3.2. Create or upload image samples for every class
    
    3.3. Select `Train Model`

4. Export Model

    4.1. Choose `Export Model`
    
    4.2. Choose `Tensorflow`
    
    4.3. Choose `Keras`
    
    4.4. Choose `Download my Model`


## Known Issues
The Bluetooth connection is not working with my setup of nxt-python under Windows.
