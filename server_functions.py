import hashlib
import hmac
import random
import numpy as np
import time

def authenticator(secret, received_shares, msg_received, time_margin):
    msg_received = msg_received.split(',')  # for test only
    # r = received
    r_client_id = msg_received[0]
    r_server_id = msg_received[1]
    r_message = msg_received[2]
    r_u = msg_received[3]
    r_timestamp = msg_received[4]
    r_time_flag = msg_received[5]
    r_sa = msg_received[6]
    r_mac = msg_received[7]

    print("Client ID = ", r_client_id)
    print("Server ID = ", r_server_id)
    print("Message = ", r_message)
    print("Share (u) = ", r_u)
    print("Timestamp = ", r_timestamp)
    print("Time flag = ", r_time_flag)
    print("Share Authenticator (sa) = ", r_sa)
    print("MAC = ", r_mac)

    # calc = newly calculated

    # Check message freshness with timestamp
    print("Timestamp difference = ", time.time() - float(r_timestamp))
    if abs(time.time() - float(r_timestamp)) <= time_margin:
        print("Message is fresh")
    else:
        print("Stale message")

    # Check if share is fresh (has not been used previously in this session)
    if received_shares.count(r_u) == 0:
        print("Share is fresh")
        received_shares.append(r_u)
    else:
        print("Share has been used previously")

    # Compute fresh MAC
    calc_mac = hmac.new(bytes(str(secret),'utf-8'), bytes(r_client_id + ',' + r_server_id + ',' + r_message + ',' + r_u + ',' + r_timestamp + ',' + r_time_flag, 'utf-8'), hashlib.sha256).digest()
    print("Calculated MAC = ", calc_mac)
    if str(calc_mac) == r_mac:
        print("MACs match")
    else:
        print("MACs do not match")

    # Compute new share authenticator
    print("u - secret - time flag= ", str(int(r_u) - secret - int(r_time_flag)))
    calc_sa = hashlib.sha256(bytes(str(int(r_u) - secret - int(r_time_flag)),'utf-8')).digest()
    print("Calculated share authenticator = ", calc_sa)
    if str(calc_sa) == r_sa:
        print("Share authenticated")
    else:
        print("Share not authenticated")