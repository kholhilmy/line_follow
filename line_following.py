from dronekit import connect, VehicleMode, LocationGlobalRelative
from pymavlink import mavutil
import cv2
import numpy as np

# Set the HSV range for the color of the line
lower_color = np.array([20, 100, 100])
upper_color = np.array([30, 255, 255])

# Initialize the camera
cap = cv2.VideoCapture(0)

# Set the frame size and FPS of the camera
cap.set(3, 640)
cap.set(4, 480)
cap.set(5, 30)

# Connect to the vehicle
vehicle = connect('udp:127.0.0.1:14550')

# Arm and takeoff the vehicle
vehicle.mode = VehicleMode("GUIDED")
vehicle.armed = True
vehicle.simple_takeoff(10)

# Start following the line
while True:
    # Read a frame from the camera
    ret, frame = cap.read()

    # Convert the frame to HSV color space
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Create a mask for the color of the line
    mask = cv2.inRange(hsv, lower_color, upper_color)

    # Apply some morphological operations to remove noise and fill gaps
    kernel = np.ones((5, 5), np.uint8)
    mask = cv2.erode(mask, kernel, iterations=2)
    mask = cv2.dilate(mask, kernel, iterations=2)

    # Find the contours of the line in the mask
    contours, hierarchy = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # If there is at least one contour, find the one with the largest area
    if len(contours) > 0:
        largest_contour = max(contours, key=cv2.contourArea)

        # Find the centroid of the largest contour
        M = cv2.moments(largest_contour)
        if M["m00"] != 0:
            cx = int(M["m10"] / M["m00"])
            cy = int(M["m01"] / M["m00"])
            cv2.circle(frame, (cx, cy), 5, (0, 0, 255), -1)

            # Control the vehicle using DroneKit
            if cx < 300:
                vehicle.channels.overrides['1'] = 1600
            elif cx > 340:
                vehicle.channels.overrides['1'] = 1400
            else:
                vehicle.channels.overrides['1'] = 1500

    # Show the frame with the line and the centroid
    cv2.imshow("Line Following", frame)

    # Exit the loop if the 'q' key is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Land and disarm the vehicle
vehicle.mode = VehicleMode("LAND")
time.sleep(5)
vehicle.armed = False

# Close the connection to the vehicle
vehicle.close()
