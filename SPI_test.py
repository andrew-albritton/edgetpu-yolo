from periphery import SPI
frequency = 40000
freq = frequency * 4294967295 / 125000000
  

spi1_0 = SPI("/dev/spidev0.0", 0, 125000000)

data = '{0:040b}'.format(freq)

data_out = [int(x) for x in str(data)]
data_out.reverse()
try:
  while(True):
    try:
      datain = spi1_0.transfer(data_out)
    except Exception as e:
      print(f"An error occurred: {e}")
except KeyboardInterrupt:
  spi1_0.close()
