from periphery import GPIO

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
    else:
      DATA.write(False)
    pulseHigh(W_CLK)              	# pulse the clock line
    data=data>>1                  	# Rotate right to get next bit
  return

def sendFrequency(frequency):     		# Function to send frequency (assumes 125MHz xtal)
  freq=int(frequency*4294967296/125000000)
  for b in range (0,4):
    tfr_byte(freq & 0xFF)
    freq=freq>>8
    tfr_byte(0x00)
    pulseHigh(FQ_UD)
  return



pulseHigh(RESET)                  		# start-up sequence...
pulseHigh(W_CLK)
pulseHigh(FQ_UD)

frequency = 1000000               		# choose frequency and
sendFrequency(frequency)          		# start the oscillator
