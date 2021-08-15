import socket
import time
import random
import client_functions
import json
import numpy as np
import sys


c = socket.socket() # create server socket c with default param ipv4, TCP

server_ip = 'localhost' # server ip addr local
#server_ip = '10.161.6.234' # server ip addr rbpi w sticker
#server_ip = '10.161.6.230' # server ip addr rbpi wo sticker

# connect to server socket
c.connect((server_ip,9999))

name = input("Enter your name:") # Taking input from client
c.send(bytes(name, 'utf-8')) # Send client name to server

# receive byte sent by server and print it
print (c.recv(1024).decode()) # decode byte to string


# Initialization
secret = 1234
k = 3 # degree of polynomial
server_id = server_ip
client_id = socket.gethostbyname(socket.gethostname())
#x = 1
start_time = client_functions.get_timestamp()
timestamp = start_time # Gives current timestamp in seconds
time_flag = 1 # Initialization of time flag

period = 2 # Period for each authentication in seconds
total_period = 21 # Total period for the session
no_of_auth = 0
sent_shares = [] # Store shares sent during the session to prevent duplicate shares

# Generate k degree polynomial for the secret
a = np.array([secret])
a = np.append(a, client_functions.polynomial_generator(k))
auth_result = "pass" # initialization
while (client_functions.get_timestamp() - start_time <= total_period):
    #if (time_flag <= no_of_auth):
    #if (time.time() - start_time <= total_period):
    if (time_flag == 1) or (client_functions.get_timestamp() - timestamp >= period):
        # If no of auth exceeds current polynomial degree, increase polynomial degree by k
        no_of_auth = no_of_auth + 1
        if no_of_auth > len(a) - 1:
            a = np.append(a, client_functions.polynomial_generator(k))

        print("Polynomial coefficients a = ", a)
        print("Share u = f(x) = (a0 + time flag) + a1*x + a2*x^2 + ... + ak-1*x^k-1 where x = 1,2,...")

        # Generate share and share authenticator
        while True: # Select random x until unique share is generated
            x = random.randint(1, 20) # Generate random x
            u, sa = client_functions.share_generator(secret, a, x, time_flag, sent_shares)
            if sent_shares.count(u) == 0: # Check that new share has not been sent previously
                sent_shares.append(u)
                break

        msg = "Continuous Authentication " + str(time_flag)
        timestamp = client_functions.get_timestamp()

        # Generate message with authentication tokens
        msg_to_send = client_functions.message_generator(secret, server_id, client_id, msg, u, timestamp, time_flag, sa)

        c.send(bytes(msg_to_send, 'utf-8')) # Send message to server

        time_flag = time_flag + 1

        result = c.recv(1024).decode() # Current auth result, backoff period
        print("Result = ", result)
        print('*********************************************************************')
        print(' ')
        result = json.loads(result)

        # Do not send data for backoff period if auth fails
        if result["auth_result"] == "fail":
            backoff_start = client_functions.get_timestamp()
            while client_functions.get_timestamp() - backoff_start <= result["backoff_period"]:
                pass

c.send(bytes('Close Connection', 'utf-8'))
print("Share storage cost: ", sys.getsizeof(sent_shares))
