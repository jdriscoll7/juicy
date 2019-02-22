import sys
import os
sys.path.append('../')
#Setup GPIO 12 as OUTPUT
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(12, GPIO.OUT)
GPIO.setup(18, GPIO.IN)
GPIO.output(12, 0)
from juicy.mpu9250.mpu9250 import mpu9250
#from matplotlib import pyplot as plt
#from mpl_toolkits.mplot3d import Axes3D
import numpy as np
from collections import deque

arr = []
arr = [0.0, 0.0, 0.0]

# If true, then accelerometer readings will be plotted. Will not be plotted if false.
PLOT =False 

# Initialize sensor with external library class.
sensor = mpu9250()


if __name__ == "__main__":

    # Setup plotting if necessary.
    if PLOT is True:

        # 3D scatter plot setup.
        fig2 = plt.figure()
        ax2 = Axes3D(fig2)
        ax2.set_xlim(-1, 1)
        ax2.set_ylim(-1, 1)
        ax2.set_zlim(-1, 1)
        plot2 = ax2.scatter3D([], [], [])
        plt.pause(1)

        # Buffer to hold points we want to show.
        points_to_show = [deque(maxlen=10), deque(maxlen=10), deque(maxlen=10)]

    last_mag = 0

    while True:

        sensor_data = sensor.accel
        print(sensor_data)
        
        next_mag = np.linalg.norm(sensor_data)        

        if last_mag  < next_mag:
            GPIO.output(12, 1)
        else:
            GPIO.output(12, 0)

       
        last_mag = next_mag

       # if ((sensor_data[0] - arr[0]) >= .5) | ((sensor_data[1] - arr[1]) >= .8) | ((sensor_data[2] - arr[2]) >= 1):
       #   GPIO.output(12, 1)
        
        if GPIO.input(18) == 1:
          GPIO.output(12, 0)
        arr[0] = sensor_data[0]
        arr[1] = sensor_data[1]
        arr[2] = sensor_data[2]
        os.system('clear')

        # Update the plot if plotting is turned on.
        if PLOT is True:
            points_to_show[0].append(sensor_data[0])
            points_to_show[1].append(sensor_data[1])
            points_to_show[2].append(sensor_data[2])
            frame = ax2.scatter3D(*points_to_show, color='blue')

            plt.pause(0.00000001)
            frame.remove()
