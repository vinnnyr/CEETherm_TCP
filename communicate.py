#!/usr/bin/env python
import socket
from umodbus import conf
from umodbus.client import tcp

# Enable values to be signed (default is False).
conf.SIGNED_VALUES = True
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

def connect(ip):
    #ip = '10.0.2.137' #ip of the WTS
    #print(ip)
    print("Attempting socket connection to " + ip)
    sock.connect((ip, 502))
    if sock:
        print("Connected!")

def send_message():
    message = tcp.read_holding_registers(slave_id = 1, starting_address = 0, quantity = 4)
    try:
        response = tcp.send_message(message, sock)
        return response
    except ValueError:
        print("Whoops... WTS seems to be not responding")

def try_reset(): #Unused method I believe.
    print("Trying Reset")
    message = tcp.write_single_register(1, 253 , value = 1)
    print(message)
    try:
        response = tcp.send_message(message, sock)
        return response
    except ValueError:
        print("Reset didn't work")

def close_sock():
    # Shutdown socket before close
    sock.shutdown(socket.SHUT_RDWR)
    sock.close()
    print(" \nSocket successfully closed")





