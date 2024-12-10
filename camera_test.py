# main_script.py
from Camera_Detection import take_picture, detect_red, detect_yellow
import cv2
import time

def main():
    while True:
        # Capture an image and save it as "captured_image.jpg"
        take_picture("captured_image.jpg")

        # Read the captured image
        image = cv2.imread("captured_image.jpg")

        # Check if the image was successfully captured
        if image is None:
            print("Failed to load image")
            break  # Exit the loop if image capture fails

        # Call the function to detect if at least 50% of the image is red
        red_detected = detect_red(image)

        # Call the function to detect if at least 50% of the image is yellow
        yellow_detected = detect_yellow(image)

        # Print the results
        if red_detected:
            print("At least 50% of the image is Red: True")
        else:
            print("At least 50% of the image is Red: False")

        if yellow_detected:
            print("At least 50% of the image is Yellow: True")
        else:
            print("At least 50% of the image is Yellow: False")

        # Wait for a short time before taking the next picture (e.g., 2 seconds)
        time.sleep(2)

# Run the main function
if __name__ == "__main__":
    main()
