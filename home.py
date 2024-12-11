import time
import sys
import os
sys.path.insert(0, '../utilities')
import utilities
import curses
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
def keyboard_input(stdscr):
    stdscr.clear()
    stdscr.addstr("Enter desired Turn or Speed: ")
    stdscr.refresh()
    key = stdscr.getch()
    stdscr.refresh()
    stdscr.getch()
    return key

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


def main(stdscr):
    stdscr.clear()
    count = 0
    while True:
        if count % 3 == 0:
            stdscr.clear()
        stdscr.addstr("\nPress any key to continue...")
        stdscr.refresh()
        key_pressed = stdscr.getch()
        stdscr.addstr(f"\nYou pressed: {int(key_pressed)}")
        stdscr.refresh()
        client.publish(pub_topic_name, payload=key_pressed, qos=0, retain=False)
        count += 1
        time.sleep(.1)


curses.wrapper(main)
