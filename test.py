from dronekit import connect, VehicleMode
import time

def print_vehicle_state(vehicle):
    print("Mode: %s" % vehicle.mode.name)
    print("Armed: %s" % vehicle.armed)
    print("Altitude: %s" % vehicle.location.global_relative_frame.alt)
    print("GPS: %s" % vehicle.gps_0)
    print("Battery: %s" % vehicle.battery)
    print("Heading: %s" % vehicle.heading)
    print("Is Armable: %s" % vehicle.is_armable)
    print("Groundspeed: %s" % vehicle.groundspeed)
    print("Airspeed: %s" % vehicle.airspeed)
    print("")

# Connect to the vehicle without waiting for it to be ready
print("Connecting to vehicle...")
vehicle = connect('/dev/ttyUSB0', baud=57600, wait_ready=False)

try:
    # Display some vehicle attributes
    print_vehicle_state(vehicle)

    # Change mode to ALT_HOLD
    print("Changing mode to STABILIZE.")
    vehicle.mode = VehicleMode("STABILIZE")
    #mode will be changed once on startup

    
    # Wait for changes in state
    while True:
        # Print the current state every 1 seconds
        print_vehicle_state(vehicle)
        time.sleep(1)

except KeyboardInterrupt:
    print("Exiting due to keyboard interrupt.")

finally:
    # Close vehicle object before exiting script
    vehicle.close()
    print("Vehicle connection closed.")


