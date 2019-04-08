import os
import time
import json
import urllib2
from mpu9250.mpu9250 import mpu9250


# Some constants used in main loop.
THINGSPEAK_API_KEY = '797UKWN6FJXVHF6O' # API write key for ThingSpeak.
WAIT_TIME          = 20                 # Update time in seconds for ThingSpeak (15s minimum)


def bulk_update_channel(write_data):
    
    # Format the input data into JSON format.
    data = json.dumps({'write_api_key': THINGSPEAK_API_KEY,
                       'updates':       write_data})
    
    # Form the http request using urllib2.
	req = urllib2.Request(url = url)
	request_headers = {"User-Agent":    "mw.doc.bulk-update (Raspberry Pi)",
                      "Content-Type":   "application/json",
                      "Content-Length": str(len(data))}
    
    # Set http request headers.
	for key,val in request_headers:
		req.add_header(key, val)
        
    # Add the formed JSON data to the http request.
	req.add_data(data)
    
    # Actually make the request to ThingSpeak.
	response = ul.urlopen(req)
    


if __name__ == "__main__":
    
    # Initialize sensor with external library class.
    sensor = mpu9250()
    
    # Start timing.
    last_update_time = time.time()
    
    # Main loop.
    while True:
        
        # If we have waited WAIT_TIME, then bulk update the ThingSpeak channel.
        if (time.time() - last_update_time) >= WAIT_TIME:
            
            
            last_update_time = time.time()
            
