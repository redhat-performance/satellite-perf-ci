'''
File: thread_pool.py
Description: Thread pool management resources
Date: 28/09/2017
Author: Saurabh Badhwar <sbadhwar@redhat.com>
'''
from structures import ThreadPool
import threading

class ThreadPoolManager(object):
    """Lays out the interface for management of thread pool"""

    def __init__(self):
        """Initialize the thread pool manager"""

        self.thread_pool = ThreadPool()

    def start_thread(self, application_name, target, params=None):
        """Start a new thread and adds it to thread pool

        Keyword arguments:
        application_name -- The name of the application whose thread is being
                            started
        target -- The target method to be executed in thread
        params -- The optional params that needs to be passed to the thread (Default: None)
        """

        th = self.__start_thread(target, params)
        self.thread_pool.add_thread(application_name, th)

    def close_application(self, application_name):
        """Stop the application running in thread pool

        Keyword arguments:
        application_name -- The name the application to stop

        Returns: Bool
        """

        if self.thread_pool.is_application(application_name):
            for thread in self.thread_pool.get_threads(application_name):
                thread.join()

        try:
            self.thread_pool.remove_application(application_name)
        except RuntimeError:
            return False

        return True

    def __start_thread(self, target, params=None):
        """Start a new thread for the provided target

        Keyword arguments:
        target -- The target method to run as thread
        params -- Parameters to be passed to target function

        Returns:
            threading.Thread
        """

        if params == None:
            app_thread = threading.Thread(target=target)
        else:
            app_thread = threading.Thread(target=target, params=params)

        app_thread.daemon = True
        app_thread.start()

        return app_thread
