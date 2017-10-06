'''
File: execution_engine.py
Description: An out of order execution engine for Bolt
Date: 06/10/2017
Author: Saurabh Badhwar <sbadhwar@redhat.com>
'''
from structures import RequestQueue

class ExecutionEngine(object):
    """Provides an out of order execution engine for the tasks that are being
    enqueued by the Bolt server.
    """

    def __init__(self, message_dispatcher, num_workers=3):
        """Initialize the Execution Engine and prepare it for task execution

        Keyword arguments:
        message_dispatcher -- The Message Dispatcher to use
        num_workers -- The number of task execution workers that should run (Default: 3)
        """

        self.message_dispatcher = message_dispatcher
        self.request_queue = RequestQueue()

    def execute_task(self, name, message_struct, params, topics, dependency=None):
        """Execute a new task

        The method queues the incoming task in the request queue for execution
        when one of the execution worker is free and the task has all its
        dependencies satisfied.

        Keyword arguments:
        name -- The name of the message
        message_struct -- The message structure that needs to be communicated
        params -- The parameters to be passed to the message structure
        topics -- The list of topics to which the message should be broadcasted
        dependency -- The list of dependent messages the current message depends on

        Raises:
            RuntimeError for execution errors

        Returns:
            Integer The message id of the current message
        """

        self.__enqueue_task(name, message_struct, params, topics, dependency)

    def __request_worker(self, request):
        """Request execution worker

        The request execution worker takes up a request and runs it in a thread
        where the request is actually executed. The execution thread is
        responsible for keeping a state check in place on the request and hence
        periodically updates the request status by polling for the changes in
        request.

        Keyword arguments:
        request -- The request object to be executed by the worker thread

        Raises:
            RuntimeError if some error occurs during the execution of the request

        Return:
            Bool
        """

        raise NotImplementedError("The method needs to be implemented")

    def __worker_launcher(self):
        """Launch the requested number of request workers."""

        raise NotImplementedError("The method needs to be implemented")

    def __enqueue_task(self, name, message_struct, params, topics, dependency=None):
        """Internal function for queuing the task

        Keyword arguments:
        name -- The name of the message provider
        message_struct -- The message structure that needs to be communicated
        params -- The parameters to be passed to the message structure
        topics -- The list of topics to which the message should be broadcasted
        dependency -- The list of dependent messages the current message depends on
        """

        request = Request(name, message_struct, params, topics)
        self.request_queue.queue(request, dependency_list=dependency)
