from periphery import SPI

spi1_0 = SPI("/dev/spidev0.0", 1, 125000000,0,40)

data = '{0:040b}'.format(40000)

data_out = [int(x) for x in str(data)]
data_out.reverse()

datain = spi.transfer(data_out)

print(data_out)
print(datain)

spi.close()
