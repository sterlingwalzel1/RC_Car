import time
import sys
import os
sys.path.insert(0, '../utilities')
import utilities
import paho.mqtt.client as mqtt
import RPi.GPIO as GPIO

led = utilities.HW_PWM(2000)
led.set_duty_cycle(0.0)

# this callback runs once when the client connects with the broker
def on_connect(client, userdata, flags, rc):
    print(f"Connected with result code {rc}")

# this callback runs whenever a message is received
def on_message(client, userdata, msg):
    act = (float(msg.payload))
    print('Actvity = ', act)
    

# read command line arguemnts
numArgs = len(sys.argv)
my_name = sys.argv[1]
pub_topic_name = my_name + '/home/dutycycle'

#intilaize MQTT
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.connect("broker.emqx.io", 1883, 60)
client.loop_start()


try:
    while True:
        action = (float(input("Enter desired Turn or Speed: ")))
        client.publish(pub_topic_name, payload=action, qos=0, retain=False)
        time.sleep(.1)


except KeyboardInterrupt:
    print('Got Keyboard Interrupt. Cleaning up and exiting')
    led.set_duty_cycle(100.0)
    GPIO.cleanup()
    sys.exit()



