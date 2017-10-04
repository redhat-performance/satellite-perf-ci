'''
File: structures.py
Description: Structures defining the plugin loading
Date: 03/10/2017
Author: Saurabh Badhwar <sbadhwar@redhat.com>
'''

class Plugin(object):
    """Load and define a new plugin"""

    def __init__(self, name, location, structure, main_class):
        """Initialize the plugin data

        Keyword arguments:
        name -- The name of the plugin
        location -- The location from where the plugin has been loaded
        structure -- The message structure that the plugin uses
        main_class -- The main class belonging to the plugin
        """

        self.plugin_name = name
        self.plugin_location = location
        self.plugin_structure = structure
        self.executor = main_class

    def get_message_struct(self):
        """Get the message structure

        Returns:
            Mixed
        """

        return self.plugin_structure

    def get_executor(self):
        """Get the plugin executor object

        Returns:
            Object
        """

        return self.executor
