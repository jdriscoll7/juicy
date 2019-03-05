# Send calls from this number: (251) 290-8658. (+12512908658)
#
# Uses Twilio API.


from twilio.rest import Client
import yaml


class CallSender:
    
    def __init__(self, config_path):
        """
        Performs some basic initialization based on config file.
       
        Note: - Config file will probably have fixed location, and fields inside
                of it will be changed by web interface or phone application.
        """
    
        # Basically sets config file as a dict that is part of the object.
        with open(config_path + "notification_settings.yml", 'r') as config_file:
            self.settings = yaml.load(config_file)
            
        # Setup Twilio client based on API keys in config file.
        self.client = Client(self.settings['api_keys']['account_sid'], 
                             self.settings['api_keys']['auth_token'])

    def send_calls(self):
        """
        Sends calls based on settings in configuration file.
        """
        
        # Extract voice message url to use.
        #voice_message_url = ("https://raw.githubusercontent.com/jwd0023/juicy/master/juicy/alarm/call_messages/" +
        #                     self.settings['call_settings']['call_message'])
        
        # Form message - needs to be integrated with directory structure to have multiple messages.
        # This is just for testing, I guess :(
        message = "No sir Marco Zuninga, that is incorrect."
        voice_message_url = "https://twimlets.com/message?" + urlencode({'Message': message})
        
        # Send call to each recipient listed in configuration file.
        for recipient in (self.settings['call_settings']['recipients']):
            self.client.calls.create(url=voice_message_url,
                                     to=recipient,
                                     from_="+12512908658")
