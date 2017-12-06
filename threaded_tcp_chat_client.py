from socket import *
from time import sleep
from threading import *


class ListenThread(Thread):
    def __init__(self, sock):
        self.sock = sock
        # Calling a constructor of 'Thread' class
        super().__init__()
        # self.start() essentially runs the run() method below
        self.start()

    def run(self):
        print('Now listening!')
        # Just keeps receiving messages as they come and prints them
        while True:
            print( self.sock.recv(4096).decode() )


# Static vars
srv_address = 'localhost'
srv_port = 2222

# Input
username = input('Enter your username: ')

# Establish connection to the server
while True:
    try:
        # Make a socket
        sock = socket(AF_INET, SOCK_STREAM)
        # Connect to the server
        sock.connect( (srv_address, srv_port) )
        print('Connected to {} on port {}'.format(srv_address, srv_port))
        # Send our username to the server
        sock.send(username.encode())
        # Initialize the listener so we can receive messages
        # And send them at the same time
        listener = ListenThread(sock)
        # We have connected so we can get out of the infinite loop
        break
    except:
        # Pretty self-explanatory
        print('Unable to connect to the server')
        print('Retrying in 5 seconds...')
        # Does nothing for 5 seconds, then goes back to the try block
        sleep(5)

# Main chat loop
while True:
    # Get user input
    message = input()
    # Send it to the server
    sock.send(message.encode())
