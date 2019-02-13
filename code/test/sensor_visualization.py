from matplotlib import pyplot as plt
import numpy as np


def a_random_sequence():
    for i in range(0, 1000):
        yield 5*np.random.rand()*np.sin(i)


if __name__ == "__main__":

    # Index for plotting.
    i = 0

    # Some setup to make rendering of plot faster.
    #fig, ax = plt.subplot()

    # Plot a sequence sequentially (not all at once).
    for x in a_random_sequence():
        plt.scatter(i, x)
        i = i + 1

plt.show()
