import os
import RPi.GPIO as GPIO
from mpu9250.mpu9250 import mpu9250
from pushetta import Pushetta 
import time 


# Constants used in program - change these to change things like thresholds.
INCREASE_THRESH_X = 12
INCREASE_THRESH_Y = 6.5
INCREASE_THRESH_Z = 1.2


# Infinite loop to constantly send distress call
# every 2 seconds.
#
# Resume program by pressing physical button on
# breadboard.
def alert(p, CHANNEL_NAME):
    
    # Push message until button press.
    while GPIO.input(18) != 1:
        p.pushMessage(CHANNEL_NAME, "CHECK POOL!!!!")
        time.sleep(2)
        
    # Clear the three LED's used for different axis thresholding.
    GPIO.output(16, 0)
    GPIO.output(20, 0)
    GPIO.output(21, 0)

    
# Function that sets up all of the GPIO's used for this program.
def gpio_setup():
    
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(16, GPIO.OUT)
    GPIO.setup(20, GPIO.OUT)
    GPIO.setup(21, GPIO.OUT)
    GPIO.setup(18, GPIO.IN)
    GPIO.output(16, 0)
    GPIO.output(20, 0)
    GPIO.output(21, 0)
    
    
if __name__ == "__main__":

    # Initialize sensor with external library class.
    sensor = mpu9250()
    
    # Setup GPIO modes and initial values.
    gpio_setup()
    
    # Initialize first magnitude to 10 - this was it won't trigger immediately every time...
    last_mag_x = 10
    last_mag_y = 10
    last_mag_z = 10

    # Key taken from account.
    API_KEY = "fb2dc4530995b2fe3d3f823a0fa35a5e8d635716"
    
    # Name of channel.
    CHANNEL_NAME = "JuicySeniorDesign"
    
    # Create pushetta object.
    p = Pushetta(API_KEY)

    while True:
        
        # Get sensor data.
        sensor_data = sensor.accel

        # Clear console before printing new information.
        os.system('clear')

        # Print sensor data and the magnitude of the acceleration.
        next_mag_x = sensor_data[0]
        next_mag_y = sensor_data[1]
        next_mag_z = sensor_data[2]

        #print('sensor x: %3.3\nsensor y: %3.3f\nsensor z: %3.3f\n\nmagnitude: %3.3f', (*sensor_data, next_mag))
        print((sensor_data[0]),',',(sensor_data[1]),',',(sensor_data[2]))

        # Thresholding for alarm detection. Adjust magnitude for each axis.
        # Three different LED's are toggled based on which axis is triggered.
        if (INCREASE_THRESH_X * last_mag_x) < next_mag_x:
            GPIO.output(21, 1)
            alert(p, CHANNEL_NAME)
            
        if (INCREASE_THRESH_Y * last_mag_y) < next_mag_y:
            GPIO.output(20, 1)
            alert(p, CHANNEL_NAME)
            
        if (INCREASE_THRESH_Z * last_mag_z) < next_mag_z:
            GPIO.output(16, 1)
            alert(p, CHANNEL_NAME)

        # Set the next value to compare.
        last_mag_x = next_mag_x
        last_mag_y = next_mag_y
        last_mag_z = next_mag_z
