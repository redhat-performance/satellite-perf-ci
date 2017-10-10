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
