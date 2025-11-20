# A Basic C++ / Python Key-Value Store

![CI Tests](https://github.com/wijits36/cpp-py-kvstore/actions/workflows/test.yml/badge.svg)

A learning project to understand C++, Python, networking, and the fundamentals of key-value databases.

## What is This?

A simple key-value store with:
- **C++ server** that stores data in memory ✓
- **Python client** to interact with the server ✓
- **Text-based protocol** for communication ✓

Think of it like a dictionary/hash map accessible over the network!

## Current Status

- [x] Protocol specification defined ([docs/protocol.md](docs/protocol.md))
- [x] C++ key-value storage class implemented
- [x] C++ TCP server with network communication
- [x] Protocol parser and command handling
- [x] Full integration and testing
- [x] Python client implementation
- [x] Comprehensive test suite (pytest)
- [x] Usage examples
- [x] CI/CD pipeline (GitHub Actions)
- [ ] Automated server management in tests
- [ ] Code coverage reporting

## Quick Start

### Prerequisites

- C++ compiler with C++17 support (g++ 7+ or clang++ 5+)
- CMake 3.10 or higher
- Python 3.7+
- pytest (for running Python tests)

### Building the Server

```bash
cd server
mkdir build && cd build
cmake ..
make
```

### Running the Server

```bash
./server
```

The server will start listening on port 8080.

### Testing the Server (Manual)

From another terminal, connect using netcat:

```bash
nc localhost 8080
```

Then try some commands:

```
SET username Alice
OK
GET username
OK Alice
EXISTS username
OK 1
DELETE username
OK
GET username
ERROR KEY_NOT_FOUND
```

### Running C++ Tests

```bash
cd server/build
./test_kvstore
```

All tests should pass ✓

### Using the Python Client

**Install dependencies:**
```bash
pip3 install pytest
```

**Basic Usage:**
```python
from kvstore_client import KVStoreClient

# Using context manager (recommended)
with KVStoreClient('localhost', 8080) as client:
    client.set('username', 'Alice')
    value = client.get('username')
    print(value)  # 'Alice'
    
    # Check if key exists
    if client.exists('username'):
        print("Key exists!")
    
    # Delete a key
    client.delete('username')
```

**Run Example Script:**
```bash
# Make sure server is running first!
cd client
python3 example.py
```

**Run Python Tests:**
```bash
cd client

# Run all tests (requires server running for integration tests)
pytest test_kvstore_client.py -v

# Run only unit tests (no server needed)
pytest test_kvstore_client.py -m "not integration" -v

# Run only integration tests (server must be running)
pytest test_kvstore_client.py -m integration -v
```

## Protocol

Simple text commands ending with `\n`:

**Available Commands:**
- `SET key value` - Store a key-value pair
- `GET key` - Retrieve a value
- `DELETE key` - Remove a key-value pair
- `EXISTS key` - Check if a key exists

**Responses:**
- `OK` - Success (for SET, DELETE)
- `OK value` - Success with data (for GET)
- `OK 1` / `OK 0` - Boolean result (for EXISTS)
- `ERROR KEY_NOT_FOUND` - Key doesn't exist
- `ERROR INVALID_COMMAND` - Unknown command
- `ERROR MISSING_ARGUMENTS` - Missing required parameters

See [docs/protocol.md](docs/protocol.md) for full details.

## Project Structure

```
cpp-py-kvstore/
├── docs/
│   └── protocol.md           # Protocol specification
├── server/                   # C++ server
│   ├── CMakeLists.txt        # Build configuration
│   ├── src/
│   │   ├── main.cpp          # Entry point
│   │   ├── server.h/cpp      # Network server
│   │   ├── kvstore.h/cpp     # Storage implementation
│   │   └── test_kvstore.cpp  # C++ tests
│   └── build/                # Build output (gitignored)
└── client/                   # Python client
    ├── kvstore_client.py     # Client library
    ├── example.py            # Usage examples
    ├── test_kvstore_client.py # Test suite
    └── pytest.ini            # Test configuration
```

## Testing

### C++ Tests
- Unit tests for `KVStore` class
- All core operations tested (set, get, delete, exists)
- Run with `./test_kvstore` from `server/build/`

### Python Tests
- **9 unit tests**: Input validation and response parsing (mocked, no server needed)
- **5 integration tests**: End-to-end testing with real C++ server
- Custom pytest markers for selective test execution
- Run with `pytest test_kvstore_client.py -v` from `client/`

### CI/CD Pipeline
- **Automated testing** via GitHub Actions on every push and pull request
- **Workflow steps**:
  1. Build C++ server
  2. Run C++ tests
  3. Run Python unit tests (no server required)
  4. Start server and run Python integration tests
  5. Automatic cleanup
- **Status badge** at top of README shows current build status
- View all test runs: [Actions tab](https://github.com/wijits36/cpp-py-kvstore/actions)

## What I'm Learning

- **C++ programming**: Classes, STL containers (`std::unordered_map`), `std::optional`
- **Python programming**: Context managers, logging, proper library design
- **Socket programming**: TCP sockets, client-server architecture
- **Protocol design**: Text-based communication protocols
- **Testing**: Unit tests, integration tests, mocking, pytest
- **CI/CD**: GitHub Actions, automated testing pipelines
- **Memory management**: RAII patterns, references vs pointers
- **Build systems**: CMake configuration
- **Git workflows**: Feature branches, pull requests, documentation

## Network Access

The server listens on all interfaces (`0.0.0.0:8080`), so you can connect from:
- Same machine: `nc localhost 8080` or use Python client
- Other machines on LAN: Connect using server's IP address

**Note:** You may need to allow port 8080 through your firewall:

```bash
# Red Hat/Fedora/CentOS
sudo firewall-cmd --add-port=8080/tcp --permanent
sudo firewall-cmd --reload
```

## Limitations

Current known limitations:
- Keys and values cannot contain spaces or newlines
- Single-threaded (handles one client at a time)
- No persistence (data lost when server stops)
- No authentication or encryption
- No maximum storage limits
- Integration tests require manual server startup locally (automated in CI)

These are acceptable for a learning project and may be addressed in future iterations.

## Future Enhancements

Potential improvements for continued learning:
- Matrix testing (test on multiple OS: Ubuntu, macOS, Windows)
- Self-hosted RHEL runner for CI
- Code coverage reporting with badges
- Automated server lifecycle in local tests
- Multi-threaded server (handle concurrent clients)
- Data persistence (save to disk)
- Additional data structures (lists, sets)
- Performance benchmarking

---

*This README grows with the project!*
