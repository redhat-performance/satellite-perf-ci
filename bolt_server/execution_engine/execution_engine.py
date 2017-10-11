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
    """

    def __init__(self, message_dispatcher, execution_threads=3):
        """Initialize the execution engine

        Keyword arguments:
        message_dispatcher -- The message dispatcher object
        execution_threads -- The number of execution threads to run concurrently
                             for the task execution (Default: 3)
        """

        self.message_dispatcher = message_dispatcher
        self.execution_threads = execution_threads
        self.task_queue = TaskQueue()

    def new_task(self, task_name, task_struct, task_params, task_topics, task_dependency=None):
        """Create a new task and queue it inside the task queue

        Keyword arguments:
        task_name -- The name of the task to be created
        task_struct -- The structure associated with the task
        task_params -- The parameters associated with the task
        task_topics -- The topics to which the task should be broadcasted
        task_dependency -- The dependency tree for the task (Default: None)

        Returns:
            task_id The task id of the current task
        """

        task_id = self.task_queue.queue_task(task_name, task_struct, task_params, task_topics, task_dependency)
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
