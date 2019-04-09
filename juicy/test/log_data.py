import os
import time
import json
import urllib.request
import urllib.parse
import random #from mpu9250.mpu9250 import mpu9250

# API write key.
THINGSPEAK_API_KEY = "797UKWN6FJXVHF6O"

# Free ThingSpeak limits to 1 API request every 15 seconds. For bulk update (i.e. multiple data points per
# API request), only 960 data points may be included.
SEND_DELAY    = 15
MEASURE_DELAY = SEND_DELAY / (960)
REQUEST_URL = "https://api.thingspeak.com/channels/753579/bulk_update.json"


def bulk_update_channel(write_data):
    # Format the input data into JSON format.
    data = {'write_api_key': THINGSPEAK_API_KEY,
            'updates'      : write_data}

    data = json.dumps(data).encode('utf-8')

    # Form the http request using urllib2.
    req = urllib.request.Request(url=REQUEST_URL)
    request_headers = {"User-Agent": "mw.doc.bulk-update (Raspberry Pi)",
                       "Content-Type": "application/json",
                       "Content-Length": str(len(data))}

    # Set http request headers.
    for key, val in request_headers.items():
        req.add_header(key, val)

    # Actually make the request to ThingSpeak.
    urllib.request.urlopen(req, data=data)


if __name__ == "__main__":

    # Initialize sensor with external library class.
    #sensor = mpu9250()

    # Keep track of measurement and API request timing.
    last_send_time          = time.time()
    last_measurement_time   = time.time()

    # Initialize measurement buffer.
    measurement_buffer = []

    # Main loop.
    while True:

        # Only make measurement if it is time to. Limited by ThingSpeak unpaid API.
        if (time.time() - last_measurement_time) >= MEASURE_DELAY:

            # Current accelerometer reading.
               #reading = sensor.accel
            reading = [random.uniform(0, 1), random.uniform(0, 1), random.uniform(0, 1)]

            # Store data to measurement buffer.
            measurement_buffer.append({'delta_t': 1,
                                       'field1': reading[0],
                                       'field2': reading[1],
                                       'field3': reading[2]})

            # Update last measurement time to now.
            last_measurement_time = time.time()



        # Make url request every WAIT_TIME seconds.
        if (time.time() - last_send_time) >= SEND_DELAY:
            # Send bulk update, clear measurement buffer, and update timing information.
            bulk_update_channel(measurement_buffer)
            measurement_buffer = []
            last_send_time = time.time()
