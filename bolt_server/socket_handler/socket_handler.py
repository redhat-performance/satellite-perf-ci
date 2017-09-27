'''
File: socket_handler.py
Description: Defines the socket handling interface
Date: 26/09/2017
Author: Saurabh Badhwar <sbadhwar@redhat.com>
'''
from structures import ClientList
import os
import socket
import threading

class SocketHandler(object):
    """Implement the socket handler interface for client handling

    Builds upon the python sockets to implement a multithreaded interface for
    handling the socket connections
    """

    def __init__(self, handler):
        """SocketHandler constructor object

        Initializes the required components for socket handling

        Keyword arguments:
        handler -- The message handler object
        """

        self.client_list = ClientList()
        self.host = os.getenv('BOLT_SERVER_HOST', '127.0.0.1')
        self.port = os.getenv('BOLT_SERVER_PORT', 5200)
        self.queue_size = os.getenv('BOLT_SERVER_CONNECTION_WAIT_QUEUE', 100)
        self.message_handler = handler
        self.listen = True
        self.thread_pool = []
        self.__setup_socket_server()

    def __setup_socket_server(self):
        """Setup the socket server to handle the connection requests."""

        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind((self.host, self.port))
        self.socket.listen(self.queue_size)
        self.__start_listner()

    def __start_listner(self):
        """Start listening for the client connections

        Starts accepting the connections on the port and assigns them to client
        list and moves forward to the next connection.
        """

        while self.listen:
            conn, addr = self.socket.accept()
            handshake = conn.recv(32000)
            topic, hostname = handshake.split(':')
            for t in topic.split(','):
                self.client_list.add_client(t, conn)
                receiver_thread = threading.Thread(target=self.__start_receiver, args=(conn,))
                receiver_thread.daemon = True
                self.thread_pool.append(receiver_thread)
                receiver_thread.start()


    def __start_receiver(self, conn):
        """Start the connection receiver

        Start receiving the messages from the connected clients
        Keyword arguments:
        conn -- The connection object on which to listen
        """

        while self.listen:
            message = conn.recv(32000)
            self.handle(message)

    def handle(self, message):
        """Handle the incoming messages

        Keyword arguments:
        message -- The message to be processed
        """

        print message

    def stop_listening(self):
        """Stop listening on the server so as to prepare for shutdown"""

        self.listen = False
