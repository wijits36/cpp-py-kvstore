"""
Tests for KVStore Client

Run with: pytest test_kvstore_client.py -v
"""

# Standard library
from unittest.mock import Mock, patch

# Third-party
import pytest

# Local
from kvstore_client import KVStoreClient

# Mark for integration tests that require a running server
integration = pytest.mark.integration

@pytest.fixture
def mock_client():
    """Create a KVStoreClient with a mocked socket"""
    client = KVStoreClient()
    client.socket = Mock()
    return client

def test_client_initialization():
    """Test that we can create a KVStoreClient instance"""
    client = KVStoreClient('localhost', 8080)
    assert client.host == 'localhost'
    assert client.port == 8080
    assert client.socket is None  # Not connected yet

def test_set_rejects_empty_key(mock_client):
    """Test that set() raises ValueError for empty key"""
    with pytest.raises(ValueError, match="Key and value must not be empty"):
        mock_client.set('', 'test_value')

def test_set_rejects_key_with_spaces(mock_client):
    """Test that set() raises ValueError for keys with spaces"""
    with pytest.raises(ValueError, match="Key cannot contain spaces"):
        mock_client.set('test key', 'test_value')

def test_get_rejects_empty_key(mock_client):
    """Test that get() raises ValueError for empty key"""
    with pytest.raises(ValueError, match="Key must not be empty"):
        mock_client.get('')

def test_delete_rejects_empty_key(mock_client):
    """Test that delete() raises ValueError for empty key"""
    with pytest.raises(ValueError, match="Key must not be empty"):
        mock_client.delete('')

def test_get_parses_success_response(mock_client):
    """Test that get() correctly parses 'OK value' response"""
    mock_client._send_command = Mock(return_value="OK test_value")
    result = mock_client.get('test_key')
    assert result == "test_value"

def test_get_returns_none_for_not_found(mock_client):
    """Test that get() returns None when key is not found"""
    mock_client._send_command = Mock(return_value="ERROR KEY_NOT_FOUND")
    result = mock_client.get('test_key')
    assert result is None

def test_exists_returns_true(mock_client):
    """Test that exists() returns True for 'OK 1' response"""
    mock_client._send_command = Mock(return_value="OK 1")
    result = mock_client.exists('test_key')
    assert result

def test_exists_returns_false(mock_client):
    """Test that exists() returns False for 'OK 0' response"""
    mock_client._send_command = Mock(return_value="OK 0")
    result = mock_client.exists('test_key')
    assert not result

@integration
def test_set_and_get_integration():
    """Integration test: Tests that set() sets a value and that get() gets a value"""
    with KVStoreClient('localhost', 8080) as client:
        client.set('test_set_and_get_integration_key', 'test_value')
        result = client.get('test_set_and_get_integration_key')
        assert result == 'test_value'

@integration
def test_delete_integration():
    """Integration test: Tests that delete() deletes a value"""
    with KVStoreClient('localhost', 8080) as client:
        client.set('test_delete_integration_key', 'test_value')
        client.delete('test_delete_integration_key')
        result = client.exists('test_delete_integration_key')
        assert not result

@integration
def test_exists_integration():
    """Integration test: Tests that exists() returns true when a value exists"""
    with KVStoreClient('localhost', 8080) as client:
        client.set('test_exists_integration_key', 'test_value')
        result = client.exists('test_exists_integration_key')
        assert result

@integration
def test_not_exists_integration():
    """Integration test: Tests that exists() returns false when a value doesn't exists"""
    with KVStoreClient('localhost', 8080) as client:
        result = client.exists('test_not_exists_integration_key')
        assert not result

@integration
def test_get_nonexistent_key_integration():
    """Integration test: GET non-existent key returns None"""
    with KVStoreClient('localhost', 8080) as client:
        result = client.get('test_get_nonexistent_key_integration_key')
        assert result is None
