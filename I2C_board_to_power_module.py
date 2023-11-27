#I2C_board_to_power_module
from periphery import I2C


try:
    while True:
        try:
            i2c = I2C("/dev/i2c-1")
            data = [0x00]
            msgs = [I2C.Message([0x01, 0x00]), I2C.Message([0x00], read=True)]

            print("0x100: 0x{:02x}".format(msgs[1].data[0]))

            
        except Exception as e:
            print(f"An error occurered: {e}")
            
except KeyboardInterrupt:
    i2c.close()
