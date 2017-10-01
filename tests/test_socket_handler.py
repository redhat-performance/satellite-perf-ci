'''
File: test_socket_handler.py
Description: Test the execution of socket handler
Date: 01/10/2017
Author: Saurabh Badhwar <sbadhwar@redhat.com>
'''
from bolt_server.socket_handler import SocketHandler
import os
import pytest
import socket

class TestSocketHandler(object):
    """Test the execution of Socket Handler"""

    def test_default_socket(self):
        """Test the default opening of the SocketHandler"""

        socket_handler = SocketHandler('print')
        test_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        ret_code = test_socket.connect_ex(('127.0.0.1', 5200))
        test_socket.sendall('Test: Pytest')
        socket_handler.stop_listening()
        assert ret_code == 0

    def test_custom_socket(self):
        """Test SocketHandler for custom port"""

        os.environ['BOLT_SERVER_PORT'] = "5000"
        socket_handler = SocketHandler('print')
        test_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        ret_code = test_socket.connect_ex(('127.0.0.1', 5000))
        test_socket.sendall('Test: Pytest')
        socket_handler.stop_listening()
        assert ret_code == 0
