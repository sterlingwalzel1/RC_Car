from gpiozero import DistanceSensor
import time
ultrasonic = DistanceSensor(echo=17, trigger=4, threshold_distance=0.5)
#ultrasonic  = DistanceSensor(echo=27, trigger=22, threshold_distance=0.5)

try:
    while True:
        print((ultrasonic.distance-0.01661) / 0.023205)
        time.sleep(1)


except KeyboardInterrupt:
    print('Got Keyboard Interrupt. Cleaning up and exiting')
    GPIO.cleanup()
    sys.exit()