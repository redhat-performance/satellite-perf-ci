'''
File: execution_engine.py
Description: An out of order execution engine for Bolt
Date: 06/10/2017
Author: Saurabh Badhwar <sbadhwar@redhat.com>
'''
from structures import TaskQueue

class ExecutionEngine(object):
    """Execution engine for task execution

    Queues and plans the execution of the tasks based on dependency resolution
    for the new tasks. The execution engine manages the order in which the tasks
    will be executed and is also responsible for updating their state in the
    task queue.

    TODO: Add a multithreaded execution mechanism
    """

    def __init__(self, message_dispatcher, plugin_loader, execution_threads=3):
        """Initialize the execution engine

        Keyword arguments:
        message_dispatcher -- The message dispatcher object
        plugin_loader -- The plugin loader object to access the loaded plugins
        execution_threads -- The number of execution threads to run concurrently
                             for the task execution (Default: 3)
        """

        self.message_dispatcher = message_dispatcher
        self.plugin_loader = plugin_loader
        self.execution_threads = execution_threads
        self.task_queue = TaskQueue()
        #Provide a strcuture to map the message id to task id
        self.message_map = {}

        #Register the execution engine message handler to message dispatcher
        self.message_dispatcher.register_handler(self.__handle_incoming_message)

    def new_task(self, task_name, plugin_name, task_params, task_topics, task_dependency=None):
        """Create a new task and queue it inside the task queue

        Keyword arguments:
        task_name -- The name of the task to be created
        plugin_name -- The name of the plugin to be used for execution
        task_params -- The parameters associated with the task
        task_topics -- The topics to which the task should be broadcasted
        task_dependency -- The dependency tree for the task (Default: None)

        Returns:
            task_id The task id of the current task
        """

        task_id = self.task_queue.queue_task(task_name, plugin_name, task_params, task_topics, task_dependency)
        return task_id

    def update_task(self, task_id, status):
        """Update the status of the task

        Keyword arguments:
        task_id -- The id of the task
        status -- The new status for the task

        Returns:
            Bool
        """

        try:
            self.task_queue.change_task_status(task_id, status)
        except KeyError:
            return False
        return True

    def execute_task(self, task_id):
        """Execute the task on the provided topics

        Keyword arguments:
        task_id -- The id of the task to be executed

        Returns:
            Bool
        """

        task = self.__resolve_task(task_id)

        if task == False:
            return

        task_id = task[0]
        task_name = task[1]
        task_plugin = task[2]
        task_params = task[3]
        task_topics = task[4]

        try:
            plugin_structure = self.plugin_loader.get_plugin_structure(task_plugin)
        except KeyError:
            return False

        if not self.message_dispatcher.message_exists(task_plugin):
            self.message_dispatcher.register_message(task_plugin, plugin_structure, task_topics)

        try:
            message_id = self.message_dispatcher.send_message(task_plugin, task_params)
            self.task_queue.change_task_status(task_id, self.task_queue.TASK_RUNNING)
            self.message_map[message_id] = task_id

        except (KeyError, RuntimeError):
            return False

        self.message_dispatcher.unregister_message(task_plugin)
        return True

    def cycle_tasks(self):
        """Cycle through the tasks and determine which tasks to execute

        The mechanism allows for cycling through the task queue to determine
        if the task is ready to execute or not. If the task is ready to execute
        the execution method is called with the task_id to get the task to
        execution state.
        """

        for task in self.task_queue.get_task_list():
            if self.__check_ready_to_execute(task):
                self.execute_task(task)

    def __check_ready_to_execute(self, task_id):
        """Check if the task is ready to execute or not

        Before we execute a task, we try to ensure that all the dependencies the
        task has have been executed and completed successfully. When this is the
        case then only we execute the task.

        Keyword arguments:
        task_id -- The id of the task to be checked for execution status

        Returns:
            Bool
        """

        try:
            dependency_list = self.task_queue.get_task_dependency(task_id)
        except KeyError:
            return False

        for dependency in dependency_list:
            dependency_status = self.task_queue.get_task_status(dependency)
            if dependency_status != self.task_queue.TASK_COMPLETE:
                return False

        return True

    def __resolve_task(self, task_id):
        """Retrieve the task information provided the task id

        Keyword arguments:
        task_id -- The task id whose task needs to be resolved
        """

        try:
            task = self.task_queue.get_task(task_id)
        except KeyError:
            return False

        return task

    def __handle_incoming_message(self, message):
        """Handle the incoming message responses

        Once the message has been sent, the clients can send status updates to
        the bolt server through the message sending mechanism. This method
        is responsible for handling the actions that needs to be taken once the
        status update is received by the Execution Engine.

        Keyword arguments:
        message -- The incoming message dict
        """

        message_id = message['id']
        message_payload = message['result']

        #Resolve the task id from the incoming message
        task_id = self.message_map[message_id]

        #Resolve the task from task id
        task = self.__resolve_task(task_id)

        if task != False:
            task_plugin = task[2]

        #Resolve the plugin executor
        plugin_executor = self.plugin_loader.get_plugin_executor(task_plugin)
        plugin_executor_instance = plugin_executor()

        #Forward the message to plugin executor along with the callback object
        plugin_executor_instance.handle(message_payload, self)
