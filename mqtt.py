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
    #print('Subscribing to topic ', sub_topic_name)
    client.subscribe(pub_topic_name)

# this callback runs whenever a message is received
def on_message(client, userdata, msg):
    act = (float(msg.payload))
    print('Actvity = ', act)
    if act == 4:
        led.set_duty_cycle(100.0)
        print(1)
    elif act == 2:
        led.set_duty_cycle(50.0)
    elif act == 1:
        led.set_duty_cycle(25.0)
    else:
        led.set_duty_cycle(0.0)
    

# read command line arguemnts
numArgs = len(sys.argv)
my_name = sys.argv[1]
pub_topic_name = my_name + '/weather_station/actnum'

#intilaize MQTT
cilent = mqtt.Client()
cilent.on_connect = on_connect
cilent.on_message = on_message
cilent.connect("broker.emqx.io", 1883, 60)
cilent.loop_start()


try:
    while True:
        time.sleep(.1)


except KeyboardInterrupt:
    print('Got Keyboard Interrupt. Cleaning up and exiting')
    led.set_duty_cycle(100.0)
    GPIO.cleanup()
    sys.exit()