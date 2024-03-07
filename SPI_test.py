from periphery import GPIO
import time

W_CLK = GPIO("/dev/gpiochip4",10,"out")         #pin 18
FQ_UD = GPIO("/dev/gpiochip4",12,"out")         #pin 22
DATA = GPIO("/dev/gpiochip0", 7, "out")         #pin 29
RESET = GPIO("/dev/gpiochip0", 8, "out")        #pin 31

def pulseHigh(pin):               		# Function to send a pulse
  pin.write(True)
  pin.write(True)
  pin.write(True)
  pin.write(False)# do it a few times to increase pulse width# (easier than writing a delay loop!)   	# end of the pulse
  return

def tfr_byte(data):               		# Function to send a byte by serial "bit-banging"
  for i in range (0,8):
    if((data & 0x01) == 0x01):	# Mask out LSB and put on GPIO pin "DATA"
      DATA.write(True)
    elif((data & 0x01) == 0x00):
      DATA.write(False)
    pulseHigh(W_CLK)              	# pulse the clock line
    data=data>>1                  	# Rotate right to get next bit
  return

def sendFrequency(frequency):     		# Function to send frequency (assumes 125MHz xtal)
  freq=round((frequency*4294967295)/125000000)
  print(freq)
  for b in range (0,4):
    tfr_byte(freq & 0xFF)
    freq=freq>>8
    tfr_byte(0x00)
    pulseHigh(FQ_UD)
  return





frequency = [40000, 50000, 70000,100000, 200000]               		# choose frequency and
for i in range(0, len(frequency)):
  pulseHigh(RESET)                  		# start-up sequence...
  pulseHigh(W_CLK)
  pulseHigh(FQ_UD)
  print("sending frequency: "+str(frequency[i]))
  sendFrequency(frequency[i])          		# start the oscillator
  time.sleep(5)
