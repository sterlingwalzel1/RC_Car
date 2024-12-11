import RPi.GPIO as GPIO
import time
import sys

GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)
LED_O_PIN = 33

GPIO.setup(LED_O_PIN, GPIO.OUT)

try: 
    while(True):
        GPIO.output(LED_O_PIN, 1)

        time.sleep(1)


except KeyboardInterrupt:
    print('Got Keyboard Interript. Cleaning up an dexiting')
    GPIO.output(LED_O_PIN, GPIO.LOW)
    GPIO.cleanup()
    sys.exit()