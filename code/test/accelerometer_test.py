from ..custom_libs.mpu9250.mpu9250 import mpu9250
from matplotlib import pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
from collections import deque


# If true, then accelerometer readings will be plotted. Will not be plotted if false.
PLOT = True

# Initialize sensor with external library class.
sensor = mpu9250()


if __name__ == "__main__":

    # Setup plotting if necessary.
    if PLOT is True:

        # 3D scatter plot setup.
        fig2 = plt.figure()
        ax2 = Axes3D(fig2)
        ax2.set_xlim(-10, 10)
        ax2.set_ylim(-10, 10)
        ax2.set_zlim(-10, 10)
        plot2 = ax2.scatter3D([], [], [])
        plt.pause(1)

        # Buffer to hold points we want to show.
        points_to_show = [deque(maxlen=10), deque(maxlen=10), deque(maxlen=10)]

    while True:

        sensor_data = sensor.accel

        print(sensor_data)

        # Update the plot if plotting is turned on.
        if PLOT is True:
            points_to_show[0].append(sensor_data[0])
            points_to_show[1].append(sensor_data[1])
            points_to_show[2].append(sensor_data[2])
            frame = ax2.scatter3D(*points_to_show, color='blue')

            plt.pause(0.00000001)
            frame.remove()
