import socket
import time
import hashlib
import struct

class Header:
    def __init__(self):
        self.field1__ = 0
        self.field2__ = 0
        self.field3__ = 0
        self.field4__ = 'fileexemplo.txt'

    def to_bytes(self):
        return struct.pack('BBB255s', self.field1, self.field2, self.field3, self.field4)
    def setMessage__(self, message):
        self.field1__ = message
    def setCommand__(self, command):
        self.field2__ = command
    def setFileNameSize__(self, FileNameSize):
        self.field3__ = FileNameSize
    def setFileName__(self, FileName):
        self.field4__ = FileName
    def addfile(self):
        self.setMessage__(1)
    def delete(self):
        self.setMessage__(2)
    def getfileslist(self):
        self.setMessage__(3)
    def getfile(self):
        self.setMessage__(4)


    
HOST = "127.0.0.1"
PORT = 65435


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    while True:
        message = input("Enter message to send or 'STOP' to quit: ")
        if message == 'STOP':
            break
        words = message.replace(',', ' ').split()  # Split the message into words
        if words[0] == 'CONNECT':
            sha512_hash = hashlib.sha512()
            sha512_hash.update(words[2].encode())
            words[2] = sha512_hash.hexdigest()  # Replace the third word with its SHA512 hash
        message_to_send = ' '.join(words)  # Join the words with a space
        print(f"Sending: {message_to_send}")
        s.sendall(message_to_send.encode())
        data = s.recv(1024)
        print(f"Received "+data.decode())
        if data.decode() == 'EXIT':
            break