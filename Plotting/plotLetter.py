import serial
from math import *
import numpy as np
from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits.axes_grid1 import make_axes_locatable
import matplotlib.pyplot as plt

# connect to serial port
arduinoComPort = '/dev/ttyACM0'

# Set the baud rate
baudRate = 9600

# open the serial port
serialPort = serial.Serial(arduinoComPort, baudRate, timeout=1)

# initialize sets of x, y, z points
X, Y, z = list(), list(), list()

# make theta lists for axes
thetas1 = np.arange(-10, 11)
thetas2 = np.arange(-12, 21)

# numpy array for distance axis
Z = np.array([])

zCounter = 0
rowCounter = 0

# main loop to read data from the Arduino, process it, and plot it
while True:
  # read one line of data from serial monitor
  lineOfData = serialPort.readline().decode()

  # check if data was received
  if len(lineOfData) > 0:
    # data was received, convert it into 3 floats
    val, theta1, theta2 = (x for x in lineOfData.split(','))

    # convert angles to -90 to 90 rather than 0 to 180
    theta1 = radians((int(theta1) - 90))
    theta2 = radians((int(theta2) - 90))

    # calculate IR sensor distance
    r = ((float(val) + 5.39) / 11786) ** -1

    # store respective points in their lists
    z.append(r*cos(theta2)*cos(theta1))

    zCounter += 1
    if zCounter == 33 and Z.size != 0:
      Z = np.hstack((Z, np.array(z)[np.newaxis].T))

      if (rowCounter == 20):
        break
      else:
        rowCounter += 1

      z = list()
      zCounter = 0

    elif zCounter == 33:
      Z = np.array(z)[np.newaxis].T

      rowCounter += 1

      z = list()
      zCounter = 0

fig, ax = plt.subplots()
im = ax.imshow(np.divide(Z, np.max(Z)))

#We want to show all ticks...
ax.set_xticks(np.arange(len(thetas1)))
ax.set_yticks(np.arange(len(thetas2)))
#... and label them with the respective list entries
ax.set_xticklabels(thetas1)
ax.set_yticklabels(np.multiply(thetas2, -1))

# label axes

ax.set_xlabel('Pan Angle of Sensor Relative to Letter (Degrees)')
ax.set_ylabel('Tilt Angle of Sensor Relative to Letter (Degrees)')

divider = make_axes_locatable(ax)
cax = divider.append_axes('right', size='5%', pad=0.05)
cbar = fig.colorbar(im, cax=cax, orientation='vertical')
cbar.ax.set_ylabel('Normalized Distance From Sensor')

# Rotate the tick labels and set their alignment.
plt.setp(ax.get_xticklabels(), rotation=45, ha="right",
         rotation_mode="anchor")

ax.set_title("3D Scan of Cardboard Letter 'E'")
fig.tight_layout()
plt.show()
