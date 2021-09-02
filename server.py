import socket
import server_functions
import time
import json
import crc_functions
from _thread import *

def multi_threaded_client(c,addr):
    # receive client's name
    name = c.recv(1024).decode()
    print('====================================================================')
    print('Connected with ', addr, name)
    print('====================================================================')

    c.send(bytes('Connected to server', 'utf-8'))  # Transmit tcp msg as a byte with encoding format str to client

    # Session Initializations Parameters
    secret = 1234
    period = 2  # Period for continuous authentication
    time_margin = 0.2 * period  # Time margin for freshness = 20 % of period
    crc_key = '1001'  # CRC key

    received_shares = []  # Store old shares received during the session to check freshness of new share

    auth_result = "pass"  # initialized as pass
    num_of_fails = 0  # Number of times authentication has failed
    backoff_period = 0  # back off period initialized to 0

    while True:
        request = c.recv(1024).decode()
        if request == 'Request to send':
            c.send(bytes('Clear to send', 'utf-8'))  # notify client that its clear to send

            while True:  # receive message until CRC is pass
                start_timestamp = time.time()
                # msg_received = c.recv(1000000).decode()
                msg_received = '0' + bin(int.from_bytes(c.recv(1000000), byteorder='big'))[2:].zfill(8)
                print("Message received = ", msg_received)

                # CRC check
                rem = crc_functions.decodeData(msg_received, crc_key)  # Remainder
                if int(rem) == 0:
                    print("CRC check pass")
                    break
                else:
                    print("CRC check fail")
                    c.send(bytes('Resend message', 'utf-8'))  # Ask client to resend message if CRC fails

            r_bin_data = msg_received[:-(len(crc_key) - 1)]
            print('Received binary data = ', r_bin_data)

            # Convert binary to string
            msg_received_jsn = ''.join(chr(int(r_bin_data[i:i + 8], 2)) for i in range(0, len(r_bin_data), 8))

            msg_received = json.loads(msg_received_jsn)
            print('Message received = ', msg_received)

            auth_result = server_functions.authenticator(secret, crc_key, received_shares, msg_received, time_margin,
                                                         start_timestamp)
            print("Authentication ", auth_result)

            # Set backoff period according to auth result and consecutive num of failures
            if auth_result == "pass":
                num_of_fails = 0  # reset no of failures to 0
                backoff_period = 0  # reset backoff time to 0
                result_dict = {
                    "auth_result": auth_result,
                    "backoff_period": backoff_period
                }
                result = json.dumps(result_dict)
                print("Result Sent = ", result)
                c.send(bytes(result, 'utf-8'))
            else:
                num_of_fails = num_of_fails + 1
                backoff_period = period ** num_of_fails  # exponential backoff = auth period ^ num of failures
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
        elif request == 'Close Connection':
            print(request)
            c.close()  # close client socket
            break

s = socket.socket() # create server socket s with default param ipv4, TCP
print('Socket Created')

# to accept connections from clients, bind IP of server, a port number to the server socket
server_ip = socket.gethostbyname(socket.gethostname())
s.bind(('localhost', 9999)) # (IP, host num) #use a non busy port num
#s.bind((server_ip, 9999)) # (IP, host num) #use a non busy port num
#s.bind(('192.168.137.215', 9999))

# wait for clients to connect (tcp listener)
s.listen(3) #buffer for only 3 connections
print('Waiting for connections')

while True:
    # accept tcp connection from client
    c, addr = s.accept() # returns client socket and IP addr
    #new_client_thread(c, addr).start()
    start_new_thread(multi_threaded_client, (c, addr))