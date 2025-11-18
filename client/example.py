#!/usr/bin/env python3
"""
Example usage of the KVStore client

Make sure the C++ server is running before executing this script:
    cd server/build
    ./server
"""

import logging
from kvstore_client import KVStoreClient

# Configure logging to see client connection messages
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')


def basic_example():
    """Basic usage example"""
    print("=== Basic Example ===")
    
    # Create client
    client = KVStoreClient('localhost', 8080)
    
    try:
        # Connect to server
        client.connect()
        
        # Store some values
        print("\n1. Storing values...")
        client.set('username', 'Alice')
        client.set('email', 'alice@example.com')
        client.set('age', '25')
        print("   [OK] Stored 3 key-value pairs")
        
        # Retrieve values
        print("\n2. Retrieving values...")
        username = client.get('username')
        email = client.get('email')
        age = client.get('age')
        print(f"   username: {username}")
        print(f"   email: {email}")
        print(f"   age: {age}")
        
        # Check existence
        print("\n3. Checking existence...")
        print(f"   'username' exists: {client.exists('username')}")
        print(f"   'phone' exists: {client.exists('phone')}")
        
        # Try to get non-existent key
        print("\n4. Getting non-existent key...")
        result = client.get('nonexistent')
        print(f"   Result: {result}")
        
        # Delete a key
        print("\n5. Deleting a key...")
        deleted = client.delete('username')
        print(f"   Deleted 'username': {deleted}")
        print(f"   'username' still exists: {client.exists('username')}")
        
        # Try to delete non-existent key
        print("\n6. Deleting non-existent key...")
        deleted = client.delete('nonexistent')
        print(f"   Result: {deleted}")
        
    except ConnectionError as e:
        print(f"Connection error: {e}")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        # Always close the connection
        client.close()


def context_manager_example():
    """Example using context manager (with statement)"""
    print("\n=== Context Manager Example ===")
    
    try:
        # Connection automatically managed
        with KVStoreClient('localhost', 8080) as client:
            client.set('language', 'Python')
            client.set('project', 'kvstore')
            
            language = client.get('language')
            project = client.get('project')
            
            print(f"Language: {language}")
            print(f"Project: {project}")
        # Connection automatically closed here!
        
        print("[OK] Connection closed automatically")
        
    except ConnectionError as e:
        print(f"Connection error: {e}")
        print("Is the server running?")


def error_handling_example():
    """Example demonstrating error handling"""
    print("\n=== Error Handling Example ===")
    
    client = KVStoreClient('localhost', 8080)
    
    try:
        client.connect()
        
        # Try invalid operations
        print("\n1. Trying to set empty key...")
        try:
            client.set('', 'value')
        except ValueError as e:
            print(f"   [OK] Caught error: {e}")
        
        print("\n2. Trying to set key with spaces...")
        try:
            client.set('my key', 'value')
        except ValueError as e:
            print(f"   [OK] Caught error: {e}")
        
        print("\n3. Trying to get empty key...")
        try:
            client.get('')
        except ValueError as e:
            print(f"   [OK] Caught error: {e}")
        
    except ConnectionError as e:
        print(f"Connection error: {e}")
    finally:
        client.close()


def interactive_mode():
    """Interactive mode - like a simple CLI"""
    print("\n=== Interactive Mode ===")
    print("Commands: SET key value, GET key, DELETE key, EXISTS key, QUIT")
    
    try:
        with KVStoreClient('localhost', 8080) as client:
            while True:
                try:
                    # Get user input
                    command = input("\n> ").strip()
                    
                    if not command:
                        continue
                    
                    parts = command.split(maxsplit=2)
                    cmd = parts[0].upper()
                    
                    if cmd == 'QUIT':
                        print("Goodbye!")
                        break
                    
                    elif cmd == 'SET' and len(parts) >= 3:
                        key, value = parts[1], parts[2]
                        client.set(key, value)
                        print("OK")
                    
                    elif cmd == 'GET' and len(parts) >= 2:
                        key = parts[1]
                        value = client.get(key)
                        if value is not None:
                            print(f"OK {value}")
                        else:
                            print("ERROR KEY_NOT_FOUND")
                    
                    elif cmd == 'DELETE' and len(parts) >= 2:
                        key = parts[1]
                        deleted = client.delete(key)
                        if deleted:
                            print("OK")
                        else:
                            print("ERROR KEY_NOT_FOUND")
                    
                    elif cmd == 'EXISTS' and len(parts) >= 2:
                        key = parts[1]
                        exists = client.exists(key)
                        print(f"OK {1 if exists else 0}")
                    
                    else:
                        print("ERROR INVALID_COMMAND")
                
                except ValueError as e:
                    print(f"ERROR: {e}")
                except Exception as e:
                    print(f"ERROR: {e}")
    
    except ConnectionError as e:
        print(f"Cannot connect to server: {e}")
        print("Make sure the server is running!")


if __name__ == '__main__':
    # Run examples
    basic_example()
    context_manager_example()
    error_handling_example()
    
    # Uncomment to try interactive mode
    # interactive_mode()
