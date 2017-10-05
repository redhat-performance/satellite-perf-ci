'''
File: plugin_loader.py
Description: Plugin loader for Bolt
Date: 03/10/2017
Author: Saurabh Badhwar <sbadhwar@redhat.com>
'''
from structures import Plugin
import os
import sys

class PluginLoader(object):
    """Load the plugins from the pre-defined load path
    """

    def __init__(self):
        """Initialize the plugin loader
        """

        #Initialize the loaded plugins recorder
        self.plugins = {}

        #We need to know from where to include our bolt plugins
        self.__determine_include_path()

    def load_plugins(self):
        """Walk through the python path and load the plugins

        Returns:
            List of the loaded plugins
        """

        module_list = []
        error_list = []
        for path in self.include_path:
            mods = self.__get_modules(path)
            module_list = module_list + mods

        iter_list = module_list[:]
        for module in iter_list:
            if not self.__validate_module(module):
                module_list.remove(module)

        self.__load_plugins(module_list)

    def __determine_include_path(self):
        """Determine the include path from where we can include our plugins"""

        self.include_path = []
        for path in sys.path:
            test_path = os.path.join(path, 'bolt_modules')
            if os.path.isdir(test_path):
                self.include_path.append(test_path)

    def __get_modules(self, path):
        """Get the list of modules present in the provided include path

        Keyword arguments:
        path -- The path under which the search should be performed

        Returns:
            List of modules along with path
        """

        subfolders = os.listdir(path)
        modules = []
        for folder in subfolders:
            tmp_path = os.path.join(path, folder)
            init_path = os.path.join(tmp_path, '__init__.py')
            if os.path.isdir(tmp_path) and os.path.exists(init_path):
                modules.append(tmp_path.split(os.path.sep)[-1])

        return modules

    def __load_plugins(self, modules):
        """Load the modules as plugins

        Keyword arguments:
        modules -- The list of modules to be loaded as plugins

        Raises:
            RuntimeError if some error occurs during module load
        """

        for module in modules:
            import_name = 'bolt_modules.' + module
            load_data = __import__(import_name, fromlist=['*'])
            name = module
            location = load_data.__file__
            structure = getattr(load_data, 'Message')
            main_class = getattr(load_data, module)
            plugin = Plugin(name, location, structure, main_class)
            self.plugins[name] = plugin

    def get_plugin(self, name):
        """Get the plugin provided its name

        Keyword arguments:
        name -- The name of the plugin to be retrieved

        Raises:
            KeyError if the plugin is not loaded

        Returns:
            Plugin
        """

        if name not in self.plugins.keys():
            raise KeyError("The plugin is not installed/loaded")

        return self.plugins[name]

    def get_plugin_executor(self, name):
        """Get the main executor for the plugin provided the name of the plugin

        Keyword arguments:
        name -- The name of the plugin to retrieve the executor for

        Raises:
            KeyError if the plugin is not loaded/installed

        Returns:
            Object
        """

        if name not in self.plugins.keys():
            raise KeyError("The plugin is not loaded")

        return self.plugins[name].get_executor()

    def get_plugin_structure(self, name):
        """Get the structure of the plugin provided the name

        Keyword arguments:
        name -- The name of the plugin to load the message of

        Raises:
            KeyError if the plugin is not loaded/installed

        Returns:
            Object
        """

        if name not in self.plugins.keys():
            raise KeyError("Plugin is not loaded/installed")

        return self.plugins[name].get_message_struct()

    def __validate_module(self, mod_name):
        """Validate if the provided plugin adheres to the specification or not

        Our plugins follow a specific set of guidelines that needs to be
        followed so as to enable an interoperable set of features between the
        server and the client.
        This allows us to keep the codebase to minimal while running the same
        plugin on the server/client.

        The general plugin structure looks like
        /plugin
        - __init__.py (Exports the message and executor structure)
        - structures.py (Containes the communication message structure)
        - plugin.py (Contains the main executor class of the plugin)

        Keyword arguments:
        mod_name -- The name of the module

        Returns: Bool
        """

        import_name = 'bolt_modules.' + mod_name
        module = __import__(import_name, fromlist=['*'])
        includes = dir(module)
        if 'Message' in includes and mod_name in includes:
            return True
        return False
