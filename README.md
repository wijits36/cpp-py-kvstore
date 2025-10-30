# A Basic C++ / Python Key-Value Store

A learning project to understand C++, Python, networking, and the fundamentals of key-value databases.

## What is This?

A simple key-value store with:
- **C++ server** that stores data in memory
- **Python client** to interact with the server
- **Text-based protocol** for communication

Think of it like a dictionary/hash map accessible over the network!

## Current Status

- [x] Protocol specification defined ([docs/protocol.md](docs/protocol.md))
- [ ] C++ server implementation
- [ ] Python client implementation
- [ ] Examples and testing

## Protocol

Simple text commands ending with `\n`:

```
Client: SET username Alice
Server: OK

Client: GET username
Server: OK Alice
```

See [docs/protocol.md](docs/protocol.md) for full details.

## Project Structure

```
cpp-py-kvstore/
├── docs/           # Documentation
├── server/         # C++ server (coming soon)
└── client/         # Python client (coming soon)
```

---

*This README will expand as the project grows!*
