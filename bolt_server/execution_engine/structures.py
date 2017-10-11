'''
File: structures.py
Description: Structures being used by the execution engine
Date: 06/10/2017
Author: Saurabh Badhwar <sbadhwar@redhat.com>
'''
import hashlib
import random

class Task(object):
    """Create a new task which can encapsulate all the data objects"""

    def __init__(self, task_name, task_struct, task_params, task_topics):
        """Initialize the Task object

        Keyword arguments:
        task_name -- The name of the task to be executed
        task_struct -- The structure of the task to be executed
        task_params -- The parameters to be passed to the task
        task_topics -- The topics to which the task should be executed on
        """

        self.task_name = task_name
        self.task_id = hashlib.md5(self.task_name + str(random.randint(1,25000))).hexdigest()
        self.task_structure = task_struct
        self.task_params = task_params
        self.task_topics = task_topics

    def get_task_id(self):
        """Get the task id

        Returns:
            task_id A unique identifier for the task
        """

        return self.task_id

    def get_task(self):
        """Get the task data

        Returns:
            List
        """

        return [self.task_id, self.task_name, self.task_structure, self.task_params, self.task_topics]

class TaskQueue(object):
    """Create and queue a new task for execution"""

    #Task lifecycle status
    TASK_QUEUED = 0
    TASK_PENDING = 1
    TASK_RUNNING = 2
    TASK_HALTED = 3
    TASK_COMPLETE = 4

    def __init__(self):
        """Initialize the task queue structure."""

        self.task_queue = {}

    def queue_task(self, task_name, task_struct, task_params, task_topics, task_dependency=None):
        """Queue a new task

        Keyword arguments:
        task_name -- The name of the task
        task_struct -- The task structure
        task_params -- The parameters to be passed to the task structure
        task_topic -- The topics the task should be broadcasted to
        task_dependency -- The tasks on which the current task depends

        Returns:
            task_id The id of the task
        """

        task = Task(task_name, task_struct, task_params, task_topics)
        task_id = task.get_task_id()
        self.task_queue[task_id] = [task, self.TASK_QUEUED, task_dependency]
        return task_id

    def get_task(self, task_id):
        """Return the task based on its task id

        Keyword arguments:
        task_id -- The id of the task

        Raises:
            KeyError if the task is not present

        Returns:
            List
        """

        if task_id not in self.task_queue.keys():
            raise KeyError("The mentioned task has not been queued")

        return self.task_queue[task_id][0].get_task()

    def get_task_status(self, task_id):
        """Get the status of the current task

        Keyword arguments:
        task_id -- The id of the task to be queried for the status

        Raises:
            KeyError if the task id is not present

        Returns:
            Integer The status of the task
        """

        if task_id not in self.task_queue.keys():
            raise KeyError("The provided task is not queued")

        return self.task_queue[task_id][1]

    def get_task_dependency(self, task_id):
        """Get the dependency list of the task

        Keyword arguments:
        task_id -- The id of the task to retrieve the dependency list for

        Raises:
            KeyError if the task_id is not queued
        Returns:
            List The dependencies for the given task
        """

        if task_id not in self.task_queue.keys():
            raise KeyError("Task is not queued")

        return self.task_queue[task_id][2]

    def change_task_status(self, task_id, task_status):
        """Change the status of the task

        Keyword arguments:
        task_id -- The task id of the task to update the status of
        task_status -- The new status value to be set for the task

        Raises:
            KeyError if the task is not queued
        """

        if task_id not in self.task_queue.keys():
            raise KeyError("The provided task is not present")

        self.task_queue[task_id][1] = task_status
