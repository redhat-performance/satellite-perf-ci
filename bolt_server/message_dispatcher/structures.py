'''
File: structures.py
Description: Message dispatcher related structures
Date: 29/09/2017
Author: Saurabh Badhwar <sbadhwar@redhat.com>
'''
import hashlib
import json

class Message(object):
    """Structure for handling new message types.

    Provides general functionality for all the messages to go through
    and pass there structural representation for validation.

    The message structure looks like:
    message = {
        message_name: [message_strcuture]
    }
    """

    def __init__(self):
        """Initialize the Message Structure"""

        self.messages = {}
        self.message_count = 0
        self.error_count = 0

    def add_message(self, message_name, message_structure):
        """Add a new message to the message structure

        Keyword arguments:
        message_name -- The name of the message
        message_strcuture -- The strcuture the message follows

        Raises:
            RuntimeError if message_name already exists
        """

        if message_name in self.messages.keys():
            raise RuntimeError("The specified message already exists")

        self.messages[message_name] = message_structure

    def add_value(self, message_name, key, value):
        """Add a new value to the message key

        Keyword arguments:
        message_name -- The name of the message
        key -- The key to be updated in the message structure
        value -- The value to be allocated to the key

        Raises:
            KeyError when the message name is not present
        """

        if message_name not in self.messages.keys():
            raise KeyError("The message type to update is not registered")

        self.messages[message_name][key] = value

    def reset_value(self, message_name, key):
        """Reset the value for the provided key in the message_name

        Keyword arguments:
        message_name -- The name of the message to to be updated
        key -- The key whose value should be reset

        Raises:
            KeyError if the message to be updated is not registered
        """

        if message_name not in self.messages.keys():
            raise KeyError("The key to be updated was not found")

        self.messages[message_name][key] = ''

    def get_message(self, message_name):
        """Get the message structure associated with the name

        Keyword arguments:
        message_name -- The name of the message whose structure is requested

        Raises:
            KeyError when the message is not found

        Returns:
            Mixed The message structure
        """

        if message_name not in self.messages.keys():
            raise KeyError("The requested message structure was not found")

        return self.messages[message_name]

    def get_message_list(self):
        """Get all the registered messages

        Return:
            List of registered messages
        """

        return self.messages.keys()

    def remove_message(self, message_name):
        """Remove the message from the registered list

        Keyword arguments:
        message_name -- The name of the message to be removed
        """

        del self.messages[message_name]

class MessagePacket(object):
    """The message pakcet Structure for the Bolt Server

    Encapsulates the message along with a unique recognizable id so as to manage
    the message lifecycle

    Message Packet: {
        identifier: <unique_identifier>,
        message: Message
    }
    """

    def __init__(self, message):
        """Initialize the Message Packet"""

        self.message_packet = {}
        self.message_digest = hashlib.sha256(message)
        self.message_packet['id'] = self.message_digest
        self.message_packet['payload'] = message

    def get_packet(self):
        """Get the JSON formatted packet which can be transmitted

        Returns: JSON
        """

        return (self.message_digest, json.dumps(self.message_packet))

class MessageQueue(self):
    """We use a message queue to track the responses received for the message

    Message Queue keeps a track of unique message identifiers along with the
    response they they generate so as to decide what to do next
    """

    def __init__(self):
        """Initialize the message queue"""

        self.message_queue = {}

    def queue(self, message_identifier):
        """Queue a newly sent message

        Keyword arguments:
        message_identifier -- The unique identifier pertaining to message
        """

        self.message_queue[message_identifier] = 'Awaited'

    def update_status(self, message_identifier, status):
        """Update the status of a sent message

        Keyword arguments:
        message_identifier -- The identifier to update
        status -- The new status of the message

        Raises:
            KeyError if the message is not present in the queue
        """

        if message_identifier not in self.message_queue.keys():
            raise KeyError("Cannot update status for an inexistant message")

        self.message_queue[message_identifier] = status
