# Sending DRONEKIT Messages from Ground Station

1. Use test.py to check the setup by connecting the ground telemetry module to Raspberry pi or computer USB port and airunit to the pixhawk drone. Check baud-rate and assigned usb port in terminal using command:
ls /dev/tty*
2. Use test2.py to check the setup for sending data from rpi or computer to multiple drones. In this codes two drones are connected and data is sent.
3. If you are planning to control multople drones from single ground control station and at  longer ranger then you can use radio module which has meshing capabalities just like master and slave nodes and using slave id number you can pass the data that particular drone from master node also you can have synchronisation between all the drones connected to the master and perform task without collision.

