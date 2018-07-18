#!/usr/bin/env python
# scripts/examples/simple_tcp_client.py
import socket

from umodbus import conf
from umodbus.client import tcp
import matplotlib.pyplot as plt

from matplotlib import style

ip = '10.0.2.137' #ip of the WTS

# Enable values to be signed (default is False).
conf.SIGNED_VALUES = True

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print("Attempting socket connection to " + ip)
sock.connect((ip, 502))

if sock:
    print("Success!")

# Returns a message or Application Data Unit (ADU) specific for doing
# Modbus TCP/IP.
message = tcp.read_holding_registers(slave_id = 1, starting_address = 0, quantity = 5)
style.use('fivethirtyeight')

fig = plt.figure()
ax1 = fig.add_subplot(1,1,1)
xs = []
ys = []
i = 0

try:
    while True:
        # Response depends on Modbus function code. This particular returns the
        # amount of coils written, in this case it is.
        response = tcp.send_message(message, sock)
        print(response)
        idx = 0
        i += 1
        xs.append(i)
        ys.append(response[idx])
        ax1.clear()
        ax1.plot(xs, ys)

except KeyboardInterrupt:
    pass
sock.close()
plt.show()
print(" \n Socket successfully closed")
