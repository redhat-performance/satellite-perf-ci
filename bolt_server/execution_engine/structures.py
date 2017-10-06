'''
File: structures.py
Description: Structures being used by the execution engine
Date: 06/10/2017
Author: Saurabh Badhwar <sbadhwar@redhat.com>
'''

class RequestQueue(object):
    """Request Queue structure for the execution engine

    The Request Queue serves the purpose of holding and queueing the Message
    requests as they arrive. The execution engine is then responsible to manage
    the lifetime of the request and the out of order execution of the requests
    by checking their dependencies.
    """

    #Request States
    REQ_QUEUED = 0
    REQ_PROCESSED = 1
    REQ_COMPLETED = 2
    REQ_FAILED = 3

    def __init__(self):
        """Initialize the Request Queue for Execution Engine"""

        self.request_queue = {}
        self.dependency_list = {}
        self.requests = 0

    def queue(self, request, dependency_list=None):
        """Queue a new request for execution

        Keyword arguments:
        request -- The request to be queued
        dependency_list -- The dependencies that must be fulfilled before the
                           current request is executed

        Returns:
            Bool
        """

        if request in self.request_queue.keys():
            return False

        self.request_queue[request] = self.REQ_QUEUED
        if dependency_list != None:
            self.dependency_list[request] = dependency_list
        return True

    def check_ready(self, request):
        """Get the status of the request if it is ready to be executed or not

        Keyword arguments:
        request -- The request whose status needs to be checked

        Returns:
            Bool
        """

        if request not in self.request_queue.keys():
            return False

        if request in self.dependency_list.keys():
            if self.dependency_list[request] != None or self.dependency_list[request] != []:
                return False

        return True

    def update_status(self, request, status):
        """Update the status of the request

        Keyword arguments:
        request -- The request whose status should be updated
        status -- The new status value

        Raises:
            KeyError if the request is not present in the queue
        """

        if request not in self.request_queue.keys():
            raise KeyError("No such request in queue")

        self.request_queue[request] = status
