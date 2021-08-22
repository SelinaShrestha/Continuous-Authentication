import hashlib
import hmac
import random
import numpy as np
import time
import json
import crc_functions
import ntplib


def authenticator(secret, crc_key, received_shares, msg_received, time_margin, start_timestamp):
    # CRC check
    rem = crc_functions.decodeData(msg_received, crc_key) # Remainder
    if int(rem) == 0:
        print("CRC check pass")
    else:
        print("CRC check fail")
        return "fail"

    r_bin_data = msg_received[:-(len(crc_key) - 1)]
    print('Received binary data = ', r_bin_data)

    msg_received_jsn = ''.join(chr(int(x, 2)) for x in r_bin_data.split())
    print(msg_received_jsn)
    msg_received = json.loads(msg_received_jsn)
    print('Message received = ', msg_received)


    #msg_received = json.loads(msg_received)
    # r = received
    r_client_id = msg_received["client_id"]
    r_server_id = msg_received["server_id"]
    r_message = msg_received["msg"]
    r_u = msg_received["u"]
    r_time_flag = msg_received["time_flag"]
    r_sa = msg_received["sa"]
    r_mac = msg_received["mac"]

    print("Client ID = ", r_client_id)
    print("Server ID = ", r_server_id)
    print("Message = ", r_message)
    print("Share (u) = ", r_u)
    print("Time flag = ", r_time_flag)
    print("Share Authenticator (sa) = ", r_sa)
    print("MAC = ", r_mac)

    # calc = newly calculated

    # Check message freshness with timestamp
    timestamp = time.time()
    print("Timestamp difference = ", start_timestamp - timestamp)
    print("time margin = ", time_margin)
    if abs(start_timestamp - timestamp) <= time_margin:
        print("Message is fresh")
    else:
        print("Stale message")
        return "fail"

    # Check if share is fresh (has not been used previously in this session)
    if received_shares.count(r_u) == 0:
        print("Share is fresh")
        received_shares.append(r_u)
    else:
        print("Share has been used previously")
        return "fail"

    # Compute fresh MAC
    msg_to_mac_dict = {
        "client_id": r_client_id,
        "server_id": r_server_id,
        "msg": r_message,
        "u": r_u,
        "time_flag": r_time_flag
    }
    # convert dict to json
    msg_to_mac = json.dumps(msg_to_mac_dict)
    print("Message to MAC = ", msg_to_mac)
    #calc_mac = hmac.new(bytes(str(secret),'utf-8'), bytes(r_client_id + ',' + r_server_id + ',' + r_message + ',' + r_u + ',' + ',' + r_time_flag, 'utf-8'), hashlib.sha256).digest()
    calc_mac = hmac.new(bytes(str(secret),'utf-8'), msg_to_mac.encode('utf-8'), hashlib.sha256).digest()
    print("Calculated MAC = ", calc_mac)
    if str(calc_mac) == r_mac:
        print("MACs match")
    else:
        print("MACs do not match")
        return "fail"

    # Compute new share authenticator
    print("u - secret - time flag= ", str(r_u - secret - r_time_flag))
    calc_sa = hashlib.sha256(bytes(str(r_u - secret - r_time_flag),'utf-8')).digest()
    print("Calculated share authenticator = ", calc_sa)
    if str(calc_sa) == r_sa:
        print("Share authenticated")
        return "pass"
    else:
        print("Share not authenticated")
        return "fail"