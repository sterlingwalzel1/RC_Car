from gpiozero import DistanceSensor
import time
ultrasonic = DistanceSensor(echo=17, trigger=4, threshold_distance=0.5)
try:
    while True:
        print(ultrasonic.distance)
        time.sleep(1)


except KeyboardInterrupt:
    print('Got Keyboard Interrupt. Cleaning up and exiting')
    GPIO.cleanup()
    sys.exit()