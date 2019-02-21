from collections import deque

from matplotlib import pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np



def a_random_sequence():
    for i in range(0, 1000):
        yield 5*np.random.rand()*np.sin(i)


if __name__ == "__main__":

    # Index for plotting.
    i = 0

    # Some setup to make rendering of plot faster.
    fig2 = plt.figure()
    ax2 = Axes3D(fig2)
    ax2.set_xlim(-10, 10)
    ax2.set_ylim(-10, 10)
    ax2.set_zlim(-10, 10)
    plot2 = ax2.scatter3D([], [], [])

    plt.pause(1)

    # Buffer to hold points we want to show.
    points_to_show = [deque(maxlen=10), deque(maxlen=10), deque(maxlen=10)]

    # Plot a sequence sequentially (not all at once).
    for x in a_random_sequence():

        points_to_show[0].append(i)
        points_to_show[1].append(i)
        points_to_show[2].append(x)
        asd = ax2.scatter3D(*points_to_show, color='blue')

        plt.pause(0.00000001)
        asd.remove()


        # Increment plot index for demo purposes.
        i = i + 1

