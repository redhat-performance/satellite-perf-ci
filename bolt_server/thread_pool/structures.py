'''
File: strcutures.py
Description: Thread pool manager resources
Author: Saurabh Badhwar <sbadhwar@redhat.com>
Date: 27/09/2017
'''

class ThreadPool(object):
    """Storage structure for Threads

    We run a number of different components as threads. ThreadPool provides a
    structure for storing the different kind of threads that are present in the
    application runtime.

    The structure is a general python dictionary in the format:
    thread_pool = {application_name: [Threads]}
    """

    thread_pool = {}

    def __init__(self):
        """Initialize the thread pool store"""

        self.thread_count = 0
        self.error_count = 0

    def add_application(self, application_name):
        """Add a new application name to the thread pool

        Keyword arguments:
        application_name -- The name of the application to be added to the
                            thread pool

        Returns: True
        """

        if application_name not in self.thread_pool.keys():
            self.thread_pool[application_name] = []

        return True

    def add_thread(self, application_name, thread):
        """Add a new thread to the thread pool of the application

        Keyword arguments:
        application_name -- The name of the application to which the thread
                            should be appended
        thread -- The thread object which should be appended

        Returns: True
        """

        if application_name not in self.thread_pool.keys():
            self.add_application(application_name)

        self.thread_pool[application_name].append(thread)

        return True

    def get_applications(self):
        """Get the list of applications that are present in the thread pool

        Returns:
            List of applications
        """

        return self.thread_pool.keys()

    def get_threads(self, application_name):
        """Get the list of threads pertaining to the provided application name

        Keyword arguments:
        application_name -- The name of the application whose threads are required

        Raises:
            RuntimeError if the application name doesn't exists

        Returns:
            List of threads
        """

        if application_name not in self.thread_pool.keys():
            raise RuntimeError("The mentioned application is not running any threads")

        return self.thread_pool[application_name]
