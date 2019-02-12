from mpu9250.mpu9250.mpu9250 import mpu9250

sensor = mpu9250()

while True:

    print(sensor.accel)
