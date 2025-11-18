"""
KVStore Client - Python client for the C++ key-value store server

This module provides a simple interface to interact with the
key-value store server over TCP.
"""

import socket
import logging

# Set up module logger
logger = logging.getLogger(__name__)


class KVStoreClient:
    """Client for connecting to and communicating with the KVStore server"""
    
    def __init__(self, host='localhost', port=8080):
        """
        Initialize the client
        
        Args:
            host (str): Server hostname or IP address
            port (int): Server port number
        """
        self.host = host
        self.port = port
        self.socket = None
    
    def connect(self):
        """
        Connect to the server
        
        Raises:
            ConnectionError: If unable to connect to the server
        """
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.connect((self.host, self.port))
            logger.info(f"Connected to {self.host}:{self.port}")
        except socket.error as e:
            raise ConnectionError(f"Failed to connect to server: {e}")
    
    def close(self):
        """Close the connection to the server"""
        if self.socket:
            self.socket.close()
            self.socket = None
            logger.info("Connection closed")
    
    def _send_command(self, command):
        """
        Send a command to the server and receive the response
        
        Args:
            command (str): The command to send (without trailing newline)
            
        Returns:
            str: The server's response (without trailing newline)
            
        Raises:
            ConnectionError: If not connected or connection fails
        """
        if not self.socket:
            raise ConnectionError("Not connected to server. Call connect() first.")
        
        try:
            # Send command with newline
            message = command + '\n'
            self.socket.sendall(message.encode('utf-8'))
            
            # Receive response
            response = self.socket.recv(4096).decode('utf-8').strip()
            return response
            
        except socket.error as e:
            raise ConnectionError(f"Communication error: {e}")
    
    def set(self, key, value):
        """
        Store a key-value pair
        
        Args:
            key (str): The key to store
            value (str): The value to store
            
        Returns:
            bool: True if successful
            
        Raises:
            ValueError: If key or value is invalid
            ConnectionError: If communication fails
        """
        if not key or not value:
            raise ValueError("Key and value must not be empty")
        
        if ' ' in key:
            raise ValueError("Key cannot contain spaces")
        
        command = f"SET {key} {value}"
        response = self._send_command(command)
        
        if response == "OK":
            return True
        else:
            raise RuntimeError(f"Unexpected server response: {response}")
    
    def get(self, key):
        """
        Retrieve a value by key
        
        Args:
            key (str): The key to retrieve
            
        Returns:
            str: The value if found, None if not found
            
        Raises:
            ValueError: If key is invalid
            ConnectionError: If communication fails
        """
        if not key:
            raise ValueError("Key must not be empty")
        
        command = f"GET {key}"
        response = self._send_command(command)
        
        if response.startswith("OK "):
            # Extract value (everything after "OK ")
            return response[3:]
        elif response == "ERROR KEY_NOT_FOUND":
            return None
        else:
            raise RuntimeError(f"Unexpected server response: {response}")
    
    def delete(self, key):
        """
        Delete a key-value pair
        
        Args:
            key (str): The key to delete
            
        Returns:
            bool: True if key existed and was deleted, False if key didn't exist
            
        Raises:
            ValueError: If key is invalid
            ConnectionError: If communication fails
        """
        if not key:
            raise ValueError("Key must not be empty")
        
        command = f"DELETE {key}"
        response = self._send_command(command)
        
        if response == "OK":
            return True
        elif response == "ERROR KEY_NOT_FOUND":
            return False
        else:
            raise RuntimeError(f"Unexpected server response: {response}")
    
    def exists(self, key):
        """
        Check if a key exists
        
        Args:
            key (str): The key to check
            
        Returns:
            bool: True if key exists, False otherwise
            
        Raises:
            ValueError: If key is invalid
            ConnectionError: If communication fails
        """
        if not key:
            raise ValueError("Key must not be empty")
        
        command = f"EXISTS {key}"
        response = self._send_command(command)
        
        if response == "OK 1":
            return True
        elif response == "OK 0":
            return False
        else:
            raise RuntimeError(f"Unexpected server response: {response}")
    
    def __enter__(self):
        """Context manager entry - connects to server"""
        self.connect()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit - closes connection"""
        self.close()
        return False
