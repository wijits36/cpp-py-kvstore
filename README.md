# A Basic C++ / Python Key-Value Store

A learning project to understand C++, Python, networking, and the fundamentals of key-value databases.

## What is This?

A simple key-value store with:
- **C++ server** that stores data in memory ✓
- **Python client** to interact with the server (coming soon)
- **Text-based protocol** for communication ✓

Think of it like a dictionary/hash map accessible over the network!

## Current Status

- [x] Protocol specification defined ([docs/protocol.md](docs/protocol.md))
- [x] C++ key-value storage class implemented
- [x] C++ TCP server with network communication
- [x] Protocol parser and command handling
- [x] Full integration and testing
- [ ] Python client implementation
- [ ] Usage examples
- [ ] Documentation improvements

## Quick Start

### Prerequisites
- C++ compiler with C++17 support (g++ 7+ or clang++ 5+)
- CMake 3.10 or higher
- Python 3.7+ (for client, coming soon)

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

### Testing the Server

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

### Running Tests

```bash
cd server/build
./test_kvstore
```

All tests should pass ✓

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
│   └── protocol.md      # Protocol specification
├── server/              # C++ server
│   ├── CMakeLists.txt   # Build configuration
│   ├── src/
│   │   ├── main.cpp     # Entry point
│   │   ├── server.h/cpp # Network server
│   │   ├── kvstore.h/cpp # Storage implementation
│   │   └── test_kvstore.cpp # Tests
│   └── build/           # Build output (gitignored)
└── client/              # Python client (coming soon)
```

## What I'm Learning

- **C++ programming**: Classes, STL containers (`std::unordered_map`), `std::optional`
- **Socket programming**: TCP sockets, client-server architecture
- **Protocol design**: Text-based communication protocols
- **Memory management**: RAII patterns, references vs pointers
- **Build systems**: CMake configuration
- **Git workflows**: Feature branches, pull requests, documentation

## Network Access

The server listens on all interfaces (`0.0.0.0:8080`), so you can connect from:
- Same machine: `nc localhost 8080`
- Other machines on LAN: `nc <server-ip> 8080`

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

These are acceptable for a learning project and may be addressed in future iterations.

---

*This README grows with the project!*
