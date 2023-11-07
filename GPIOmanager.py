from periphery import SPI
from periphery import GPIO
import time

motionsensor = GPIO("sys/class/gpio/gpio141", 13, "in") # pin 36

try:
    while True:
        #put control in here
        time.sleep(10)
        

