import os
import time
import json
import urllib.request
import urllib.parse
from mpu9250.mpu9250 import mpu9250


# Some constants used in main loop.
THINGSPEAK_API_KEY = '797UKWN6FJXVHF6O' # API write key for ThingSpeak.
WAIT_TIME          = 20                 # Update time in seconds for ThingSpeak (15s minimum)
REQUEST_URL        = "https://api.thingspeak.com/channels/juicy_logging/bulk_update.json"

def bulk_update_channel(write_data):
    
    # Format the input data into JSON format.
    data = json.dumps({'write_api_key': THINGSPEAK_API_KEY,
                       'updates'      : write_data})
    
    data = data.encode("utf-8")
    
    # Form the http request using urllib2.
    req = urllib.request.Request(url = REQUEST_URL)
    request_headers = {"User-Agent"    : "mw.doc.bulk-update (Raspberry Pi)",
                       "Content-Type"  : "application/json",
                       "Content-Length": str(len(data))}
    
    # Set http request headers.
    for key, val in request_headers.items():
        req.add_header(key, val)
        
    # Actually make the request to ThingSpeak.
    response = urllib.request.urlopen(req, data=data)
    

if __name__ == "__main__":
    
    # Initialize sensor with external library class.
    sensor = mpu9250()
    
    # Start timing.
    last_update_time = time.time()
    
    # Initialize measurement buffer.
    measurement_buffer = []
    
    # Main loop.
    while True:
        
        # Current accelerometer reading.
        reading = sensor.accel
        
        # Store data to measurement buffer.
        measurement_buffer.append({'field1' : reading[0],
                                   'field2' : reading[1],
                                   'field3' : reading[2],
                                   'delta_t': time.time() - last_update_time})
        
        # Make url request every WAIT_TIME seconds.
        if (time.time() - last_update_time) >= WAIT_TIME:
            
            # Send bulk update, clear measurement buffer, and update timing information.
            bulk_update_channel(measurement_buffer)
            measurement_buffer = []
            last_update_time = time.time()
