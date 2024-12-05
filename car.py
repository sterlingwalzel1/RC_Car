import RPi.GPIO as GPIO
import time
import sys
import os
import spidev
import paho.mqtt.client as mqtt
from gpiozero import DistanceSensor

sys.path.insert(0, '../utilities')
import utilities
leftFLED  = 29
leftBLED  = 31
rightFLED = 32
rightBLED = 33

#ultrasonic sensor config
us_front = DistanceSensor(echo=17, trigger=4,  threshold_distance=0.5)
us_back  = DistanceSensor(echo=27, trigger=22, threshold_distance=0.5)

#GPIO configuration
GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)
GPIO.setup(16, GPIO.OUT)
GPIO.setup(18, GPIO.OUT)
GPIO.setup(22, GPIO.OUT)
GPIO.setup(leftFLED,  GPIO.OUT)
GPIO.setup(leftBLED,  GPIO.OUT)
GPIO.setup(rightFLED, GPIO.OUT)
GPIO.setup(rightBLED, GPIO.OUT)

#configure duty cycles
turn   = GPIO.PWM(16, 50)
turn.start(8.5)
speed1 = GPIO.PWM(18, 1000)
speed1.start(0)
speed2 = GPIO.PWM(22, 1000)
speed2.start(0)

#led blinking
light_state = ['LIGHT_OFF', 'LIGHT_ON']
light_state = enumerate(light_state)
light_state = 'LIGHT_OFF'

# this callback runs once when the client connects with the broker
def on_connect(client, userdata, flags, rc):
    print(f"Connected with result code {rc}")
    client.subscribe(sub_topic_name)

# this callback runs whenever a message is received
def on_message(client, userdata, msg):
    act = (float(msg.payload))
    print(act)
    if (act > 100 and act < 1000) or (act > 1100 and act < 2000) or act > 2100 or act < 0:
        print("DIPSHIT THAT DON'T WORK")
    elif act <= 100:
        act = (act / 16.67) + 6
        turn.ChangeDutyCycle(act)
        global turnSignal = act 
    elif (act >= 1000) and (act <= 1100):
        act = act % 1000
        speed1.ChangeDutyCycle(act) 
        speed2.ChangeDutyCycle(0) 
    elif (act >= 2000) and (act <= 2100):
        act = act % 2000
        speed1.ChangeDutyCycle(0) 
        speed2.ChangeDutyCycle(act) 


    
# Read command line arguments and set the publish and subscribe topic names
# based on the command line arguments
numArgs = len(sys.argv)
my_name = sys.argv[1]
sub_topic_name = my_name + '/home/dutycycle'

# Initialize MQTT and connects to the broker
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.connect("broker.emqx.io", 1883, 60)
client.loop_start()

try:
    while True:
        #convert the ultrasonic numbers to inches
        front_distance = (us_front.distance - 0.01661) / 0.023205
        back_distance  = (us_back.distance - 0.01661)  / 0.023205
        if front_distance < 24.0 or back_distance < 24.0:
            speed.set_duty_cycle(0.0) #automatic braking system

        #turn signals
        if turnSignal > 6 and turnSignal < 8.3:
            light_state = not light_state
            GPIO.output(leftFLED, light_state)
            GPIO.output(leftBLED, light_state)
        elif turnSignal > 8.7:
            light_state = not light_state
            GPIO.output(rightFLED, light_state)
            GPIO.output(rightBLED, light_state)
        else:
            light_state = LIGHT_OFF
            GPIO.output(rightFLED, light_state)
            GPIO.output(rightBLED, light_state)
            GPIO.output(leftFLED,  light_state)
            GPIO.output(leftBLED,  light_state)

        time.sleep(0.01)
  
except KeyboardInterrupt:
    print('Got Keyboard Interrupt. Cleaning up and exiting')
    turn.stop(0.0)
    speed1.stop(0.0)
    speed2.stop(0.0)
    GPIO.cleanup()
    sys.exit()