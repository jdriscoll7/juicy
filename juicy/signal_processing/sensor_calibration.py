import time
import numpy as np


class SensorModel:
    """
    Basic sensor model to keep rough estimation of orientation
    under certain assumptions. May not be needed if sensor is
    assumed to never flip over...
    
    This model is designed specifically to work for the MPU9250 
    package used throughout the project. See requirements.txt.
    
    This could be made more generic, but much simplicity would
    need to be sacrified for generality.

    - Current capabilities
        - Estimate rotational orientation based on integrating over
          gyro measurements.
        - State estimation used to more robustly subtract gravity
          component from accelerometer measurements.
        - Determine mean gyroscope error on startup.

    - Notes
        - Internal orientation is based on starting orientation. It's
          not worth the trouble of estimating starting orientation!
    """

    def __init__(self, moving_average_size=500):
        """
        - Initialized
            - orientation:      [0, 0, 0]
            - measurement_time: current time
        """

        # Orientations will be based off of initial orientation - this
        # assumes that sensor will start perpendicular to Earth.
        self.orientation = np.asarray([0, 0, 0], dtype=np.float64)

        # Initialize timing. Differences in time used for integration.
        self.first_measurement = True

        # Initialize some information about gyroscope bias correction.
        self.gyro_bias = np.asarray([0, 0, 0])
        self.gyro_bias_fixed = False
        
        # Moving average is used to eliminate steady error.
        self.moving_average = np.asarray([0, 0, 0])
        self.moving_average_buffer = []
        self.moving_average_size = moving_average_size

    def correct_gyro_error(self, sensor, processing_time=5, *args, **kwargs):
        """
        Computes the mean steady error of the sensor's gyro measurements.
        This is used in later computation to correct for any latent error
        in the gyroscope itself.

        :param sensor:           MPU9250 sensor object (gyro attribute is used)
        :param processing_time:  time to determine mean error in seconds
        :param args:             unused
        :param kwargs:           unused
        :return:                 nothing
        """

        # Get beginning time.
        beginning_time = time.time()

        # Measurements sum and number of measurements for mean computation.
        measurement_sum = np.asarray([0, 0, 0], dtype=np.float64)
        num_measurements = 0
        
        # Sum up measurements until time difference reaches processing_time input.
        while (time.time() - beginning_time) < processing_time:
            
            # Don't worry about arithmetic overflow - Python deals with that :).
            measurement_sum += np.asarray(sensor.gyro)
            num_measurements += 1
            
        # Set the gyroscope bias and the fact that gyro has been corrected.
        self.gyro_bias = measurement_sum / num_measurements
        self.gyro_bias_fixed = True
        
        # Initialize moving average buffer with "moving_average_size" copies of the computed average.
        self.moving_average_buffer = [self.gyro_bias for i in range(self.moving_average_size + 1)]
        self.moving_average = self.gyro_bias
        
        # Restart measurement timer. This function takes a long time!
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
        
        # Ignores dt for first measurement to prevent errors from latency in setup and sampling.
        if self.first_measurement is True:
            dt = 0
            self.first_measurement = False
        else:
            # Calculate time difference between current and last measurement.
            dt = time.time() - self.measurement_time

        # The sensor's axes do not obey right hand rule.
        # This is fixed by reverse-orienting x and y axes.
        rhr_compensation = np.asarray([-1, -1, 1])

        # Integrate over gyroscope measurement to estimate rotational
        # displacement. Filter should go here... (UKF or particle)
        # 
        # Also correct for gyro error if possible.
        gyro_val = np.asarray(gyro)
        
        if self.gyro_bias_fixed is True:
            
            # Compute discrete integral.
            integrand = (gyro_val - self.moving_average) * dt
            
            # Offset orientation by difference and correct for RHR.
            self.orientation += (rhr_compensation * integrand)
            
        else:
            
            # Compute discrete integral.
            integrand = (gyro_val * dt)
            
            # Offset orientation by difference and correct for RHR.
            self.orientation -= (rhr_compensation * integrand)
            print('Gyroscope error is not being fixed - uh oh.')
        
        # Update measurement time to get ready for next measurement.
        self.measurement_time = time.time()
        
        # Update moving average.
        self.update_moving_average(gyro_val)
        
        # Return orientation. Not really used at the moment.
        return self.orientation

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
                                [0, sin_angles[0], cos_angles[0]]]).T

        rotation_y = np.matrix([[cos_angles[1], 0, sin_angles[1]],
                                [0, 1, 0],
                                [-sin_angles[1], 0, cos_angles[1]]]).T

        rotation_z = np.matrix([[cos_angles[2], -sin_angles[2], 0],
                                [sin_angles[2], cos_angles[2], 0],
                                [0, 0, 1]]).T

        # "Unrotate" the measurement based on orientation.
        #     - https://en.wikipedia.org/wiki/Rotation_matrix
        estimated_measurement = rotation_x*rotation_y*rotation_z*np.matrix(measurement).T

        # Optionally return measurement with gravity compensation.
        if sub_gravity is True:
            estimated_measurement -= np.asmatrix((0, 0, 1)).T

        # Return the final estimated measurement based on internal state.
        return estimated_measurement

    def update_moving_average(self, new_sample):
        """
        Updates the moving average used by the internal gyroscope measurements.
        
        Expects self.moving_average_buffer to be full - this is done in initialization.
        """
        
        # Compute current moving average value.
        self.moving_average = ((self.moving_average_size * self.moving_average) 
                               - self.moving_average_buffer[0] 
                               + new_sample) / self.moving_average_size
    
        # Update moving average buffer for next update. (remove first element and add sample to end)
        self.moving_average_buffer.pop(0)
        self.moving_average_buffer.append(new_sample)    
