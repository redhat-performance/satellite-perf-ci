'''
File: logger.py
Description: Log management engine
Date: 28/09/2017
Author: Saurabh Badhwar <sbadhwar@redhat.com>
'''
from structures import LogMessage
import os

class Logger(object):
    """Start the logger"""

    def __init__(self):
        """Initialize the Logger"""

        self.log_messages = []
        self.message_count = 0
        self.write_messages = os.getenv('BOLT_LOG_MESSAGES', 0)
        self.log_file = os.getenv('BOLT_LOG_FILE', '')
        self.message_severity = os.getenv('BOLT_LOG_LEVEL', 2)

    def new_message(self, message, code, location):
        """Log a new message

        Keyword arguments:
        message -- The message to be logged
        code -- The code associated with the message
        location -- The location of the file where the message originated
        """

        log_message = LogMessage(message, code, location)
        self.log_message.append(log_message)

    def flush(self):
        """Flush the recorded messages to the disk

        Returns: Bool
        """

        if self.__write_message():
            self.log_message = []
            return True
        return False


    def __write_message(self):
        """Writes the message to the disk

        Returns: Bool
        """

        if self.log_file == '':
            return False
        try:
            with open(self.log_file, 'a+') as log_file:
                for messages in self.log_message:
                    log_file.write(message.get_message())
        except Exception:
            return False

        return True
