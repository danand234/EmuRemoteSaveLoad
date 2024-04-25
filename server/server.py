import json
import os
import random
import socket
import time

config_path = '../working/library.json'
config_data = None
conn = None

def waitForConnection():
    global conn
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
    s.bind(("127.0.0.1", 8080))
    s.listen(1)
    s.setblocking(1)
    print("[-] INFO: Waiting connection from emulator...")
    conn, addr = s.accept()
    conn.setblocking(1)
    conn.settimeout(5)
    print("[-] INFO: Connected: ", conn)

if not os.path.exists(config_path):
    print("[!] ERROR: Invalid config file: {}".format(config_path))
    exit(1)

with open(config_path) as json_data:
    config_data = json.load(json_data)

if not config_data.get('games') or not config_data['games']:
    print("[!] ERROR: Invalid config file data: {}".format(config_path))
    exit(1)

prior_select = -1
while True:
    try:
        waitForConnection()
        while True:
            time.sleep(10) # TODO: Replace with input detection for red button (keyboard mapped)
            while True:
                random_select = random.choice(config_data['games'])
                if random_select['id'] != prior_select:
                    prior_select = random_select['id']
                    break
            byte_data = bytearray(b'\x00')
            byte_data[0] = random_select['id']
            byte_message = bytes(byte_data)
            print("[-] INFO: Sending: [{}] {}".format(random_select['id'], random_select['game']))
            conn.send(byte_message) #"HelloWorld".encode("utf-8")
    except Exception as err:
        print("[!] ERROR: Exception Occurred:\n{}\n{}".format(type(err).__name__, err))

