'''This is a remote control for the NXT. All keystrokes will be send to the NXT with the corresponding key code'''
# system imports

# 3rd party imports
import nxt.locator
from nxt.error import DirectProtocolError
from pynput.keyboard import Key, Listener


# local imports


class Remote():
    def __init__(self, **kwargs) -> None:
        self.connect(**kwargs)
        print('started remote - press ESC to close it.')
        # wait for keystrokes
        with Listener(on_press=self.on_keystroke, on_release=self.on_release) as listener:
            listener.join()

    def connect(self, **kwargs):
        if 'host' in kwargs:
            host = kwargs['host']
        else:
            host = "00:16:53:0E:45:FA"
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
    remote = Remote()
    # remote.on_keystroke('b')
