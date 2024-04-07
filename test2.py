from dronekit import connect, VehicleMode
import time

def print_vehicle_state(vehicle, telemetry_name):
    print("Telemetry: %s" % telemetry_name)
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

# Connect to the first vehicle (telemetry 1)
print("Connecting to vehicle 1...")
vehicle1 = connect('/dev/ttyUSB0', baud=57600, wait_ready=False)

# Connect to the second vehicle (telemetry 2)
print("Connecting to vehicle 2...")
vehicle2 = connect('/dev/ttyACM1', baud=57600, wait_ready=False)

try:
    # Display some vehicle attributes for both vehicles
    print_vehicle_state(vehicle1, "Telemetry 1")
    print_vehicle_state(vehicle2, "Telemetry 2")

    # Change mode to STABILIZE for both vehicles
    print("Changing mode to STABILIZE for vehicle 1.")
    vehicle1.mode = VehicleMode("STABILIZE")
    print("Changing mode to STABILIZE for vehicle 2.")
    vehicle2.mode = VehicleMode("STABILIZE")

    # Wait for changes in state
    while True:
        # Print the current state for both vehicles every second
        print_vehicle_state(vehicle1, "Telemetry 1")
        print_vehicle_state(vehicle2, "Telemetry 2")
        time.sleep(1)

except KeyboardInterrupt:
    print("Exiting due to keyboard interrupt.")

finally:
    # Close vehicle objects before exiting script
    vehicle1.close()
    vehicle2.close()
    print("Vehicle connections closed.")

