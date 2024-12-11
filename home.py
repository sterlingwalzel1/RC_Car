import time
import sys
import os
sys.path.insert(0, '../utilities')
import utilities
#import keyboard
import paho.mqtt.client as mqtt
import RPi.GPIO as GPIO


# this callback runs once when the client connects with the broker
def on_connect(client, userdata, flags, rc):
    print(f"Connected with result code {rc}")

# this callback runs whenever a message is received
def on_message(client, userdata, msg):
    act = (float(msg.payload))
    print('Actvity = ', act)
    

# Function to check and return valid key presses
def get_key_input():
    # Define the valid keys
    valid_keys = ['up', 'down', 'left', 'right', 'space']

    # Check if any of the valid keys are pressed
    for key in valid_keys:
        if keyboard.is_pressed(key):
            return key  # Return the key that was pressed

    # If none of the valid keys are pressed, return None
    return None


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
        print("Enter desired Turn or Speed: ")
        key_pressed = get_key_input()  # Get the key pressed, or None if no key is pressed
        
        if key_pressed:  # If a valid key was pressed, output the key
            print(f"Key pressed: {key_pressed}")
        
        client.publish(pub_topic_name, payload=key_pressed, qos=0, retain=False)
        time.sleep(.1)


except KeyboardInterrupt:
    print('Got Keyboard Interrupt. Cleaning up and exiting')
    led.set_duty_cycle(100.0)
    GPIO.cleanup()
    sys.exit()



