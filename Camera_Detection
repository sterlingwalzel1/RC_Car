import cv2
import numpy as np

# Define color ranges for detection in HSV space

# Yellow range (Hue between 20 and 40)
lower_yellow = np.array([20, 100, 100])  # Lower bound of yellow
upper_yellow = np.array([40, 255, 255])  # Upper bound of yellow

# Green range (Hue between 40 and 90)
lower_green = np.array([40, 100, 100])  # Lower bound of green
upper_green = np.array([90, 255, 255])  # Upper bound of green

# Red range (Hue between 0-10 and 170-180)
# Lower Red (light red range)
lower_red1 = np.array([0, 120, 70])  # Lower bound of light red
upper_red1 = np.array([10, 255, 255])  # Upper bound of light red

# Upper Red (dark red range)
lower_red2 = np.array([170, 120, 70])  # Lower bound of dark red
upper_red2 = np.array([180, 255, 255])  # Upper bound of dark red

# Initialize the camera
cap = cv2.VideoCapture(0)  # 0 for the built-in camera, or adjust for other cameras

while True:
    # Capture each frame from the camera
    ret, frame = cap.read()
    
    if not ret:
        print("Failed to grab frame")
        break
    
    # Convert the captured frame from BGR to HSV (better for color detection)
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    
    # Create masks for yellow, green, and red colors
    mask_yellow = cv2.inRange(hsv, lower_yellow, upper_yellow)
    mask_green = cv2.inRange(hsv, lower_green, upper_green)
    
    # Red masks (two ranges)
    mask_red1 = cv2.inRange(hsv, lower_red1, upper_red1)  # Light red
    mask_red2 = cv2.inRange(hsv, lower_red2, upper_red2)  # Dark red
    
    # Combine the two red masks
    mask_red = cv2.bitwise_or(mask_red1, mask_red2)
    
    # Bitwise AND to isolate the colored areas in the frame
    result_yellow = cv2.bitwise_and(frame, frame, mask=mask_yellow)
    result_green = cv2.bitwise_and(frame, frame, mask=mask_green)
    result_red = cv2.bitwise_and(frame, frame, mask=mask_red)
    
    # Display the original frame and the color detection results
    cv2.imshow('Original Frame', frame)
    cv2.imshow('Yellow Detection', result_yellow)
    cv2.imshow('Green Detection', result_green)
    cv2.imshow('Red Detection', result_red)

    # Break the loop when the 'q' key is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the camera and close all windows
cap.release()
cv2.destroyAllWindows()

# use the camera Raspberry Pi Camera Module V2 (Official Camera)
# install openCV
#sudo apt update
#sudo apt install python3-opencv python3-numpy
