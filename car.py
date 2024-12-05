import RPi.GPIO as GPIO
import time
import sys
import os
import spidev
import paho.mqtt.client as mqtt
from gpiozero import DistanceSensor

sys.path.insert(0, '../utilities')
import utilities


#ultrasonic sensor config
us_front = DistanceSensor(echo=17, trigger=4,  threshold_distance=0.5)
us_back  = DistanceSensor(echo=27, trigger=22, threshold_distance=0.5)

#GPIO configuration
GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)

#configure duty cycles
turn = utilities.HW_PWM(50)
turn.set_duty_cycle(0.0)
speed = utilities.HW_PWM(2000)
speed.set_duty_cycle(0.0) 

# this callback runs once when the client connects with the broker
def on_connect(client, userdata, flags, rc):
    print(f"Connected with result code {rc}")
    client.subscribe(sub_topic_name)

# this callback runs whenever a message is received
def on_message(client, userdata, msg):
    act = (float(msg.payload))
    print(act)
    if (act > 100 and act < 1000) or act > 1100 or act < 0:
        print("DIPSHIT THAT DON'T WORK")
    if act < 1000:
       turn.set_duty_cycle(act) 
    else:
        act = act % 1000
        speed.set_duty_cycle(act) 

    
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
        if front_distance < 24.0 or back_distance < 24.0
            speed.set_duty_cycle(0.0) #automatic braking system

        time.sleep(0.1)
  
except KeyboardInterrupt:
    print('Got Keyboard Interrupt. Cleaning up and exiting')
    turn.set_duty_cycle(0.0)
    speed.set_duty_cycle(0.0)
    GPIO.cleanup()
    sys.exit()