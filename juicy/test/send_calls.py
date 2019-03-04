from juicy.alarm.call_sender import CallSender


if __name__ == "__main__":
    
    # Path to configuration file - if no user input, then it is in cwd.
    config_directory = input("Enter notification_settings.yaml directory. If it is in cwd, just press <enter>.")
    
    # Parse based on rules in last comment.
    if len(config_directory) == 0:
        config_directory = "./"
    
    # Create CallSender object.
    test_caller = CallSender(config_directory)
    
    # Just send a single call for now.
    test_caller.send_calls()
    
