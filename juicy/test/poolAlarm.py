import os
import RPi.GPIO as GPIO
from mpu9250.mpu9250 import mpu9250
from pushetta import Pushetta 
import time 


# Constants used in program - change these to change things like thresholds.
Z_THRESHOLD = 0.08

# Global variable because lazy - value that threshold is relative to.
start_value = 0.98

# Infinite loop to constantly send distress call
# every 2 seconds.
#
# Resume program by pressing physical button on
# breadboard.
def alert(p, CHANNEL_NAME, sensor):
    
    # Shake device hard to reset after alarm trigger.
    Z_RESET = 1.8
    
    # Push message until button press.
    while (sensor.accel[2] < Z_RESET):
        p.pushMessage(CHANNEL_NAME, "CHECK POOL!!!!")
        time.sleep(2)
        
    # Turn off alarm and reset threshold starting value.
    time.sleep(15)
    start_value = sensor.accel[2]
    
    
if __name__ == "__main__":

    # Initialize sensor with external library class.
    sensor = mpu9250()
    
    # Key taken from account.
    API_KEY = "fb2dc4530995b2fe3d3f823a0fa35a5e8d635716"
    
    # Name of channel.
    CHANNEL_NAME = "JuicySeniorDesign"
    
    # Create pushetta object.
    p = Pushetta(API_KEY)

    data_max = 0
    
    while True:
        
        # Get sensor data.
        data = sensor.accel[2]

        # Look at new max value.
        if data > data_max:
            data_max = data
            
        # Thresholding for alarm detection. Adjust magnitude for each axis.           
        if (data_max >= (start_value + Z_THRESHOLD)):
            alert(p, CHANNEL_NAME, sensor)
