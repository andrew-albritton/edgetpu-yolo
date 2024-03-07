from periphery import SPI

while(1):
  spi1_0 = SPI("/dev/spidev0.0", 0, 125000000)
  
  data = '{0:040b}'.format(40000)
  
  data_out = [int(x) for x in str(data)]
  data_out.reverse()
  
  datain = spi1_0.transfer(data_out)
  
  print(data_out)
  print(datain)
  

spi1_0.close()
