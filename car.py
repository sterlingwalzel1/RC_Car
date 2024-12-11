import RPi.GPIO as GPIO
import time
import sys
import os
import spidev
import paho.mqtt.client as mqtt
from gpiozero import DistanceSensor
from Camera_Detection import take_picture, detect_red, detect_yellow
import cv2

# Reboot time
time.sleep(60)

# Set up LED pins
leftFLED = 29
leftBLED = 31
rightFLED = 32
rightBLED = 33

sys.path.insert(0, '../utilities')
import utilities

# Configure ultrasonic sensor
us_front = DistanceSensor(echo=17, trigger=4,  threshold_distance=0.5)
us_back  = DistanceSensor(echo=27, trigger=22, threshold_distance=0.5)

# GPIO Setup
GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)
GPIO.setup(16, GPIO.OUT)
GPIO.setup(18, GPIO.OUT)
GPIO.setup(22, GPIO.OUT)
GPIO.setup(leftFLED,  GPIO.OUT)
GPIO.setup(leftBLED,  GPIO.OUT)
GPIO.setup(rightFLED, GPIO.OUT)
GPIO.setup(rightBLED, GPIO.OUT)

# PWM configuration for motor control
turn   = GPIO.PWM(16, 50)
turn.start(8.5)
speed1 = GPIO.PWM(18, 1000)
speed1.start(0)
speed2 = GPIO.PWM(22, 1000)
speed2.start(0)

# Default light state
light_state = ['LIGHT_OFF', 'LIGHT_ON']
turnSignal = 8.5
speed = 0

# MQTT setup
# this callback runs once when the client connects with the broker
def on_connect(client, userdata, flags, rc):
    print(f"Connected with result code {rc}", flush = True)
    client.subscribe(sub_topic_name)

# this callback runs whenever a message is received
def on_message(client, userdata, msg):
    global turnSignal, speed
    try:
        act = float(msg.payload)    
        if act == 259:
            if speed > 0:
                if speed <= 80:
                    speed += 4
                    speed1.ChangeDutyCycle(speed)
            else:
                speed1.ChangeDutyCycle(0)
                speed += 4
                speed2.ChangeDutyCycle(speed * -1)
        elif act == 258:
            if speed > 0:
                speed2.ChangeDutyCycle(0)
                speed -= 4
                speed1.ChangeDutyCycle(speed)
            else:
                speed1.ChangeDutyCycle(0)
                if speed > -80:
                    speed -= 4
                    speed2.ChangeDutyCycle(speed * -1)
        elif act == 260:
            if 6.5 < turnSignal:
                turnSignal -= 0.4
                turn.ChangeDutyCycle(turnSignal)
        elif act == 261:
            if 11.2 > turnSignal:
                turnSignal += 0.4
                turn.ChangeDutyCycle(turnSignal)
        elif act == 32:
            speed = 0
            speed1.ChangeDutyCycle(0)
            speed2.ChangeDutyCycle(0)

    except ValueError:
        print("Received invalid data.", flush = True)


    
# Read command line arguments
numArgs = len(sys.argv)
my_name = sys.argv[1]
sub_topic_name = my_name + '/home/dutycycle'

# Initialize MQTT Client
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.connect("broker.emqx.io", 1883, 60)
client.loop_start()

# Main logic for distance sensing and image processing
try:
    while True:
        # Capture an image and process it
        take_picture("captured_image.jpg")
        image = cv2.imread("captured_image.jpg")
        # Detect colors
        red_detected = detect_red(image)
        yellow_detected = detect_yellow(image)

        # Apply automatic braking if red is detected
        if red_detected:
            speed1.ChangeDutyCycle(0.0)
            speed2.ChangeDutyCycle(0.0)
        # Adjust speed if yellow is detected
        if yellow_detected:
            speed1.ChangeDutyCycle(speed / 2.0)

        #convert the ultrasonic numbers to inches
        front_distance = (us_front.distance - 0.01661) / 0.023205
        back_distance  = (us_back.distance -  0.01661) / 0.023205
        if front_distance < 12.0:
            speed = 0
            speed1.set_duty_cycle(0.0) # Can't go forwards anymore
        elif back_distance < 12.0:
            speed = 0
            speed2.set_duty_cycle(0.0) # Can't go backwards anymore

        if 6 < turnSignal < 8.2:
            GPIO.output(leftFLED,  True)
            GPIO.output(leftBLED,  True)
            GPIO.output(rightFLED, False)
            GPIO.output(rightBLED, False)
        elif turnSignal > 8.8:
            GPIO.output(rightFLED, True)
            GPIO.output(rightBLED, True)
            GPIO.output(leftFLED,  False)
            GPIO.output(leftBLED,  False)
        else:
            GPIO.output(leftFLED,  False)
            GPIO.output(leftBLED,  False)
            GPIO.output(rightFLED, False)
            GPIO.output(rightBLED, False)

        time.sleep(0.01)
  
except KeyboardInterrupt:
    print('Exiting due to KeyboardInterrupt...', flush = True)
    turn.stop()
    speed1.stop()
    speed2.stop()
    GPIO.cleanup()
    sys.exit()
