from periphery import GPIO
import time

time.sleep(5)
test_pin = GPIO("dev/gpiochip4", 13, "out")

while(i < 10):
  try:
    test_pin.write(True)
    time.sleep(5)
    test_pin.write(False)
    time.sleep(5)
    i = i + 1
  except Exception as e:
    print(f"An error occured: {e}")
    

