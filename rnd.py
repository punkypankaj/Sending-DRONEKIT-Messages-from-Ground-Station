from dronekit import connect, VehicleMode, LocationGlobalRelative
from pymavlink import mavutil
import time
import argparse
import numpy as np
import cv2
from cv2 import aruco

cap = cv2.VideoCapture(0)

parser = argparse.ArgumentParser()
parser.add_argument('--connect', default='127.0.0.1:14550')
args = parser.parse_args()

# Connect to the Vehicle
print('Connecting to vehicle on: %s' % args.connect)
vehicle = connect(args.connect, baud=921600, wait_ready=True)

# Function to arm and then takeoff to a user-specified altitude
def arm_and_takeoff(aTargetAltitude):
    while not vehicle.is_armable:
        time.sleep(1)

    vehicle.mode = VehicleMode("GUIDED")
    vehicle.armed = True

    while not vehicle.armed:
        time.sleep(1)

    vehicle.simple_takeoff(aTargetAltitude)

    while True:
        if vehicle.location.global_relative_frame.alt >= aTargetAltitude * 0.95:
            break
        time.sleep(1)

# Function to set velocity in the north direction
def set_velocity_north(velocity):
    msg = vehicle.message_factory.set_position_target_local_ned_encode(
        0, 0, 0,
        mavutil.mavlink.MAV_FRAME_LOCAL_NED,
        0b0000111111000111,
        0, 0, 0,
        velocity, 0, 0,
        0, 0, 0,
        0, 0
    )
    vehicle.send_mavlink(msg)
    vehicle.flush()

# Function to set velocity in the east direction
def set_velocity_east(velocity):
    msg = vehicle.message_factory.set_position_target_local_ned_encode(
        0, 0, 0,
        mavutil.mavlink.MAV_FRAME_LOCAL_NED,
        0b0000111111000111,
        0, 0, 0,
        0, velocity, 0,
        0, 0, 0,
        0, 0
    )
    vehicle.send_mavlink(msg)
    vehicle.flush()

# Function to set yaw in degrees (0-360)
def set_yaw(yaw):
    msg = vehicle.message_factory.set_position_target_local_ned_encode(
        0, 0, 0,
        mavutil.mavlink.MAV_FRAME_LOCAL_NED,
        0b0000111111000111,
        0, 0, 0,
        0, 0, 0,
        0, 0, 0,
        np.radians(yaw), 0
    )
    vehicle.send_mavlink(msg)
    vehicle.flush()

# Variables for marker detection and flight
takeoff_target_marker_id = 7
landing_target_marker_id = 53
forward_marker_id = 10
backward_marker_id = 9
left_marker_id = 19
right_marker_id = 20
yaw_left_marker_id = 29
yaw_right_marker_id = 30
has_taken_off = False

# Create a named window for displaying the camera feed with resizable flag
cv2.namedWindow('Camera Feed', cv2.WINDOW_NORMAL)

# Set the window to normal (resizable) size
cv2.resizeWindow('Camera Feed', 800, 600)  # Set your desired initial size

# Wait for marker 7 to initiate takeoff
while True:
    ret, frame = cap.read()

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    aruco_dict = aruco.Dictionary_get(aruco.DICT_4X4_100)
    parameters = aruco.DetectorParameters_create()
    corners, ids, rejectedImgPoints = aruco.detectMarkers(gray, aruco_dict, parameters=parameters)
    frame_markers = aruco.drawDetectedMarkers(frame.copy(), corners, ids)

    # Display the camera feed with detected markers
    cv2.imshow('Camera Feed', frame_markers)

    if ids is not None and takeoff_target_marker_id in ids and not has_taken_off:
        print("Takeoff marker detected. Initiating takeoff.")
        arm_and_takeoff(2)
        has_taken_off = True

    if ids is not None and landing_target_marker_id in ids:
        print("Landing marker detected. Initiating landing.")
        vehicle.mode = VehicleMode("RTL")
        break

    if has_taken_off:
        if ids is not None and forward_marker_id in ids:
            print("Forward marker detected. Moving forward.")
            set_velocity_north(1.0)

        elif ids is not None and backward_marker_id in ids:
            print("Backward marker detected. Moving backward.")
            set_velocity_north(-1.0)

        elif ids is not None and left_marker_id in ids:
            print("Left marker detected. Moving left.")
            set_velocity_east(-1.0)

        elif ids is not None and right_marker_id in ids:
            print("Right marker detected. Moving right.")
            set_velocity_east(1.0)

        elif ids is not None and yaw_left_marker_id in ids:
            print("Yaw left marker detected. Turning left.")
            set_yaw(vehicle.heading + 20)

        elif ids is not None and yaw_right_marker_id in ids:
            print("Yaw right marker detected. Turning right.")
            set_yaw(vehicle.heading - 20)

        else:
            # Stop the drone by setting velocities and yaw to zero
            set_velocity_north(0.0)
            set_velocity_east(0.0)
            set_yaw(vehicle.heading)

    if cv2.waitKey(1) & 0xFF == ord('q'):  # Press 'q' to exit the loop
        break

# Release the camera
cap.release()

# Close the vehicle object
vehicle.close()

# Close OpenCV windows
cv2.destroyAllWindows()

