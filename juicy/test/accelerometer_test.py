#Setup GPIO 12 as OUTPUT
import RPi.GPIO as GPIO
from mpu9250.mpu9250 import mpu9250
from matplotlib import pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
from collections import deque


# If true, then accelerometer readings will be plotted. Will not be plotted if false.
PLOT = False 


if __name__ == "__main__":

    
    # Initialize sensor with external library class.
    sensor = mpu9250()
    
    # Marco's detection method setup.
    arr = [0.0, 0.0, 0.0]
    
    # Setup GPIO modes and initial values.
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(12, GPIO.OUT)
    GPIO.setup(18, GPIO.IN)
    GPIO.output(12, 0)

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

    # Initialize first magnitude to 10 - this was it won't trigger immediately every time...
    last_mag = 10

    while True:

        # Get sensor data.
        sensor_data = sensor.accel
        
        # Clear console before printing new information.
        os.system('clear')
        
        # Print sensor data and the magnitude of the acceleration.
        next_mag = np.linalg.norm(sensor_data)
        print('sensor x: %3.3\nsensor y: %3.3f\nsensor z: %3.3f\n\nmagnitude: %3.3f', (*sensor_data, next_mag))
   
        # Thresholding for alarm detection - uncomment else for software LED/alarm reset.
        if 1.4*last_mag  < next_mag:
            GPIO.output(12, 1)
       # else:
       #     GPIO.output(12, 0)

        # Set the next value to compare.
        last_mag = next_mag

       # Marco's detection method - uncomment to use this.
       # if ((sensor_data[0] - arr[0]) >= .5) | ((sensor_data[1] - arr[1]) >= .8) | ((sensor_data[2] - arr[2]) >= 1):
       #   GPIO.output(12, 1)
        
        # Allows LED to be reset by external input (currently button).
        if GPIO.input(18) == 1:
            GPIO.output(12, 0)
        
        # Marco's detection method.
        arr[0] = sensor_data[0]
        arr[1] = sensor_data[1]
        arr[2] = sensor_data[2]
       
        # Update the plot if plotting is turned on.
        if PLOT is True:
            points_to_show[0].append(sensor_data[0])
            points_to_show[1].append(sensor_data[1])
            points_to_show[2].append(sensor_data[2])
            frame = ax2.scatter3D(*points_to_show, color='blue')

            plt.pause(0.00000001)
            frame.remove()
