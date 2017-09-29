'''
File: structures.py
Description: Logging information structures
Date: 28/09/2017
Author: Saurabh Badhwar <sbadhwar@redhat.com>
'''
import datetime
import json

class LogMessage(object):
    """Handle the log messages"""

    LEVEL_DEBUG = 1
    LEVEL_INFO = 2
    LEVEL_WARN = 3
    LEVEL_ERROR = 4
    LEVEL_FATAL = 5

    def __init__(self, message, code, location, severity):
        """Initialize the LogMessage

        Keyword arguments:
        message -- The message to be logged
        code -- The code associated with the log message
        location -- Location of the file where the log message originates
        severity -- The severity of the message
        """

        self.message = message
        self.message_code = str(code)
        self.message_location = location
        self.message_severity = severity
        self.message_time = str(datetime.datetime.now())

    def get_message(self):
        """Return the fully formatted message for use

        Returns: String
        """

        message = "[{}]({}):{}:{}"
        message = message.format(self.message_time, self.message_location, self.message_code, self.message)

        return message

    def get_json(self):
        """Return the json formatted Log message

        Returns: JSON
        """

        message = {
            'message': self.message,
            'severity': self.message_severity,
            'code': self.message_code,
            'location': self.message_location,
            'time': self.message_time
        }

        return json.dumps(message)

    
