import hashlib
import hmac
import random
import numpy as np

def polynomial_generator(secret, k):
    random.seed(50) # Random seed fixed for testing purpose

    # Forming k-1 degree polynomial
    # f(x) = a0 + a1*x + a2*x^2 + ... + ak-1*x^k-1
    a = np.zeros(k, dtype=int)
    a[0] = secret  # a0 = secret
    a[1:] = random.sample(range(1, secret), k - 1)  # Generate random k-1 coefficients a1, a2, ..., ak-1
    print("Polynomial coefficients a = ", a)
    print("Share u = f(x) = a0 + a1*x + a2*x^2 + ... + ak-1*x^k-1 where x = 1,2,...")
    return a # Return polynomial coefficients

def share_generator(secret, a, x, time_flag):

    # Constructing points from the polynomial as shares
    # share u = f(x) where x = 1,2,..
    u = time_flag # Initializing to 0 and adding time flag
    for i in range(len(a)): # i = degree of x in each polynomial coefficient (0 to k-1)
        u += a[i]*(x**i) # u += ai*(x^i)
    print("share (x,u) = (", x, ",",u,")")

    # Computing share authenticator (sa)
    # sa equals hash(sum(ai*(x^i)) for i = 1,2,..,k-1)
    print("u - secret - time_flag = ", str(u-secret-time_flag))
    sa = hashlib.sha256(bytes(str(u - secret - time_flag),'utf-8')).digest()
    print("Share Authenticator sa = ", sa)

    return(u, sa) # return share, share authenticator


def message_generator(secret, server_id, client_id, msg, u, timestamp, time_flag, sa):
    # msg_to_mac = {server id,client id,message,share ui, timestamp, time_flag}
    msg_to_mac = str(client_id) + ',' + str(server_id) + ',' + msg + ',' + str(u) + ',' + str(timestamp) + ',' + str(time_flag)
    print("Message to MAC = ", msg_to_mac)
    # mac = MAC with secret as key (server id,client id,message,share u, timestamp, time_flag)
    mac = hmac.new(bytes(str(secret),'utf-8'), bytes(msg_to_mac, 'utf-8'), hashlib.sha256).digest()
    # message to send = {server id,client id,message,share u, timestamp, sa, MAC(server id,client id,message,share u)secret}
    msg_to_send = msg_to_mac + ',' + str(sa) + ',' + str(mac)
    print("Message to send = ", msg_to_send)
    return msg_to_send


