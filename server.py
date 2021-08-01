import socket
import server_functions
import time
import json

s = socket.socket() # create server socket s with default param ipv4, TCP
print('Socket Created')

# to accept connections from clients, bind IP of server, a port number to the server socket
#server_ip = socket.gethostbyname(socket.gethostname())
s.bind(('localhost', 9999)) # (IP, host num) #use a non busy port num
#s.bind((server_ip, 9999)) # (IP, host num) #use a non busy port num

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

    # Session Initializations Parameters
    secret = 1234
    period = 3 # Period for continuous authentication
    time_margin = 0.2*period  # Time margin for freshness = 20 % of period

    received_shares = [] # Store old shares received during the session to check freshness of new share

    auth_result = "pass" # initialized as pass
    num_of_fails = 0 # Number of times authentication has failed
    backoff_period = 0 # back off period initialized to 0

    while True:
        msg_received = c.recv(1024).decode()
        if msg_received != 'Close Connection':
            print("Message received = ", msg_received)

            auth_result = server_functions.authenticator(secret, received_shares, msg_received, time_margin)
            print("Authentication ", auth_result)

            # Set backoff period according to auth result and consecutive num of failures
            if auth_result == "pass":
                num_of_fails = 0  # reset no of failures to 0
                backoff_period = 0 # reset backoff time to 0
                result_dict = {
                    "auth_result": auth_result,
                    "backoff_period": backoff_period
                }
                result = json.dumps(result_dict)
                print("Result Sent = ", result)
                c.send(bytes(result, 'utf-8'))
            else:
                num_of_fails = num_of_fails + 1
                backoff_period = period**num_of_fails # exponential backoff period^
                result_dict = {
                    "auth_result": auth_result,
                    "backoff_period": backoff_period
                }
                result = json.dumps(result_dict)
                print("Result Sent = ", result)
                c.send(bytes(result, 'utf-8'))
                backoff_start = time.time()
                # Do not receive data for backoff period
                while time.time() - backoff_start <= backoff_period:
                    pass
            print('*********************************************************************')
            print(' ')
        else:
            print(msg_received)
            c.close() # close client socket
            break