#!/usr/bin/env python
# scripts/examples/simple_tcp_client.py
import socket

from umodbus import conf
from umodbus.client import tcp

ip = '10.0.2.156' #ip of the WTS

# Enable values to be signed (default is False).
conf.SIGNED_VALUES = True

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print("Attempting socket connection to " + ip)
sock.connect((ip, 502))

if sock:
    print("Success!")
else:
    print("Make sure you are connected to the right network")
# Returns a message or Application Data Unit (ADU) specific for doing
# Modbus TCP/IP.
message = tcp.read_holding_registers(slave_id = 1, starting_address = 0, quantity = 5)
while True:
    # Response depends on Modbus function code. This particular returns the
    # amount of coils written, in this case it is.
    response = tcp.send_message(message, sock)
    print(response)
sock.close()