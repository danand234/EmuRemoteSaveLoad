import argparse
import json
import os
import random
import socket
import time
import traceback
from pynput.keyboard import Listener

#
# Example usage:
# ./server.py ../test/library.json -timer
#

key_pressed = False

class ErslServer:
    def __init__(self, config_data, key_trigger='=', timer_mode=False, timer_seconds=10):
        self.config_data = config_data
        self.key_trigger = key_trigger
        self.timer_mode = timer_mode
        self.timer_seconds = timer_seconds
        self.client_connection = None
        self.prior_select = -1

    def random_game_select(self, prior_game):
        while True:
            random_select = random.choice(self.config_data['games'])
            if random_select['id'] != prior_game:
                break
        return random_select

    def wait_for_connection(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
        s.bind(("127.0.0.1", 8080))
        s.listen(1)
        s.setblocking(1)
        print("[-] INFO: Waiting connection from emulator...")
        self.client_connection, addr = s.accept()
        self.client_connection.setblocking(1)
        self.client_connection.settimeout(5)
        print("[-] INFO: Connected: ", self.client_connection)

    def select_and_message(self):
        random_select = self.random_game_select(self.prior_select)
        self.prior_select = random_select['id']
        byte_data = bytearray(b'\x00')
        byte_data[0] = random_select['id']
        byte_message = bytes(byte_data)
        print("[-] INFO: Sending: [{}] {}".format(random_select['id'], random_select['game']))
        self.client_connection.send(byte_message)  # "HelloWorld".encode("utf-8")

    def start(self):
        global key_pressed
        # Main Loop
        while True:
            try:
                self.wait_for_connection()
                while True:
                    if self.timer_mode:
                        time.sleep(self.timer_seconds)
                        self.select_and_message()
                    elif key_pressed:
                        key_pressed = False
                        self.select_and_message()
                    else:
                        time.sleep(1)
            except Exception as err:
                print("[!] ERROR: Exception Occurred:\n{}\n{}".format(type(err).__name__, err))
                print(traceback.format_exc())

def on_press(key):
    global key_pressed
    print("[-] INFO: pressed key: {}".format(key))
    if hasattr(key, 'char') and key.char == ']':
        print("[-] INFO: Key triggered!")
        key_pressed = True


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('config_path', type=str, help="Path to config file")
    parser.add_argument('-timer', action='store_true', dest='timer_mode', default=False, help="Timer mode?")
    args = parser.parse_args()

    # Handle config
    if not os.path.exists(args.config_path):
        print("[!] ERROR: Invalid config file: {}".format(args.config_path))
        exit(1)

    with open(args.config_path) as json_data:
        config_data = json.load(json_data)

    if not config_data.get('games') or not config_data['games']:
        print("[!] ERROR: Invalid config file data: {}".format(args.config_path))
        exit(1)

    server = ErslServer(config_data, timer_mode=args.timer_mode)

    # Set up keyboard listener if timer mode is not enabled
    if not args.timer_mode:
        Listener(on_press=on_press).start()

    server.start()



if __name__ == "__main__":
    main()



