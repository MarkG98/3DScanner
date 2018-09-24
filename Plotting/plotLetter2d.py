import serial
from math import *
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt


# connect to serial port
arduinoComPort = '/dev/ttyACM0'

# Set the baud rate
baudRate = 9600

# open the serial port
serialPort = serial.Serial(arduinoComPort, baudRate, timeout=1)

# initialize sets of x, y, z points
X, Y, Z = list(), list(), list()

theta2 = 0

# main loop to read data from the Arduino, process it, and plot it
while True:
  # read one line of data from serial monitor
  lineOfData = serialPort.readline().decode()

  #TODO convert angles from [0, 180] to [-90, 90]

  # check if data was received
  if len(lineOfData) > 0:
    # data was received, convert it into 3 floats
    val, theta1 = (x for x in lineOfData.split(','))

    theta1 = radians((int(theta1) - 90))
    r = ((float(val) + 5.39) / 11786) ** -1

    print(theta1)

    # store respective points in their lists
    X.append(r*cos(theta2)*sin(theta1))
    Y.append(r*sin(theta2))
    Z.append(r*cos(theta2)*cos(theta1))

    if (theta1 == radians(-20)):
      break

fig = plt.figure()
ax = fig.add_subplot(111, projection=None)

ax.scatter(X, Z, c='r', marker='o')

ax.set_xlabel('Horizontal Distance From IR Sensor (cm)')
ax.set_ylabel('Vertical Distance From IR Sensor (cm)')
ax.set_title('Top Down View of Sweep Across Letter')

plt.show()
