'''
File: structures.py
Description: Defines the structures used by socket handler
Date: 26/09/2017
Author: Saurabh Badhwar <sbadhwar@redhat.com>
'''

class ClientList(object):
    """ClientList structure. Used for holding the connected clients list

    The general structure looks like:
    client_list: {'topic': [clients]}
    """

    client_list = {}    #Initialize the client list

    def __init__(self):
        """ClientList constructor

        Initializes the ClientList for use in the socket handler
        """

        self.topic_count = 0
        self.error_count = 0

    def add_topic(self, topic):
        """Add a new topic to the client list

        Keyword arguments:
        topic -- the topic to be added to the client list

        Returns:
            count The number of keys in list
        """

        if topic in self.client_list.keys():
            return self.topic_count

        self.client_list[topic] = []
        self.topic_count = len(self.client_list)

        return self.topic_count

    def add_client(self, topic, client):
        """Add a new client to the client list

        Keyword arguments:
        topic -- The topic to which the client should be added
        client -- The callable socket object for the client

        Returns:
            True on success
            False on Failure
        """

        if topic not in self.client_list.keys():
            self.add_topic(topic)
        if client in self.client_list[topic]:
            return False

        self.client_list[topic].append(client)
        return True

    def get_topics(self):
        """Get the list of topics

        Returns: List of topics
        """

        return self.client_list.keys()

    def get_clients(self, topic):
        """Return the list of clients associated with the provided topic

        Keyword arguments:
        topic -- The topic for which to return the client list

        Returns:
            list on Success
            False on Failure
        """

        if topic not in self.client_list.keys():
            return False

        return self.client_list[topic]

    def remove_client(self, client, topic=''):
        """Remove the provided client from the client list

        If the topic is not provided, client will be removed from all the topics
        it is present in.

        Keyword arguments:
        topic -- The topic to be searched for the client (Default: '')
        client -- The client to be removed

        Return: True
        """

        if topic == '':
            for t in self.client_list:
                if client in self.client_list[t]:
                    self.client_list[t].remove(client)
        else:
            self.client_list[topic].remove(client)

        return True

    def remove_topic(self, topic, force=False):
        """Removes the mentioned topics from the client list

        Removes the topics from the client list if the client list for that
        topic is empty.
        The optional force parameter if set to true will cause the topic to be
        removed even if the client list contains clients subscribed to that
        topic.

        Keyword arguments:
        topic -- The topic to be removed
        force -- Force the removal of the topic (Default: False)

        Raises:
            RuntimeError if the user tries to remove a topic which has active
            clients

        Returns: True
        """

        if topic in self.client_list.keys():
            if len(self.client_list[topic]) != 0 and force==False:
                raise RuntimeError("Can't remove a topic with active clients")
            else:
                del self.client_list[topic]

        return True
