from socket import *
from threading import *


class ClientHandler(Thread):
    def __init__(self, cl_sock, cl_address, cl_username):
        self.sock = cl_sock
        self.address = cl_address
        self.username = cl_username

        # Append thread to all clients
        clients.append(self)
        # Calling a constructor of 'Thread' class
        super().__init__()
        # self.start() essentially runs the run() method below
        self.start()

    def run(self):
        print('<{}> has connected!'.format(self.username))

        while True:
            try:
                # Receive message from this client
                text = self.sock.recv(4096).decode()
                # Making a sending format variable
                send_to_client = '<{}> {}'.format(self.username, text)
                print('<{}> {}'.format(self.username, text))

                # Send data to every other user
                for client in clients:
                    client.sock.send(send_to_client.encode())

            except ConnectionResetError:
                # Making a sending format variable
                dc_message = 'User {} has disconnected'.format(self.username)
                print(dc_message)
                # Thread removes itself from clients list
                clients.remove(self)
                # Send every client that this client disconnected
                for client in clients:
                    client.sock.send(dc_message.encode())
                # Close the connection to the server
                self.sock.close()
                # Break out of the infinite loop so the thread can finish
                break


# Consts
srv_address = 'localhost'
srv_port = 2222

# Vars
clients = []

# Listen for connections

# Make a socket
srv_sock = socket(AF_INET, SOCK_STREAM)
# Bind the socket to specific address and port
srv_sock.bind( (srv_address, srv_port) )
# Listen for connections
srv_sock.listen(5)
print('Server is ready to accept new connections!')

# Accept new connections
while True:
    # Get the client socket and client address when accepting the connection
    cl_sock, cl_address = srv_sock.accept()
    # We wait for the client to send us his/her username
    cl_username = cl_sock.recv(4096).decode()
    # We initialize the ClientThread class defined above
    client = ClientHandler(cl_sock, cl_address, cl_username)