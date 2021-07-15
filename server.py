import socket
import server_functions

s = socket.socket() # create server socket s with default param ipv4, TCP
print('Socket Created')

# to accept connections from clients, bind IP of server, a port number to the server socket
s.bind(('localhost', 9999)) # (IP, host num) #use a non busy port num

# wait for clients to connect (tcp listener)
s.listen(3) #buffer for only 3 connections
print('Waiting for connections')

while True:
    # accept tcp connection from client
    c, addr = s.accept() # returns client socket and IP addr
    # receive client's name
    name = c.recv(1024).decode()
    print('====================================================================')
    print('Connected with ', addr, name)
    print('====================================================================')


    c.send(bytes('Connected to server','utf-8')) # Transmit tcp msg as a byte with encoding format str to client

    secret = 1234
    time_margin = 2  # Time margin for freshness in seconds
    received_shares = [] # Store old shares received during the session to check freshness of new share
    while True:
        msg_received = c.recv(1024).decode()
        if msg_received != 'Close Connection':
            print("Message received = ", msg_received)

            server_functions.authenticator(secret, received_shares, msg_received, time_margin)
            print('*********************************************************************')
            print(' ')
        else:
            c.close() # close client socket
            break