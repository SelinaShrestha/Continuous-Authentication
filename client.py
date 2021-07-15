import socket
import time
import client_functions

c = socket.socket() # create server socket c with default param ipv4, TCP

server_ip = 'localhost' # server ip addr

# connect to server socket
c.connect((server_ip,9999))

name = input("Enter your name:") # Taking input from client
c.send(bytes(name, 'utf-8')) # Send client name to server

# receive byte sent by server and print it
print (c.recv(1024).decode()) # decode byte to string


# Initialization
secret = 1234
k = 5 # degree of polynomial
server_id = 1
client_id = 2
x = 1
start_time = time.time()
timestamp = start_time # Gives current timestamp in seconds
time_flag = 1 # Initialization of time flag

no_of_auth = 3 # No of times to authenticate
period = 3 # Period for each authentication in seconds

while True:
    if (time_flag <= no_of_auth):
        if (time_flag == 1) or (time.time() - timestamp >= period):

            timestamp = time.time()

            # Generate k degree polynomial for the secret
            a = client_functions.polynomial_generator(secret, k)

            # Generate share and share authenticator
            u, sa = client_functions.share_generator(secret, a, x, time_flag)

            msg = "Continuous Authentication " + str(time_flag)


            # Generate message with authentication tokens
            msg_to_send = client_functions.message_generator(secret, server_id, client_id, msg, u, timestamp, time_flag, sa)

            c.send(bytes(msg_to_send, 'utf-8')) # Send message to server

            x = x + 1
            time_flag = time_flag + 1
            #timestamp = time.time()
            print('*********************************************************************')
            print(' ')
    else:
        c.send(bytes('Close Connection', 'utf-8'))
        break