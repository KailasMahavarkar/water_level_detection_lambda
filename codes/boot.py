# Complete project details at https://RandomNerdTutorials.com

try:
  import usocket as socket
except:
  import socket

from machine import Pin
import network
import time



import esp
esp.osdebug(None)


import gc
gc.collect()


led = Pin(2, Pin.OUT)

ssid = 'kailashmm'
password = 'charcharmanderx'

station = network.WLAN(network.STA_IF)
station.active(True)
station.connect(ssid, password)


# give 3 seconds to connect to wifi
print("searching for wifi")
time.sleep(5)
print("stopping search for wifi")

while station.isconnected() == False:
  pass

print('Connection successful')
print(station.ifconfig())


