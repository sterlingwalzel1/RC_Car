from picamera2 import Picamera2
import time
import cv2
import numpy as np

def take_picture(filename="captured_image.jpg"):
    try:
        # Initialize Picamera2 object
        picam2 = Picamera2()

        # Allow time for the camera to initialize
        time.sleep(2)

        # Create and configure the camera preview configuration
        camera_config = picam2.create_preview_configuration()
        picam2.configure(camera_config)

        # Start the camera
        picam2.start()

        # Capture the image and save it
        picam2.capture_file(filename)
        print(f"Image saved as {filename}")

        # Stop the camera after capturing the image to avoid it being in the Running state
        picam2.stop()
        print("Camera stopped successfully.")

        # Explicitly release resources
        picam2.close()
        print("Camera resources released.")

    except Exception as e:
        print(f"An error occurred while capturing the image: {e}")

def detect_red(image, threshold=0.5):
    """
    Detects if at least `threshold` percentage of the image is red.
    Returns True if at least 50% of the image is red, else False.
    """
    # Convert the image from BGR (OpenCV's default) to HSV
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    # Define the range for detecting red color (higher thresholds)
    lower_red1 = np.array([0, 150, 100])  # Higher saturation and value for red
    upper_red1 = np.array([10, 255, 255])
    
    lower_red2 = np.array([170, 150, 100])  # Higher saturation and value for red
    upper_red2 = np.array([180, 255, 255])

    # Create masks for red color
    mask_red1 = cv2.inRange(hsv, lower_red1, upper_red1)
    mask_red2 = cv2.inRange(hsv, lower_red2, upper_red2)
    mask_red = cv2.bitwise_or(mask_red1, mask_red2)

    # Calculate the percentage of red pixels in the image
    total_pixels = image.shape[0] * image.shape[1]
    red_pixels = np.count_nonzero(mask_red)
    
    red_percentage = red_pixels / total_pixels

    # If red makes up more than 50% of the image, return True
    if red_percentage >= threshold:
        return True
    else:
        return False

def detect_yellow(image, threshold=0.5):
    """
    Detects if at least `threshold` percentage of the image is yellow.
    Returns True if at least 50% of the image is yellow, else False.
    """
    # Convert the image from BGR (OpenCV's default) to HSV
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    # Define the range for detecting yellow color (higher thresholds)
    lower_yellow = np.array([20, 150, 150])  # Higher saturation and value for yellow
    upper_yellow = np.array([40, 255, 255])

    # Create masks for yellow color
    mask_yellow = cv2.inRange(hsv, lower_yellow, upper_yellow)

    # Calculate the percentage of yellow pixels in the image
    total_pixels = image.shape[0] * image.shape[1]
    yellow_pixels = np.count_nonzero(mask_yellow)
    
    yellow_percentage = yellow_pixels / total_pixels

    # If yellow makes up more than 50% of the image, return True
    if yellow_percentage >= threshold:
        return True
    else:
        return False

if __name__ == "__main__":
    # Run the picture capture and detection in the main block
    filename = "test.jpg"
    take_picture(filename)

    # Read the captured image
    image = cv2.imread(filename)

    # Check if the image was successfully captured
    if image is None:
        print("Failed to load image")
        exit()

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
