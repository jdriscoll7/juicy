import time
import numpy as np


class SensorModel:
    """
    Basic sensor model to keep rough estimation of orientation
    under certain assumptions. May not be needed if sensor is
    assumed to never flip over...

    - Current capabilities
        - Estimate rotational orientation based on integrating over
          gyro measurements.
        - State estimation used to more robustly subtract gravity
          component from accelerometer measurements.

    - Notes
        - Internal orientation is based on starting orientation. It's
          not worth the trouble of estimating starting orientation!
    """

    def __init__(self):
        """
        - Initialized
            - orientation:      [0, 0, 0]
            - measurement_time: current time
        """

        # Orientations will be based off of initial orientation - this
        # assumes that sensor will start perpendicular to Earth.
        self.orientation = np.asarray([0, 0, 0], dtype=np.float64)

        # Initialize timing. Differences in time used for integration.
        self.measurement_time = time.time()

    def update_state(self, gyro, *args, **kwargs):
        """
        Takes gyroscope measurements to update internal state
        estimation. Currently no filters implemented. Something
        like unscented Kalman or particle filter would be dandy.

        :param gyro:    gyroscope measurement
        :param args:    unused
        :param kwargs:  unused
        :return:        current orientation estimate
        """

        # Calculate time difference between current and last measurement.
        dt = time.time() - self.measurement_time

        # Integrate over gyroscope measurement to estimate rotational
        # displacement. Filter should go here... (UKF or particle)
        self.orientation += (np.asarray(gyro) * dt)

        # Update measurement time to get ready for next measurement.
        self.measurement_time = time.time()

    def convert_accelerometer_measurement(self, measurement, sub_gravity=False):
        """
        Converts a raw accelerometer measurement into a measurement
        that considers orientation, which the model attempts to keep
        track of. Optionally remove gravity component from measurement
        for use in tests/drivers to minimize verbosity from caller.

        :param   measurement: Raw accelerometer measurement
        :param   sub_gravity: Option for subtracting gravity from measurement.
        :return:              Measurement with orientation estimate.
        """

        # Compute sines and cosines of each rotation angle to save repeated
        # computation in rotation matrix declaration below.
        sin_angles = np.sin(self.orientation * np.pi / 180)
        cos_angles = np.cos(self.orientation * np.pi / 180)

        # Define rotation inverse matrices for each axis.
        rotation_x = np.matrix([[1, 0, 0],
                                [0, cos_angles[0], -sin_angles[0]],
                                [0, -sin_angles[0], cos_angles[0]]]).T

        rotation_y = np.matrix([[cos_angles[1], 0, sin_angles[1]],
                                [0, 1, 0],
                                [-sin_angles[1], 0, cos_angles[1]]]).T

        rotation_z = np.matrix([[cos_angles[2], -sin_angles[2], 0],
                                [-sin_angles[2], cos_angles[2], 0],
                                [0, 0, 1]]).T

        # "Unrotate" the measurement based on orientation.
        #     - https://en.wikipedia.org/wiki/Rotation_matrix
        estimated_measurement = rotation_x*rotation_y*rotation_z*np.asarray(measurement)

        # Optionally return measurement with gravity compensation.
        if sub_gravity is True:
            estimated_measurement += (0, 0, 9.8)

        # Return the final estimated measurement based on internal state.
        return estimated_measurement
