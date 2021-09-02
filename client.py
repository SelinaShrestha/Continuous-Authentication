import socket
import time
import random
import client_functions
import json
import numpy as np
import sys
import math
import hashlib

c = socket.socket() # create server socket c with default param ipv4, TCP

server_ip = 'localhost' # server ip addr local
#server_ip = '192.168.137.197'
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
crc_key = '1001' # CRC key
#x = 1
start_time = time.time()
timestamp = start_time # Gives current timestamp in seconds
time_flag = 1 # Initialization of time flag

period = 2 # Period for each authentication in seconds
total_period = 20 # Total period for the session
#no_of_auth = 0
sent_shares = [] # Store shares sent during the session to prevent duplicate shares

# Generate k degree polynomial for the secret
#a = np.array([secret])
#a = np.append(a, client_functions.polynomial_generator(k))
auth_result = "pass" # initialization
while (time.time() - start_time <= total_period):
    #if (time_flag <= no_of_auth):
    #if (time.time() - start_time <= total_period):
    if (time_flag == 1) or (time.time() - timestamp >= period):
        # If no of auth exceeds current polynomial degree, increase polynomial degree by k
        #no_of_auth = no_of_auth + 1
        #if no_of_auth > len(a) - 1:
            #a = np.append(a, client_functions.polynomial_generator(k))

        #print("Polynomial coefficients a = ", a)
        #print("Share u = f(x) = (a0 + time flag) + a1*x + a2*x^2 + ... + ak-1*x^k-1 where x = 1,2,...")

        # Generate share and share authenticator
        while True: # Select random x until unique share is generated
            x = random.randint(1, 9999) # Generate random x
            u = secret + time_flag + x # Share = secret + time flag + random number x
            #u, sa = client_functions.share_generator(secret, a, x, time_flag)
            if sent_shares.count(u) == 0: # Check that new share has not been sent previously
                sent_shares.append(u)
                break

        sa = hashlib.sha256(bytes(str(x),'utf-8')).digest() # Share authenticator = hash(share - secret - timeflag) = hash(x)

        print("share u = ", u)
        print("Share Authenticator sa = ", sa)

        msg = "Continuous Authentication " + str(time_flag)
        timestamp = time.time()

        # Generate message with authentication tokens
        msg_to_send = client_functions.message_generator(secret, server_id, client_id, msg, u, time_flag, sa)
        msg_with_crc = client_functions.crc_generator(msg_to_send, crc_key) # Add CRC

        #print("Size of message sent = ", sys.getsizeof(bytes(msg_with_crc, 'utf-8')))
        #print("Message sent in bytes = ", msg_with_crc.encode('utf-8'))

        msg_with_crc_bytes = int(msg_with_crc,2).to_bytes(math.ceil(len(msg_with_crc)/8), byteorder='big') # Convert from binary to bytes
        print("Message sent in bytes = ", msg_with_crc_bytes)
        print("Size of message in bytes = ", sys.getsizeof(msg_with_crc_bytes))

        c.send(bytes('Request to send','utf-8')) # Request to send message to server

        if(c.recv(1024).decode() == 'Clear to send'):

            #c.send(msg_with_crc.encode('utf-8')) # Send message to server
            c.send(msg_with_crc_bytes)  # Send message to server

            time_flag = time_flag + 1

            while True:
                # Resend message to server if CRC fails
                result = c.recv(1024).decode()
                if result == 'Resend message':
                    c.send(msg_with_crc_bytes)  # Resend message to server
                else:
                    break
            #result = c.recv(1024).decode() # Current auth result, backoff period
            print("Result = ", result)
            print('*********************************************************************')
            print(' ')
            result = json.loads(result)

            # Do not send data for backoff period if auth fails
            if result["auth_result"] == "fail":
                backoff_start = time.time()
                while time.time() - backoff_start <= result["backoff_period"]:
                    pass

c.send(bytes('Close Connection', 'utf-8'))
print("Share storage cost: ", sys.getsizeof(sent_shares))
