import hashlib
import hmac
import random
import numpy as np
import json
import ntplib
import time

def get_timestamp():
    # Returns current ntp timestamp
    try:
        client = ntplib.NTPClient()
        response = client.request('pool.ntp.org')
        #print("Try 1")
        return response.tx_time
    except:
        try:
            client = ntplib.NTPClient()
            response = client.request('0.asia.pool.ntp.org')
            #print("Try 2")
            return response.tx_time
        except:
            try:
                client = ntplib.NTPClient()
                response = client.request('1.asia.pool.ntp.org')
                #print("Try 3")
                return response.tx_time
            except:
                try:
                    client = ntplib.NTPClient()
                    response = client.request('2.asia.pool.ntp.org')
                    #print("Try 4")
                    return response.tx_time
                except:
                    try:
                        client = ntplib.NTPClient()
                        response = client.request('3.asia.pool.ntp.org')
                        # print("Try 5")
                        return response.tx_time
                    except:
                        print("Error fetching time")

def polynomial_generator(k):
    #random.seed(50) # Random seed fixed for testing purpose

    # Forming k degree polynomial
    # f(x) = a0 + a1*x + a2*x^2 + ... + ak*x^k
    #a = np.zeros(k + 1, dtype=int)
    #a[0] = secret  # a0 = secret
    a = np.array(random.sample(range(1, 100), k)) # Generate random k coefficients a1, a2, ..., ak

    return a # Return polynomial coefficients

def share_generator(secret, a, x, time_flag, sent_shares):

    # Constructing points from the polynomial as shares
    # share u = f(x) where x = 1,2,..
    u = time_flag # Initializing to 0 and adding time flag
    for i in range(len(a)): # i = degree of x in each polynomial coefficient (0 to k)
        u += a[i]*(x**i) # u += ai*(x^i)
    print("share (x,u) = (", x, ",",u,")")

    # Computing share authenticator (sa)
    # sa equals hash(sum(ai*(x^i)) for i = 1,2,..,k)
    print("u - secret - time_flag = ", str(u-secret-time_flag))
    sa = hashlib.sha256(bytes(str(u - secret - time_flag),'utf-8')).digest()
    print("Share Authenticator sa = ", sa)

    return(u, sa) # return share, share authenticator


def message_generator(secret, server_id, client_id, msg, u, timestamp, time_flag, sa):
    # msg_to_mac = {server id,client id,message,share ui, timestamp, time_flag}
    # msg_to_mac = str(client_id) + ',' + str(server_id) + ',' + msg + ',' + str(u) + ',' + str(timestamp) + ',' + str(time_flag)

    msg_to_mac_dict = {
        "client_id": client_id,
        "server_id": server_id,
        "msg": msg,
        "u": int(u),
        "timestamp": timestamp,
        "time_flag": time_flag
    }

    # convert dict to json
    msg_to_mac = json.dumps(msg_to_mac_dict)
    print("Message to MAC = ", msg_to_mac)
    # mac = MAC with secret as key (server id,client id,message,share u, timestamp, time_flag)
    mac = hmac.new(bytes(str(secret),'utf-8'), msg_to_mac.encode('utf-8'), hashlib.sha256).digest()
    print("MAC =", mac)

    # message to send = {server id,client id,message,share u, timestamp, sa, MAC(server id,client id,message,share u)secret}
    #msg_to_send = msg_to_mac + ',' + str(sa) + ',' + str(mac)
    msg_to_send_dict = msg_to_mac_dict.copy()
    msg_to_send_dict["sa"] = str(sa)
    msg_to_send_dict["mac"] = str(mac)
    msg_to_send = json.dumps(msg_to_send_dict)
    print("Message to send = ", msg_to_send)
    return msg_to_send


