'''
This is a remote control for the NXT.
All keystrokes will be send to the NXT with the corresponding key code if the KEYBOARD mode is chosen and all classnames will be send if the CAM mode is chosen.
'''
# system imports

# 3rd party imports
import nxt.locator
from nxt.error import DirectProtocolError
from pynput.keyboard import Key, Listener
import cv2 as cv


# local imports
from model import ImageModel


class Remote():
    TYPES = ['KEYBOARD', 'CAM']

    def __init__(self, type='KEYBOARD', model_path=None, labels=None, cam_port=0, **kwargs) -> None:
        if not type in self.TYPES:
            raise AttributeError(
                f'{type} is not a supported type. Supported types are {self.TYPES}')
        self.connect(**kwargs)
        if type == 'KEYBOARD':
            print('started remote - press ESC to close it.')
            # wait for keystrokes
            with Listener(on_press=self.on_keystroke, on_release=self.on_release) as listener:
                listener.join()
        elif type == 'CAM':
            print('started remote - press CTRL+C to close it.')
            if not model_path:
                raise ValueError('model_path must be given!')
            model = ImageModel(model_path=model_path, labels_path=labels)
            cam = cv.VideoCapture(cam_port)
            result, image = cam.read()
            while result:
                prediction = model.predict(image_path=None, image=image)
                # only send the class with highest probability
                print(max(prediction, key=prediction.get))
                self.on_keystroke(max(prediction, key=prediction.get))
                result, image = cam.read()

    def connect(self, **kwargs):
        if 'host' in kwargs:
            host = kwargs['host']
        else:
            host = None
        try:
            self.brick = nxt.locator.find(host=host)
            print(f'connected to {host}')
        except Exception as e:
            print(f"Couldn't connect: {e}")

    def on_keystroke(self, key, mailbox=0):
        '''
        This callback sends the key code to the NXT
        '''
        try:
            self.brick.message_write(mailbox, bytes(str(key), 'utf-8'))
        except DirectProtocolError as e:
            print(e)
        except AttributeError as e:
            print('Remote is not connected')
            # TODO: add some logic to reconnect - maybe a specific button or combi like ctrl+r

    def on_release(self, key):
        if key == Key.esc:
            # Stop listener
            return False


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(
        description='Remote to send keystrokes or classnames to NXT')
    parser.add_argument('mode', help="Mode of the remote",
                        choices=Remote.TYPES)
    parser.add_argument(
        '--model_path', help="Path to the model file(only required in CAM mode)")
    parser.add_argument(
        '--labels', help="Path to the labels file(only required in CAM mode)")
    parser.add_argument(
        '--cam_port', help='cam_port decides which cam to use')
    args = parser.parse_args()
    host = "00:16:53:0E:45:FA"
    remote = Remote(host=host, type=args.mode,
                    model_path=args.model_path, labels=args.labels)
    # remote.on_keystroke('b')
